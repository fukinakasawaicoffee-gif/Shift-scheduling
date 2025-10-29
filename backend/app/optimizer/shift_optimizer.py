from ortools.sat.python import cp_model
from typing import List, Dict, Tuple, Optional
from datetime import datetime, date, timedelta
from dataclasses import dataclass


@dataclass
class Employee:
    """従業員データ"""
    id: int
    name: str
    can_work_shifts: List[int]  # 勤務可能なシフトパターンID


@dataclass
class ShiftPattern:
    """シフトパターンデータ"""
    id: int
    name: str
    shift_type: str


@dataclass
class ShiftRequirement:
    """シフト必要人数データ"""
    date: date
    shift_pattern_id: int
    required_count: int


@dataclass
class LeaveRequest:
    """休暇申請データ"""
    employee_id: int
    date: date
    leave_type: str


@dataclass
class OptimizationResult:
    """最適化結果"""
    success: bool
    schedule: Dict[Tuple[int, date, int], bool]  # (employee_id, date, shift_pattern_id) -> assigned
    message: str
    statistics: Dict


class ShiftOptimizer:
    """シフト最適化エンジン - Google OR-Toolsを使用"""

    def __init__(
        self,
        employees: List[Employee],
        shift_patterns: List[ShiftPattern],
        date_range: Tuple[date, date],
        shift_requirements: List[ShiftRequirement],
        leave_requests: List[LeaveRequest],
        max_regular_holidays: int = 8,
        max_consecutive_work_days: int = 6,
    ):
        self.employees = employees
        self.shift_patterns = shift_patterns
        self.start_date, self.end_date = date_range
        self.shift_requirements = shift_requirements
        self.leave_requests = leave_requests
        self.max_regular_holidays = max_regular_holidays
        self.max_consecutive_work_days = max_consecutive_work_days

        # 日付リストを生成
        self.dates = []
        current_date = self.start_date
        while current_date <= self.end_date:
            self.dates.append(current_date)
            current_date += timedelta(days=1)

        # 休暇申請をマップに変換
        self.leave_map = {}
        for leave in leave_requests:
            if leave.employee_id not in self.leave_map:
                self.leave_map[leave.employee_id] = []
            self.leave_map[leave.employee_id].append(leave.date)

        # 必要人数をマップに変換
        self.requirement_map = {}
        for req in shift_requirements:
            key = (req.date, req.shift_pattern_id)
            self.requirement_map[key] = req.required_count

    def optimize(self, time_limit_seconds: int = 300) -> OptimizationResult:
        """シフト最適化を実行"""
        model = cp_model.CpModel()

        # 変数定義: shifts[(emp_id, date, shift_id)] = BoolVar
        shifts = {}
        for emp in self.employees:
            for d in self.dates:
                # 休暇申請がある場合はスキップ
                if emp.id in self.leave_map and d in self.leave_map[emp.id]:
                    continue

                for shift in self.shift_patterns:
                    if shift.id in emp.can_work_shifts:
                        shifts[(emp.id, d, shift.id)] = model.NewBoolVar(
                            f"shift_e{emp.id}_d{d}_s{shift.id}"
                        )

        # 制約1: 各従業員は1日に最大1シフト
        for emp in self.employees:
            for d in self.dates:
                # 休暇申請がある日はスキップ
                if emp.id in self.leave_map and d in self.leave_map[emp.id]:
                    continue

                daily_shifts = [
                    shifts[(emp.id, d, shift.id)]
                    for shift in self.shift_patterns
                    if (emp.id, d, shift.id) in shifts
                ]
                if daily_shifts:
                    model.Add(sum(daily_shifts) <= 1)

        # 制約2: 必要人数を満たす
        for d in self.dates:
            for shift in self.shift_patterns:
                required = self.requirement_map.get((d, shift.id), 0)
                if required > 0:
                    assigned = [
                        shifts[(emp.id, d, shift.id)]
                        for emp in self.employees
                        if (emp.id, d, shift.id) in shifts
                    ]
                    if assigned:
                        model.Add(sum(assigned) >= required)

        # 制約3: 月の休日数（通常休日は最大max_regular_holidays日）
        total_days = len(self.dates)
        for emp in self.employees:
            # 従業員が働く日数
            work_days = [
                shifts[(emp.id, d, shift.id)]
                for d in self.dates
                for shift in self.shift_patterns
                if (emp.id, d, shift.id) in shifts
            ]

            # 休暇申請の日数を計算
            leave_days = len([d for d in self.dates if emp.id in self.leave_map and d in self.leave_map[emp.id]])

            if work_days:
                # 勤務日数 <= 総日数 - 最大休日数 - 休暇日数
                max_work_days = total_days - self.max_regular_holidays - leave_days
                model.Add(sum(work_days) <= max_work_days)

        # 制約4: 連続勤務日数の制限
        for emp in self.employees:
            for i in range(len(self.dates) - self.max_consecutive_work_days):
                consecutive_days = []
                for j in range(self.max_consecutive_work_days + 1):
                    d = self.dates[i + j]
                    # 休暇申請がある日はスキップ
                    if emp.id in self.leave_map and d in self.leave_map[emp.id]:
                        continue

                    day_shifts = [
                        shifts[(emp.id, d, shift.id)]
                        for shift in self.shift_patterns
                        if (emp.id, d, shift.id) in shifts
                    ]
                    if day_shifts:
                        consecutive_days.extend(day_shifts)

                # 連続する(max_consecutive_work_days + 1)日間のうち、少なくとも1日は休み
                if consecutive_days:
                    model.Add(sum(consecutive_days) <= self.max_consecutive_work_days)

        # 目的関数: シフトの公平性（各従業員の勤務日数を均等に）
        work_day_counts = []
        for emp in self.employees:
            work_days = [
                shifts[(emp.id, d, shift.id)]
                for d in self.dates
                for shift in self.shift_patterns
                if (emp.id, d, shift.id) in shifts
            ]
            if work_days:
                work_day_counts.append(sum(work_days))

        # 勤務日数の分散を最小化（簡易版：最小と最大の差を最小化）
        if len(work_day_counts) >= 2:
            min_work = model.NewIntVar(0, total_days, "min_work")
            max_work = model.NewIntVar(0, total_days, "max_work")

            for count in work_day_counts:
                model.Add(min_work <= count)
                model.Add(max_work >= count)

            # 最大と最小の差を最小化
            diff = model.NewIntVar(0, total_days, "diff")
            model.Add(diff == max_work - min_work)
            model.Minimize(diff)

        # ソルバー実行
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit_seconds
        solver.parameters.log_search_progress = True

        status = solver.Solve(model)

        # 結果を抽出
        schedule = {}
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            for (emp_id, d, shift_id), var in shifts.items():
                schedule[(emp_id, d, shift_id)] = solver.Value(var) == 1

            return OptimizationResult(
                success=True,
                schedule=schedule,
                message=f"最適化成功: {'最適解' if status == cp_model.OPTIMAL else '実行可能解'}が見つかりました",
                statistics={
                    "status": "optimal" if status == cp_model.OPTIMAL else "feasible",
                    "wall_time": solver.WallTime(),
                    "objective_value": solver.ObjectiveValue() if len(work_day_counts) >= 2 else 0,
                },
            )
        else:
            return OptimizationResult(
                success=False,
                schedule={},
                message=f"最適化失敗: 制約を満たす解が見つかりませんでした（ステータス: {status}）",
                statistics={
                    "status": "infeasible",
                    "wall_time": solver.WallTime(),
                },
            )
