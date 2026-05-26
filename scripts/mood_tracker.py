#!/usr/bin/env python3
"""
父母的功课 - 亲子互动情绪追踪系统
Parent-Child Interaction Mood Tracker

追踪和记录亲子互动中的情绪变化，帮助识别模式和触发因素。

用法:
    python3 scripts/mood_tracker.py --add    # 添加记录
    python3 scripts/mood_tracker.py --stats 30  # 分析最近30天

来源: OpenClaw still-growing mood_tracker.py
整合: v0.9.60
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

# 数据目录
DATA_DIR = Path.home() / ".hermes" / "still_growing"
DATA_DIR.mkdir(parents=True, exist_ok=True)
RECORDS_FILE = DATA_DIR / "mood_records.json"

# 情绪词汇表
MOOD_POSITIVE = ["开心", "快乐", "温暖", "满足", "自豪", "平静", "被爱", "被理解", "连接"]
MOOD_NEGATIVE = ["愤怒", "沮丧", "焦虑", "失望", "无奈", "疲惫", "受伤", "被拒绝", "挫败"]
MOOD_NEUTRAL = ["平静", "一般", "无所谓", "中性"]

# 触发因素列表
TRIGGER_FACTORS = [
    "作业/学业压力",
    "电子产品使用",
    "作息时间",
    "饮食问题",
    "兄弟姐妹冲突",
    "外出/社交",
    "早晨准备",
    "bedtime睡前",
    "餐桌时间",
    "学习辅导",
    "零花钱/物质",
    "其他"
]


class MoodTracker:
    """亲子互动情绪追踪类"""

    def __init__(self, data_file: Path = None):
        self.data_file = data_file or RECORDS_FILE

    def load_records(self) -> List[Dict]:
        """加载情绪记录"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_records(self, records: List[Dict]):
        """保存情绪记录"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

    def add_record(
        self,
        parent_mood: str,
        child_mood: str,
        interaction_type: str,
        trigger: str,
        notes: str = "",
        intensity: int = 5
    ) -> Dict:
        """添加情绪记录"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "parent_mood": parent_mood,
            "child_mood": child_mood,
            "interaction_type": interaction_type,
            "trigger": trigger,
            "intensity": intensity,
            "notes": notes,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        records = self.load_records()
        records.append(record)
        self.save_records(records)

        return record

    def get_records_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """按日期范围获取记录"""
        records = self.load_records()
        filtered = []

        for record in records:
            record_date = record['created_at'][:10]
            if start_date <= record_date <= end_date:
                filtered.append(record)

        return filtered

    def analyze_patterns(self, days: int = 30) -> Dict:
        """分析情绪模式"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        records = self.get_records_by_date_range(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )

        if not records:
            return {"message": f"过去{days}天没有记录"}

        analysis = {
            "period": f"{start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}",
            "total_records": len(records),
            "parent_moods": defaultdict(int),
            "child_moods": defaultdict(int),
            "triggers": defaultdict(int),
            "avg_intensity": 0,
            "daily_distribution": defaultdict(int)
        }

        total_intensity = 0

        for record in records:
            analysis["parent_moods"][record["parent_mood"]] += 1
            analysis["child_moods"][record["child_mood"]] += 1
            analysis["triggers"][record["trigger"]] += 1
            total_intensity += record["intensity"]
            analysis["daily_distribution"][record["created_at"][:10]] += 1

        analysis["avg_intensity"] = round(total_intensity / len(records), 1)

        # 找出最常见的触发因素
        analysis["top_triggers"] = dict(sorted(
            analysis["triggers"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5])

        return analysis

    def get_daily_summary(self) -> str:
        """获取每日摘要"""
        today = datetime.now().strftime("%Y-%m-%d")
        records = self.get_records_by_date_range(today, today)

        if not records:
            return "今天还没有记录"

        positive = sum(1 for r in records if r['parent_mood'] in MOOD_POSITIVE)
        negative = sum(1 for r in records if r['parent_mood'] in MOOD_NEGATIVE)

        summary = f"今日记录: {len(records)}条 | "
        summary += f"正面: {positive}次 | "
        summary += f"负面: {negative}次"

        return summary

    def print_analysis(self, analysis: Dict):
        """打印分析结果"""
        print("\n" + "=" * 50)
        print("情绪模式分析报告")
        print("=" * 50)

        print(f"\n【分析周期】: {analysis.get('period', 'N/A')}")
        print(f"【记录总数】: {analysis.get('total_records', 0)}")
        print(f"【平均强度】: {analysis.get('avg_intensity', 0)}/10")

        print("\n【父母情绪分布】:")
        for mood, count in sorted(analysis["parent_moods"].items(), key=lambda x: x[1], reverse=True):
            bar = "█" * count
            print(f"  {mood}: {count}次 {bar}")

        print("\n【触发因素 TOP5】:")
        for trigger, count in analysis.get("top_triggers", {}).items():
            bar = "█" * count
            print(f"  {trigger}: {count}次 {bar}")

        print("\n【每日记录分布】:")
        for date, count in sorted(analysis.get("daily_distribution", {}).items()):
            bar = "█" * count
            print(f"  {date}: {count}次 {bar}")

        print("=" * 50)

    def interactive_add(self):
        """交互式添加记录"""
        print("\n" + "=" * 50)
        print("添加亲子互动情绪记录")
        print("=" * 50)

        # 父母情绪
        print("\n【父母情绪】")
        print("正面情绪:", ", ".join(MOOD_POSITIVE[:5]))
        print("负面情绪:", ", ".join(MOOD_NEGATIVE[:5]))
        parent_mood = input("请输入父母情绪: ").strip()

        # 孩子情绪
        print("\n【孩子情绪】")
        child_mood = input("请输入孩子情绪: ").strip()

        # 互动类型
        print("\n【互动类型】")
        print("1. 日常沟通  2. 作业辅导  3. 冲突/争吵  4. 游戏/活动  5. 其他")
        interaction_map = {"1": "日常沟通", "2": "作业辅导", "3": "冲突/争吵", "4": "游戏/活动", "5": "其他"}
        interaction_choice = input("请选择(1-5): ").strip()
        interaction_type = interaction_map.get(interaction_choice, "其他")

        # 触发因素
        print("\n【触发因素】")
        for i, trigger in enumerate(TRIGGER_FACTORS, 1):
            print(f"  {i}. {trigger}")
        trigger_choice = input("请选择或输入自定义因素: ").strip()
        if trigger_choice.isdigit() and 1 <= int(trigger_choice) <= len(TRIGGER_FACTORS):
            trigger = TRIGGER_FACTORS[int(trigger_choice) - 1]
        else:
            trigger = trigger_choice

        # 强度
        intensity_input = input("\n情绪强度(1-10，10最强): ").strip()
        intensity = int(intensity_input) if intensity_input else 5

        # 备注
        notes = input("备注(可选): ").strip()

        # 保存
        record = self.add_record(
            parent_mood=parent_mood,
            child_mood=child_mood,
            interaction_type=interaction_type,
            trigger=trigger,
            notes=notes,
            intensity=intensity
        )

        print(f"\n✅ 记录已保存: {record['created_at']}")

        return record


def main():
    args = sys.argv[1:]
    tracker = MoodTracker()

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    if "--add" in args:
        tracker.interactive_add()
        return

    # 获取天数参数
    days = 30
    for i, arg in enumerate(args):
        if arg == "--stats" and i + 1 < len(args):
            days = int(args[i + 1])

    # 显示今日摘要
    print("\n欢迎使用亲子互动情绪追踪系统")
    print(f"今日状态: {tracker.get_daily_summary()}\n")

    # 分析模式
    analysis = tracker.analyze_patterns(days=days)
    if "message" not in analysis:
        tracker.print_analysis(analysis)
    else:
        print(analysis["message"])

    return tracker


if __name__ == "__main__":
    main()
