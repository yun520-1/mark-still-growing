#!/usr/bin/env python3
"""
父母的功课 - 教育目标追踪系统
家庭教育目标追踪系统

帮助家庭设定、追踪和达成教育目标。

用法:
    python3 scripts/goal_tracker.py --create    # 创建目标
    python3 scripts/goal_tracker.py --dashboard # 查看仪表板
    python3 scripts/goal_tracker.py --list     # 列出所有目标
    python3 scripts/goal_tracker.py --progress # 添加进度

来源: OpenClaw still-growing goal_tracker.py
整合: v0.9.58
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Optional
from enum import Enum

# 数据目录
DATA_DIR = Path.home() / ".hermes" / "still_growing"
DATA_DIR.mkdir(parents=True, exist_ok=True)
GOALS_FILE = DATA_DIR / "goals.json"


class GoalStatus(Enum):
    """目标状态枚举"""
    NOT_STARTED = "未开始"
    IN_PROGRESS = "进行中"
    COMPLETED = "已完成"
    PAUSED = "已暂停"
    CANCELLED = "已取消"


class GoalCategory(Enum):
    """目标类别枚举"""
    COMMUNICATION = "沟通改善"
    DISCIPLINE = "纪律管教"
    EMOTION = "情绪管理"
    ROUTINE = "习惯养成"
    EDUCATION = "学业支持"
    RELATIONSHIP = "亲子关系"
    OTHER = "其他"


class GoalTracker:
    """教育目标追踪类"""

    def __init__(self, data_file: Path = None):
        self.data_file = data_file or GOALS_FILE

    def load_goals(self) -> List[Dict]:
        """加载目标列表"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_goals(self, goals: List[Dict]):
        """保存目标列表"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(goals, f, ensure_ascii=False, indent=2)

    def create_goal(
        self,
        title: str,
        description: str,
        category: str,
        target_date: str = None,
        milestones: List[Dict] = None
    ) -> Dict:
        """创建新目标"""
        goal = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "title": title,
            "description": description,
            "category": category,
            "status": GoalStatus.NOT_STARTED.value,
            "target_date": target_date,
            "milestones": milestones or [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "progress": 0,
            "check_ins": []
        }

        goals = self.load_goals()
        goals.append(goal)
        self.save_goals(goals)

        return goal

    def get_goals_by_status(self, status: str) -> List[Dict]:
        """按状态获取目标"""
        goals = self.load_goals()
        return [g for g in goals if g['status'] == status]

    def get_goals_by_category(self, category: str) -> List[Dict]:
        """按类别获取目标"""
        goals = self.load_goals()
        return [g for g in goals if g['category'] == category]

    def update_goal_status(self, goal_id: str, status: str, notes: str = "") -> bool:
        """更新目标状态"""
        goals = self.load_goals()

        for goal in goals:
            if goal['id'] == goal_id:
                goal['status'] = status
                goal['updated_at'] = datetime.now().isoformat()

                # 添加检查点
                goal['check_ins'].append({
                    "timestamp": datetime.now().isoformat(),
                    "from_status": goal['status'],
                    "to_status": status,
                    "notes": notes
                })

                self.save_goals(goals)
                return True

        return False

    def add_progress(self, goal_id: str, progress_delta: int, notes: str = "") -> bool:
        """添加进度"""
        goals = self.load_goals()

        for goal in goals:
            if goal['id'] == goal_id:
                goal['progress'] = min(100, max(0, goal['progress'] + progress_delta))
                goal['updated_at'] = datetime.now().isoformat()

                # 如果达到100%，自动标记为完成
                if goal['progress'] >= 100:
                    goal['status'] = GoalStatus.COMPLETED.value

                # 添加检查点
                goal['check_ins'].append({
                    "timestamp": datetime.now().isoformat(),
                    "progress_delta": progress_delta,
                    "new_progress": goal['progress'],
                    "notes": notes
                })

                self.save_goals(goals)
                return True

        return False

    def get_dashboard_summary(self) -> Dict:
        """获取仪表板摘要"""
        goals = self.load_goals()

        summary = {
            "total": len(goals),
            "by_status": {},
            "by_category": {},
            "avg_progress": 0,
            "upcoming_deadlines": [],
            "recent_check_ins": []
        }

        total_progress = 0
        now = datetime.now()

        for goal in goals:
            # 按状态统计
            status = goal['status']
            summary["by_status"][status] = summary["by_status"].get(status, 0) + 1

            # 按类别统计
            category = goal['category']
            summary["by_category"][category] = summary["by_category"].get(category, 0) + 1

            # 平均进度
            total_progress += goal['progress']

            # 即将到期
            if goal.get('target_date'):
                try:
                    target = datetime.fromisoformat(goal['target_date'])
                    days_left = (target - now).days
                    if 0 <= days_left <= 7 and goal['status'] == GoalStatus.IN_PROGRESS.value:
                        summary["upcoming_deadlines"].append({
                            "title": goal['title'],
                            "days_left": days_left,
                            "progress": goal['progress']
                        })
                except ValueError:
                    pass

            # 最近的检查点
            if goal['check_ins']:
                last_check = goal['check_ins'][-1]
                summary["recent_check_ins"].append({
                    "goal_title": goal['title'],
                    "timestamp": last_check['timestamp'],
                    "notes": last_check.get('notes', '')
                })

        summary["recent_check_ins"] = sorted(
            summary["recent_check_ins"],
            key=lambda x: x['timestamp'],
            reverse=True
        )[:5]

        if goals:
            summary["avg_progress"] = round(total_progress / len(goals), 1)

        return summary

    def interactive_create(self):
        """交互式创建目标"""
        print("\n" + "=" * 50)
        print("创建新的教育目标")
        print("=" * 50)

        # 标题
        title = input("目标标题: ").strip()
        if not title:
            print("标题不能为空")
            return None

        # 描述
        description = input("目标描述: ").strip()

        # 类别
        print("\n目标类别:")
        for i, cat in enumerate(GoalCategory, 1):
            print(f"  {i}. {cat.value}")

        cat_choice = input("请选择类别(1-7): ").strip()
        try:
            category = list(GoalCategory)[int(cat_choice) - 1].value
        except (ValueError, IndexError):
            category = GoalCategory.OTHER.value

        # 目标日期
        target_date = input("目标日期(YYYY-MM-DD，可选): ").strip()
        if target_date:
            try:
                datetime.strptime(target_date, "%Y-%m-%d")
            except ValueError:
                print("日期格式错误，已跳过")
                target_date = None

        # 里程碑
        milestones = []
        print("\n添加里程碑（输入空行结束）:")
        while True:
            milestone_text = input("  里程碑: ").strip()
            if not milestone_text:
                break
            milestones.append({
                "text": milestone_text,
                "completed": False
            })

        # 创建目标
        goal = self.create_goal(
            title=title,
            description=description,
            category=category,
            target_date=target_date,
            milestones=milestones
        )

        print(f"\n✅ 目标已创建: {goal['id']}")
        return goal

    def print_dashboard(self, summary: Dict):
        """打印仪表板"""
        print("\n" + "=" * 50)
        print("家庭教育目标仪表板")
        print("=" * 50)

        print(f"\n总目标数: {summary['total']}")
        print(f"平均进度: {summary['avg_progress']}%")

        print("\n【按状态分布】:")
        for status, count in summary["by_status"].items():
            bar = "█" * count
            print(f"  {status}: {count}个 {bar}")

        print("\n【按类别分布】:")
        for category, count in summary["by_category"].items():
            bar = "█" * count
            print(f"  {category}: {count}个 {bar}")

        if summary["upcoming_deadlines"]:
            print("\n【即将到期】:")
            for item in summary["upcoming_deadlines"]:
                print(f"  • {item['title']} (剩余{item['days_left']}天, {item['progress']}%)")

        if summary["recent_check_ins"]:
            print("\n【最近更新】:")
            for item in summary["recent_check_ins"]:
                date = item['timestamp'][:10]
                print(f"  • [{date}] {item['goal_title']}")

        print("=" * 50)


def main():
    args = sys.argv[1:]
    tracker = GoalTracker()

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    if "--create" in args:
        tracker.interactive_create()
        return

    if "--dashboard" in args:
        summary = tracker.get_dashboard_summary()
        tracker.print_dashboard(summary)
        return

    if "--list" in args:
        goals = tracker.load_goals()
        if not goals:
            print("暂无目标")
            return
        print("\n【所有目标】:")
        for g in goals:
            print(f"  [{g['status']}] {g['title']} ({g['progress']}%)")
        return

    if "--progress" in args:
        goals = tracker.load_goals()
        if not goals:
            print("暂无目标")
            return
        print("\n【选择目标】:")
        for i, g in enumerate(goals, 1):
            print(f"  {i}. {g['title']} (当前: {g['progress']}%)")
        choice = input("\n选择目标编号: ").strip()
        try:
            idx = int(choice) - 1
            goal = goals[idx]
            delta = int(input("添加进度(+/-): ").strip())
            notes = input("备注: ").strip()
            tracker.add_progress(goal['id'], delta, notes)
            print(f"✅ 进度已更新")
        except (ValueError, IndexError):
            print("无效选择")
        return

    # 默认显示仪表板
    summary = tracker.get_dashboard_summary()
    tracker.print_dashboard(summary)


if __name__ == "__main__":
    main()
