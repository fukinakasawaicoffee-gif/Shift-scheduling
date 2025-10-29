from typing import List, Dict, Tuple
from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.shift_pattern import ShiftPattern
from app.models.shift_requirement import ShiftRequirement
from app.models.leave_request import LeaveRequest, LeaveRequestStatus
from app.models.schedule import Schedule
from app.optimizer.shift_optimizer import (
    ShiftOptimizer,
    Employee as OptimizerEmployee,
    ShiftPattern as OptimizerShiftPattern,
    ShiftRequirement as OptimizerShiftRequirement,
    LeaveRequest as OptimizerLeaveRequest,
)


class ScheduleService:
    """スケジュール生成サービス"""

    def __init__(self, db: Session):
        self.db = db

    def generate_schedule(
        self,
        department_id: int,
        start_date: date,
        end_date: date,
        time_limit_seconds: int = 300,
    ) -> Dict:
        """部署のシフトを自動生成"""

        # 1. 従業員データを取得
        employees = (
            self.db.query(Employee)
            .filter(
                Employee.department_id == department_id,
                Employee.is_active == True
            )
            .all()
        )

        if not employees:
            return {
                "success": False,
                "message": "対象となる従業員が見つかりません",
                "schedules_created": 0,
                "statistics": {},
            }

        # 2. シフトパターンを取得
        shift_patterns = (
            self.db.query(ShiftPattern)
            .filter(
                ShiftPattern.department_id == department_id,
                ShiftPattern.is_active == True
            )
            .all()
        )

        if not shift_patterns:
            return {
                "success": False,
                "message": "シフトパターンが設定されていません",
                "schedules_created": 0,
                "statistics": {},
            }

        # 3. シフト必要人数を取得
        shift_requirements = (
            self.db.query(ShiftRequirement)
            .filter(
                ShiftRequirement.department_id == department_id,
                ShiftRequirement.date >= start_date,
                ShiftRequirement.date <= end_date
            )
            .all()
        )

        # 4. 承認済みの休暇申請を取得
        leave_requests = (
            self.db.query(LeaveRequest)
            .join(Employee)
            .filter(
                Employee.department_id == department_id,
                LeaveRequest.status == LeaveRequestStatus.APPROVED,
                LeaveRequest.start_date <= end_date,
                LeaveRequest.end_date >= start_date
            )
            .all()
        )

        # 5. オプティマイザー用のデータに変換
        optimizer_employees = [
            OptimizerEmployee(
                id=emp.id,
                name=f"{emp.last_name} {emp.first_name}",
                can_work_shifts=[sp.id for sp in shift_patterns]
            )
            for emp in employees
        ]

        optimizer_shift_patterns = [
            OptimizerShiftPattern(
                id=sp.id,
                name=sp.name,
                shift_type=sp.shift_type.value
            )
            for sp in shift_patterns
        ]

        optimizer_requirements = []
        for req in shift_requirements:
            optimizer_requirements.append(
                OptimizerShiftRequirement(
                    date=req.date,
                    shift_pattern_id=req.shift_pattern_id,
                    required_count=req.required_count
                )
            )

        # 休暇申請を日付ごとに展開
        optimizer_leaves = []
        for leave in leave_requests:
            current_date = max(leave.start_date, start_date)
            end = min(leave.end_date, end_date)

            while current_date <= end:
                optimizer_leaves.append(
                    OptimizerLeaveRequest(
                        employee_id=leave.employee_id,
                        date=current_date,
                        leave_type=leave.leave_type.value
                    )
                )
                current_date += timedelta(days=1)

        # 6. 最適化を実行
        # 部署設定から制約を取得
        from app.models.department import Department
        dept = self.db.query(Department).filter(Department.id == department_id).first()

        optimizer = ShiftOptimizer(
            employees=optimizer_employees,
            shift_patterns=optimizer_shift_patterns,
            date_range=(start_date, end_date),
            shift_requirements=optimizer_requirements,
            leave_requests=optimizer_leaves,
            max_regular_holidays=dept.max_regular_holidays_per_month if dept else 8,
            max_consecutive_work_days=dept.max_consecutive_work_days if dept else 6,
        )

        result = optimizer.optimize(time_limit_seconds=time_limit_seconds)

        if not result.success:
            return {
                "success": False,
                "message": result.message,
                "schedules_created": 0,
                "statistics": result.statistics,
            }

        # 7. 結果をデータベースに保存
        schedules_created = 0

        # 既存のシステム生成スケジュールを削除（期間内）
        self.db.query(Schedule).filter(
            Schedule.employee_id.in_([emp.id for emp in employees]),
            Schedule.date >= start_date,
            Schedule.date <= end_date,
            Schedule.generated_by_system == True
        ).delete(synchronize_session=False)

        # 新しいスケジュールを作成
        for (emp_id, schedule_date, shift_id), assigned in result.schedule.items():
            if assigned:
                schedule = Schedule(
                    employee_id=emp_id,
                    shift_pattern_id=shift_id,
                    date=schedule_date,
                    is_holiday=False,
                    generated_by_system=True,
                    is_confirmed=False,
                    is_published=False,
                )
                self.db.add(schedule)
                schedules_created += 1

        # 休暇申請に基づく休日スケジュールを作成
        for leave in optimizer_leaves:
            # 重複チェック
            existing = self.db.query(Schedule).filter(
                Schedule.employee_id == leave.employee_id,
                Schedule.date == leave.date
            ).first()

            if not existing:
                schedule = Schedule(
                    employee_id=leave.employee_id,
                    shift_pattern_id=None,
                    date=leave.date,
                    is_holiday=True,
                    holiday_type=leave.leave_type,
                    generated_by_system=True,
                    is_confirmed=False,
                    is_published=False,
                )
                self.db.add(schedule)
                schedules_created += 1

        self.db.commit()

        return {
            "success": True,
            "message": result.message,
            "schedules_created": schedules_created,
            "statistics": result.statistics,
        }
