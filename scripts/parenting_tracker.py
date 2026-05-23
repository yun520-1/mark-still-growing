#!/usr/bin/env python3
"""
父母的功课 - 父母情绪追踪器
追踪父母每日情绪状态，识别模式

用法:
    python3 scripts/parenting_tracker.py
    python3 scripts/parenting_tracker.py --view 7    # 查看最近7天
    python3 scripts/parenting_tracker.py --stats      # 统计摘要
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

DATA_FILE = Path.home() / ".hermes" / "still_growing" / "mood_log.json"
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_entries():
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_entries(entries):
    with open(DATA_FILE, 'w') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def emotion_score_to_label(score):
    """将0-10情绪分数转换为标签"""
    if score >= 8: return "平静/积极"
    elif score >= 6: return "略感压力"
    elif score >= 4: return "焦虑/烦躁"
    elif score >= 2: return "压力大"
    else: return "崩溃边缘"


def log_entry():
    """记录一条情绪日志"""
    entries = load_entries()
    today = datetime.now().strftime("%Y-%m-%d")

    # 检查今天是否已记录
    today_entries = [e for e in entries if e['date'] == today]
    if today_entries:
        print(f"\n今天({today})已有记录:")
        for e in today_entries:
            print(f"  [{e['time']}] 情绪:{e['score']}/10 ({emotion_score_to_label(e['score'])}) 触发:{e['trigger']}")
        print("\n继续添加新记录...")

    print("\n=== 父母情绪日志 ===")
    print(f"日期: {today}")

    # 情绪分数
    while True:
        try:
            score = input("情绪分数 (0-10, 0=崩溃边缘, 10=非常平静): ").strip()
            score = int(score)
            if 0 <= score <= 10:
                break
            print("请输入0-10之间的数字")
        except ValueError:
            print("请输入有效数字")

    # 触发事件
    trigger = input("触发事件 (孩子行为/工作压力/夫妻冲突/其他, 回车跳过): ").strip() or "未记录"

    # 回应方式
    response = input("你是如何回应的? (发火/沉默/深呼吸/离开现场/其他): ").strip() or "未记录"

    # 事后修复
    repair = input("事后有修复吗? (是/否/部分): ").strip() or "否"

    # 备注
    note = input("备注 (回车跳过): ").strip()

    entry = {
        "date": today,
        "time": datetime.now().strftime("%H:%M"),
        "score": score,
        "trigger": trigger,
        "response": response,
        "repair": repair,
        "note": note,
    }

    entries.append(entry)
    save_entries(entries)

    print(f"\n已记录! 情绪: {score}/10 ({emotion_score_to_label(score)})")
    return entry


def view_entries(days=7):
    """查看最近N天的记录"""
    entries = load_entries()
    if not entries:
        print("暂无记录。使用 --log 添加第一条记录。")
        return

    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    recent = [e for e in entries if e['date'] >= cutoff]
    recent.sort(key=lambda x: (x['date'], x['time']), reverse=True)

    if not recent:
        print(f"最近{days}天没有记录。")
        return

    print(f"\n=== 最近{days}天情绪记录 ({len(recent)}条) ===")
    print(f"{'日期':<12} {'时间':<6} {'分数':<4} {'状态':<10} {'触发事件':<20} {'回应':<10} {'修复'}")
    print("-" * 90)

    for e in recent:
        label = emotion_score_to_label(e['score'])
        print(f"{e['date']:<12} {e['time']:<6} {e['score']}/10  {label:<10} {e['trigger'][:18]:<20} {e['response'][:8]:<10} {e['repair']}")

    # 统计
    scores = [e['score'] for e in recent]
    avg = sum(scores) / len(scores)
    low_days = [e for e in recent if e['score'] <= 3]
    repair_yes = [e for e in recent if e['repair'] == '是']

    print(f"\n--- 统计 ---")
    print(f"平均情绪: {avg:.1f}/10")
    print(f"低压天数: {len(low_days)}/{len(recent)}")
    print(f"主动修复: {len(repair_yes)}/{len(recent)}")
    if recent:
        triggers = {}
        for e in recent:
            t = e['trigger']
            triggers[t] = triggers.get(t, 0) + 1
        top_triggers = sorted(triggers.items(), key=lambda x: x[1], reverse=True)[:3]
        if top_triggers:
            print(f"高频触发: {', '.join(f'{t}({c}次)' for t, c in top_triggers)}")


def show_stats():
    """长期统计"""
    entries = load_entries()
    if not entries:
        print("暂无记录。")
        return

    print(f"\n=== 全部记录统计 ===")
    print(f"总记录数: {len(entries)}")

    scores = [e['score'] for e in entries]
    avg = sum(scores) / len(scores)
    print(f"总体平均情绪: {avg:.1f}/10")

    # 按触发事件统计
    triggers = {}
    responses = {}
    for e in entries:
        t = e['trigger']
        r = e['response']
        triggers[t] = triggers.get(t, 0) + 1
        responses[r] = responses.get(r, 0) + 1

    print(f"\n触发事件统计:")
    for t, c in sorted(triggers.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {t}: {c}次")

    print(f"\n回应方式统计:")
    for r, c in sorted(responses.items(), key=lambda x: x[1], reverse=True):
        print(f"  {r}: {c}次")

    # 趋势：每周平均
    by_week = {}
    for e in entries:
        d = datetime.strptime(e['date'], "%Y-%m-%d")
        week = d.strftime("%Y-W%W")
        by_week.setdefault(week, []).append(e['score'])

    print(f"\n每周平均趋势:")
    for week, scores in sorted(by_week.items(), reverse=True)[:4]:
        avg_w = sum(scores) / len(scores)
        bar = "█" * int(avg_w) + "░" * (10 - int(avg_w))
        print(f"  {week}: {bar} {avg_w:.1f}/10")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    if "--view" in args:
        try:
            days = int(args[args.index("--view") + 1])
        except (IndexError, ValueError):
            days = 7
        view_entries(days)
        return

    if "--stats" in args:
        show_stats()
        return

    if "--log" in args or len(args) == 0:
        log_entry()
        return

    print(__doc__)


if __name__ == "__main__":
    main()
