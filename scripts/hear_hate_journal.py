#!/usr/bin/env python3
"""
Still Growing - 听见恨日记
结构化记录愤怒背后的真实感受

核心哲学：恨比爱更原始。
愤怒不是来自爱，是来自恨——恨自己小时候没有被好好对待。
看见恨，才能放下孩子的愧疚。

用法:
    python3 scripts/hear_hate_journal.py --write     # 写日记
    python3 scripts/hear_hate_journal.py --view     # 查看历史
    python3 scripts/hear_hate_journal.py --analyze   # 分析模式
    python3 scripts/hear_hate_journal.py --quick     # 快速记录(无交互)
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

DATA_FILE = Path.home() / ".hermes" / "still_growing" / "hate_journal.json"
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def load():
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save(entries):
    with open(DATA_FILE, 'w') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def label(score):
    if score <= 2: return "强烈恨"
    elif score <= 4: return "中度恨"
    elif score <= 6: return "轻度恨"
    elif score <= 8: return "烦躁"
    else: return "平静"


def write_entry():
    """交互式写日记"""
    entries = load()
    today = datetime.now().strftime("%Y-%m-%d")

    print("\n" + "=" * 50)
    print(f"听见恨日记 - {today}")
    print("=" * 50)
    print("""
记住：这里没有评判。
恨是正常的。恨意味着你在乎。
写下恨，是为了看见它，然后放下它。
""")

    # 情境
    situation = input("发生了什么情境？孩子做了什么？ ").strip()
    if not situation:
        situation = "未记录"

    # 你的反应
    reaction = input("你当时的反应是什么？发火/沉默/惩罚/冷处理？ ").strip()
    if not reaction:
        reaction = "未记录"

    # 愤怒程度
    while True:
        try:
            anger = int(input("愤怒程度 (0-10, 0=平静, 10=暴怒): ").strip())
            if 0 <= anger <= 10:
                break
        except ValueError:
            pass
        print("请输入0-10的数字")

    # 自动化思维
    auto_thought = input("那一刻你头脑里闪过的念头是什么？ ").strip()
    if not auto_thought:
        auto_thought = "未记录"

    # 恨的来源
    print("""
那个念头让你想起了什么？
是关于孩子，还是关于你自己小时候？
""")
    hate_source = input("恨的来源（回车跳过）: ").strip()
    if not hate_source:
        hate_source = "未探索"

    # 孩子的真实需求
    print("""
站在孩子的角度：
他/她真正需要的是什么？
他/她在那一刻感受到什么？
""")
    child_need = input("孩子的真实需求（回车跳过）: ").strip()
    if not child_need:
        child_need = "未探索"

    # 事后的我
    repair = input("事后你有修复吗？做了什么？ ").strip()
    if not repair:
        repair = "未修复"

    # 笔记
    note = input("其他笔记（回车跳过）: ").strip()

    entry = {
        "date": today,
        "time": datetime.now().strftime("%H:%M"),
        "situation": situation,
        "reaction": reaction,
        "anger": anger,
        "anger_label": label(anger),
        "auto_thought": auto_thought,
        "hate_source": hate_source,
        "child_need": child_need,
        "repair": repair,
        "note": note,
    }

    entries.append(entry)
    save(entries)

    print(f"\n已保存。愤怒程度: {anger}/10 ({label(anger)})")
    print("""
记住：
你今天的恨，是你小时候没有被好好对待的恨。
孩子不是恨的来源。孩子是恨的触发器。
""")
    return entry


def view_history(days=30):
    """查看历史"""
    entries = load()
    if not entries:
        print("暂无日记。使用 --write 添加。")
        return

    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    recent = [e for e in entries if e['date'] >= cutoff]
    recent.sort(key=lambda x: (x['date'], x['time']), reverse=True)

    print(f"\n=== 听见恨日记 (最近{days}天, {len(recent)}条) ===\n")

    for e in recent:
        print(f"[{e['date']} {e['time']}] 愤怒:{e['anger']}/10 ({e['anger_label']})")
        print(f"  情境: {e['situation'][:50]}")
        print(f"  反应: {e['reaction']}")
        if e['hate_source'] != '未探索':
            print(f"  恨的来源: {e['hate_source'][:60]}")
        if e['child_need'] != '未探索':
            print(f"  孩子需求: {e['child_need'][:60]}")
        print()


def analyze_patterns():
    """分析恨的模式"""
    entries = load()
    if len(entries) < 3:
        print(f"需要至少3条日记才能分析。当前: {len(entries)}条")
        return

    # 统计
    anger_avg = sum(e['anger'] for e in entries) / len(entries)
    anger_trend = [e['anger'] for e in sorted(entries, key=lambda x: x['date'])]

    # 高愤怒触发
    high_anger = [e for e in entries if e['anger'] >= 7]

    # 反应分布
    reactions = {}
    for e in entries:
        r = e['reaction']
        reactions[r] = reactions.get(r, 0) + 1

    # 恨的来源
    hate_sources = {}
    for e in entries:
        h = e['hate_source']
        if h and h != '未探索':
            hate_sources[h] = hate_sources.get(h, 0) + 1

    # 修复率
    repair_count = sum(1 for e in entries if e['repair'] and e['repair'] != '未修复')

    print("\n" + "=" * 50)
    print("恨的模式分析")
    print("=" * 50)
    print(f"总记录: {len(entries)}条")
    print(f"平均愤怒: {anger_avg:.1f}/10")
    print(f"高愤怒(≥7)次数: {len(high_anger)}/{len(entries)}")

    print(f"\n修复率: {repair_count}/{len(entries)} ({repair_count/len(entries)*100:.0f}%)")

    print(f"\n反应方式分布:")
    for r, c in sorted(reactions.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * c
        print(f"  {r}: {bar} ({c}次)")

    if hate_sources:
        print(f"\n恨的来源 (已探索的):")
        for h, c in sorted(hate_sources.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {h} ({c}次)")

    # 最近趋势
    if len(anger_trend) >= 3:
        recent = anger_trend[-3:]
        print(f"\n最近3次愤怒值: {' → '.join(str(x) for x in recent)}")
        if recent[-1] < anger_avg:
            print("趋势: ↓ 低于平均，在进步")
        elif recent[-1] > anger_avg:
            print("趋势: ↑ 高于平均，需关注")
        else:
            print("趋势: → 稳定")

    print("\n" + "=" * 50)


def quick_entry():
    """快速记录（命令行参数，无交互）"""
    # 解析参数
    args = sys.argv[2:] if len(sys.argv) > 2 else []

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "situation": " ".join(args) if args else "快速记录",
        "reaction": "快速",
        "anger": 5,
        "anger_label": "轻度恨",
        "auto_thought": "快速",
        "hate_source": "未探索",
        "child_need": "未探索",
        "repair": "未",
        "note": "",
    }

    entries = load()
    entries.append(entry)
    save(entries)
    print(f"快速记录已保存 (愤怒:{entry['anger']}/10)")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
    elif "--write" in args:
        write_entry()
    elif "--view" in args:
        days = 30
        if "--view" in args:
            try:
                idx = args.index("--view") + 1
                days = int(args[idx])
            except (IndexError, ValueError):
                pass
        view_history(days)
    elif "--analyze" in args or "--stats" in args:
        analyze_patterns()
    elif "--quick" in args:
        quick_entry()
    elif len(args) == 0:
        write_entry()
    else:
        print(__doc__)


if __name__ == "__main__":
    from datetime import timedelta
    main()
