#!/usr/bin/env python3
"""
Still Growing - 养育评估工具
科学量表评分系统

用法:
    python3 scripts/assessment.py --stress      # 养育压力评估
    python3 scripts/assessment.py --relation  # 亲子关系评估
    python3 scripts/assessment.py --all       # 全部评估
    python3 scripts/assessment.py --history   # 查看历史记录
"""

import json
import sys
from datetime import datetime
from pathlib import Path

DATA_DIR = Path.home() / ".hermes" / "still_growing"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_history():
    f = DATA_DIR / "assessment_history.json"
    if not f.exists():
        return []
    try:
        with open(f) as fp:
            return json.load(fp)
    except (json.JSONDecodeError, IOError):
        return []


def save_history(history):
    with open(DATA_DIR / "assessment_history.json", 'w') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def stress_assessment():
    """养育压力快速筛查（5题）"""
    print("\n" + "=" * 50)
    print("养育压力快速筛查（过去一个月）")
    print("=" * 50)
    print("评分: 1=从不, 2=偶尔, 3=有时, 4=经常, 5=总是\n")

    questions = [
        "1. 育儿让我感到疲惫不堪",
        "2. 我觉得作为父母很失败",
        "3. 育儿占据了太多时间",
        "4. 我经常对孩子发脾气",
        "5. 我觉得没有人理解我",
    ]

    scores = []
    for q in questions:
        while True:
            try:
                print(f"{q}")
                score = int(input("评分(1-5): ").strip())
                if 1 <= score <= 5:
                    scores.append(score)
                    break
                print("请输入1-5")
            except ValueError:
                print("请输入数字1-5")
        print()

    total = sum(scores)
    n = len(scores)

    if total <= 10:
        level = "正常压力范围"
        advice = "你的压力在正常范围内。继续保持自我觉察。"
    elif total <= 17:
        level = "轻度压力"
        advice = "建议关注自己的情绪状态，尝试增加休息时间。"
    elif total <= 25:
        level = "中度压力"
        advice = "建议寻求支持：与伴侣沟通、朋友倾诉或心理咨询。"
    else:
        level = "高度压力"
        advice = "你的压力较大，建议优先照顾自己，考虑专业帮助。"

    print("=" * 50)
    print(f"总分: {total}/{n*5}")
    print(f"平均: {total/n:.1f}/5")
    print(f"压力等级: {level}")
    print(f"建议: {advice}")
    print("=" * 50)

    return {
        "type": "stress",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total": total,
        "max": n * 5,
        "level": level,
        "scores": scores,
    }


def relation_assessment():
    """亲子关系质量快速评估（5题）"""
    print("\n" + "=" * 50)
    print("亲子关系质量快速评估")
    print("评分: 1=从不, 2=偶尔, 3=有时, 4=经常, 5=总是\n")

    questions = [
        "1. 我能感受到孩子的情感需求",
        "2. 我能够平静地回应孩子的哭闹",
        "3. 我和孩子有愉快的共处时光",
        "4. 我能够接纳孩子的负面情绪",
        "5. 我相信孩子愿意向我敞开心扉",
    ]

    scores = []
    for q in questions:
        while True:
            try:
                print(f"{q}")
                score = int(input("评分(1-5): ").strip())
                if 1 <= score <= 5:
                    scores.append(score)
                    break
                print("请输入1-5")
            except ValueError:
                print("请输入数字1-5")
        print()

    total = sum(scores)
    n = len(scores)

    if total >= 23:
        level = "高质量亲子关系"
        advice = "你和孩子的关系很好。继续保持这种连接。"
    elif total >= 18:
        level = "中等质量"
        advice = "关系尚可，注意在压力下保持对孩子的回应质量。"
    else:
        level = "需要改善"
        advice = "建议每天安排专门的全心陪伴时间，从15分钟开始。"

    print("=" * 50)
    print(f"总分: {total}/{n*5}")
    print(f"平均: {total/n:.1f}/5")
    print(f"关系等级: {level}")
    print(f"建议: {advice}")
    print("=" * 50)

    return {
        "type": "relation",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total": total,
        "max": n * 5,
        "level": level,
        "scores": scores,
    }


def self_compassion_check():
    """自我慈悲快速评估（5题）"""
    print("\n" + "=" * 50)
    print("自我慈悲快速评估")
    print("评分: 1=完全不像我, 5=非常像我\n")

    questions = [
        "1. 我对犯错的自己能够保持耐心",
        "2. 我能够像对待朋友一样对待自己",
        "3. 我知道失败是成长的一部分",
        "4. 我能够接纳自己的不完美",
        "5. 我在疲惫时会照顾自己而不是自责",
    ]

    scores = []
    for q in questions:
        while True:
            try:
                print(f"{q}")
                score = int(input("评分(1-5): ").strip())
                if 1 <= score <= 5:
                    scores.append(score)
                    break
                print("请输入1-5")
            except ValueError:
                print("请输入数字1-5")
        print()

    total = sum(scores)
    n = len(scores)

    if total >= 23:
        level = "高度自我慈悲"
        advice = "你对自己有健康的慈悲心。这会传递给孩子。"
    elif total >= 15:
        level = "中等自我慈悲"
        advice = "你对自己有一定的接纳，但可以更慈悲地对待自己的不完美。"
    else:
        level = "缺乏自我慈悲"
        advice = "你可能对自己过于苛刻。记住：对自己慈悲，才能对孩子慈悲。"

    print("=" * 50)
    print(f"总分: {total}/{n*5}")
    print(f"平均: {total/n:.1f}/5")
    print(f"等级: {level}")
    print(f"建议: {advice}")
    print("=" * 50)

    return {
        "type": "self_compassion",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total": total,
        "max": n * 5,
        "level": level,
        "scores": scores,
    }


def show_history():
    """显示评估历史"""
    history = load_history()
    if not history:
        print("暂无历史记录。")
        return

    print("\n=== 评估历史 ===")
    by_type = {}
    for record in history:
        t = record['type']
        by_type.setdefault(t, []).append(record)

    for t, records in by_type.items():
        print(f"\n[{t}]")
        records.sort(key=lambda x: x['date'], reverse=True)
        for r in records[:5]:
            pct = r['total'] / r['max'] * 100
            print(f"  {r['date']}: {r['total']}/{r['max']} ({pct:.0f}%) - {r['level']}")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    if "--history" in args:
        show_history()
        return

    result = None
    if "--stress" in args:
        result = stress_assessment()
    elif "--relation" in args:
        result = relation_assessment()
    elif "--compassion" in args:
        result = self_compassion_check()
    elif "--all" in args:
        results = []
        results.append(stress_assessment())
        print("\n按Enter继续亲子关系评估...")
        input()
        results.append(relation_assessment())
        print("\n按Enter继续自我慈悲评估...")
        input()
        results.append(self_compassion_check())

        # 汇总
        print("\n" + "=" * 50)
        print("三维度综合评估摘要")
        print("=" * 50)
        for r in results:
            pct = r['total'] / r['max'] * 100
            print(f"  {r['type']}: {r['total']}/{r['max']} ({pct:.0f}%) - {r['level']}")
        result = results
    else:
        print(__doc__)
        return

    # 保存
    if result:
        history = load_history()
        if isinstance(result, list):
            history.extend(result)
        else:
            history.append(result)
        save_history(history)
        print(f"\n已保存到历史记录 (共{len(history)}条)")


if __name__ == "__main__":
    main()
