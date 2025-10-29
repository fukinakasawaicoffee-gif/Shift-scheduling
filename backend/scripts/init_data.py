"""
初期データ投入スクリプト
管理者ユーザー、サンプル部署、シフトパターンを作成します。
"""
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).parent.parent))

from datetime import date, time
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User
from app.models.department import Department
from app.models.shift_pattern import ShiftPattern, ShiftType


def init_db():
    db = SessionLocal()

    try:
        # 1. 管理者ユーザーの作成
        print("管理者ユーザーを作成中...")
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                email="admin@example.com",
                username="admin",
                hashed_password=get_password_hash("admin123"),
                full_name="システム管理者",
                is_active=True,
                is_superuser=True,
            )
            db.add(admin_user)
            db.commit()
            print("✓ 管理者ユーザーを作成しました (username: admin, password: admin123)")
        else:
            print("✓ 管理者ユーザーは既に存在します")

        # 2. サンプル部署の作成
        print("\nサンプル部署を作成中...")
        departments_data = [
            {
                "name": "販売部",
                "code": "SALES",
                "description": "店舗販売を担当する部署",
                "max_regular_holidays_per_month": 8,
                "max_consecutive_work_days": 6,
            },
            {
                "name": "物流部",
                "code": "LOGISTICS",
                "description": "商品の入出荷を担当する部署",
                "max_regular_holidays_per_month": 8,
                "max_consecutive_work_days": 5,
            },
            {
                "name": "カスタマーサポート部",
                "code": "CS",
                "description": "顧客サポートを担当する部署",
                "max_regular_holidays_per_month": 8,
                "max_consecutive_work_days": 6,
            },
        ]

        for dept_data in departments_data:
            dept = db.query(Department).filter(Department.code == dept_data["code"]).first()
            if not dept:
                dept = Department(**dept_data)
                db.add(dept)
                db.commit()
                db.refresh(dept)
                print(f"✓ 部署「{dept.name}」を作成しました")

                # 3. シフトパターンの作成
                create_shift_patterns_for_department(db, dept)
            else:
                print(f"✓ 部署「{dept.name}」は既に存在します")

        print("\n初期データの投入が完了しました！")
        print("\n次のステップ:")
        print("1. http://localhost:3000 にアクセス")
        print("2. ログイン (username: admin, password: admin123)")
        print("3. 従業員を登録してシフトを生成")

    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        db.rollback()
    finally:
        db.close()


def create_shift_patterns_for_department(db: SessionLocal, department: Department):
    """部署のシフトパターンを作成"""
    print(f"  部署「{department.name}」のシフトパターンを作成中...")

    if department.code == "SALES":
        # 販売部のシフトパターン
        patterns = [
            {
                "name": "早番A",
                "code": "EA",
                "shift_type": ShiftType.EARLY,
                "start_time": time(5, 0),
                "end_time": time(14, 0),
                "work_hours": 480,  # 8時間（休憩1時間含む9時間勤務）
                "color_code": "#FF6B6B",
            },
            {
                "name": "早番B",
                "code": "EB",
                "shift_type": ShiftType.EARLY,
                "start_time": time(6, 0),
                "end_time": time(15, 0),
                "work_hours": 480,
                "color_code": "#FFA07A",
            },
            {
                "name": "普通番",
                "code": "N",
                "shift_type": ShiftType.NORMAL,
                "start_time": time(9, 0),
                "end_time": time(18, 0),
                "work_hours": 480,
                "color_code": "#4ECDC4",
            },
            {
                "name": "遅番A",
                "code": "LA",
                "shift_type": ShiftType.LATE,
                "start_time": time(13, 0),
                "end_time": time(22, 0),
                "work_hours": 480,
                "color_code": "#95E1D3",
            },
            {
                "name": "遅番B",
                "code": "LB",
                "shift_type": ShiftType.LATE,
                "start_time": time(14, 0),
                "end_time": time(23, 0),
                "work_hours": 480,
                "color_code": "#A8E6CF",
            },
        ]
    elif department.code == "LOGISTICS":
        # 物流部のシフトパターン
        patterns = [
            {
                "name": "早番",
                "code": "E",
                "shift_type": ShiftType.EARLY,
                "start_time": time(6, 0),
                "end_time": time(15, 0),
                "work_hours": 480,
                "color_code": "#FF6B6B",
            },
            {
                "name": "普通番",
                "code": "N",
                "shift_type": ShiftType.NORMAL,
                "start_time": time(9, 0),
                "end_time": time(18, 0),
                "work_hours": 480,
                "color_code": "#4ECDC4",
            },
            {
                "name": "遅番",
                "code": "L",
                "shift_type": ShiftType.LATE,
                "start_time": time(13, 0),
                "end_time": time(22, 0),
                "work_hours": 480,
                "color_code": "#95E1D3",
            },
        ]
    else:
        # カスタマーサポート部のシフトパターン
        patterns = [
            {
                "name": "早番",
                "code": "E",
                "shift_type": ShiftType.EARLY,
                "start_time": time(7, 0),
                "end_time": time(16, 0),
                "work_hours": 480,
                "color_code": "#FF6B6B",
            },
            {
                "name": "普通番",
                "code": "N",
                "shift_type": ShiftType.NORMAL,
                "start_time": time(9, 0),
                "end_time": time(18, 0),
                "work_hours": 480,
                "color_code": "#4ECDC4",
            },
            {
                "name": "遅番",
                "code": "L",
                "shift_type": ShiftType.LATE,
                "start_time": time(12, 0),
                "end_time": time(21, 0),
                "work_hours": 480,
                "color_code": "#95E1D3",
            },
        ]

    for pattern_data in patterns:
        pattern = ShiftPattern(
            department_id=department.id,
            **pattern_data
        )
        db.add(pattern)

    db.commit()
    print(f"  ✓ {len(patterns)}個のシフトパターンを作成しました")


if __name__ == "__main__":
    init_db()
