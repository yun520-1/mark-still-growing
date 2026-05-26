#!/usr/bin/env python3
"""
父母的功课 - 养育评估工具
科学量表评分系统

用法:
    python3 scripts/assessment.py --stress      # 养育压力评估
    python3 scripts/assessment.py --relation  # 亲子关系评估
    python3 scripts/assessment.py --compassion # 自我慈悲评估
    python3 scripts/assessment.py --parenting  # 教养风格评估 (v0.9.55新增)
    python3 scripts/assessment.py --communication # 沟通模式评估 (v0.9.55新增)
    python3 scripts/assessment.py --all       # 全部评估
    python3 scripts/assessment.py --history   # 查看历史记录

v0.9.55升级:
    - 新增: 教养风格评估 (专制型/权威型/溺爱型/忽视型)
    - 新增: 沟通模式评估 (4负面+4正面模式检测)
    - 吸收自OpenClaw still-growing v1.0.51
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from typing import List

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


# ========================
# 教养风格评估 (v0.9.55新增)
# ========================

PARENTING_STYLE_QUESTIONNAIRE = {
    "authoritarian": {
        "name": "专制型",
        "description": "高要求、低回应型教养风格",
        "questions": [
            {"id": "a1", "text": "我认为孩子应该完全服从父母的决定"},
            {"id": "a2", "text": "我不解释为什么制定规则，孩子遵守就是了"},
            {"id": "a3", "text": "当孩子不听话时，我会用惩罚而不是沟通"},
            {"id": "a4", "text": "我认为严格管教是爱孩子的表现"},
            {"id": "a5", "text": "我不允许孩子质疑我的决定"},
        ]
    },
    "authoritative": {
        "name": "权威型",
        "description": "高要求、高回应型教养风格（最理想）",
        "questions": [
            {"id": "b1", "text": "我会解释制定规则的原因，并倾听孩子的想法"},
            {"id": "b2", "text": "我对孩子有明确的期望，但也会考虑他们的意见"},
            {"id": "b3", "text": "我会在坚定原则的同时，表达对孩子的关爱"},
            {"id": "b4", "text": "我会根据孩子的表现调整管教方式"},
            {"id": "b5", "text": "我鼓励孩子独立思考，同时设定清晰的界限"},
        ]
    },
    "permissive": {
        "name": "溺爱型",
        "description": "低要求、高回应型教养风格",
        "questions": [
            {"id": "c1", "text": "我尽量避免与孩子发生冲突"},
            {"id": "c2", "text": "我认为孩子高兴最重要，规则可以灵活"},
            {"id": "c3", "text": "我很少对孩子说'不'或设置限制"},
            {"id": "c4", "text": "我尽量满足孩子的所有要求"},
            {"id": "c5", "text": "我认为孩子会自己学会规矩"},
        ]
    },
    "neglectful": {
        "name": "忽视型",
        "description": "低要求、低回应型教养风格",
        "questions": [
            {"id": "d1", "text": "我经常忙于工作，没有时间陪伴孩子"},
            {"id": "d2", "text": "我不了解孩子在学校的情况"},
            {"id": "d3", "text": "我很少参与孩子的日常活动"},
            {"id": "d4", "text": "我对孩子的情绪不太关注"},
            {"id": "d5", "text": "我认为孩子应该自己管自己"},
        ]
    }
}


def parenting_style_assessment():
    """教养风格评估问卷（4种风格，20题）
    
    来源: OpenClaw still-growing v1.0.51 parenting_assessment.py
    整合: v0.9.55
    """
    print("\n" + "=" * 50)
    print("父母教养风格评估问卷")
    print("=" * 50)
    print("\n请根据您的真实情况，选择最符合的选项（1-5分）：")
    print("1 = 完全不符合  2 = 偶尔符合  3 = 有时符合  4 = 经常符合  5 = 完全符合\n")

    scores = {style: 0 for style in PARENTING_STYLE_QUESTIONNAIRE.keys()}

    for style_key, style_data in PARENTING_STYLE_QUESTIONNAIRE.items():
        print(f"\n【{style_data['name']}】- {style_data['description']}")

        for q in style_data['questions']:
            while True:
                try:
                    print(f"  {q['text']}")
                    score = int(input(f"  分数(1-5): "))
                    if 1 <= score <= 5:
                        scores[style_key] += score
                        break
                    else:
                        print("  请输入1-5之间的数字")
                except ValueError:
                    print("  请输入有效的数字")
        print()

    # 计算结果
    results = {}
    for style, score in scores.items():
        percentage = (score / 25) * 100
        results[style] = {
            "name": PARENTING_STYLE_QUESTIONNAIRE[style]["name"],
            "score": score,
            "percentage": round(percentage, 1)
        }

    # 确定主要风格
    dominant_style = max(scores, key=scores.get)
    results["dominant_style"] = dominant_style
    results["dominant_name"] = PARENTING_STYLE_QUESTIONNAIRE[dominant_style]["name"]

    # 建议
    recommendations = {
        "authoritarian": "建议增加与孩子的沟通，解释规则的原因，尊重孩子的想法。",
        "authoritative": "继续保持！您正在采用最理想的教养方式。",
        "permissive": "建议适当设立明确的规则和界限，帮助孩子建立规则感。",
        "neglectful": "建议增加与孩子的互动时间，关注孩子的情感需求。"
    }

    # 打印结果
    print("\n" + "=" * 50)
    print("教养风格评估结果")
    print("=" * 50)

    print("\n各风格得分：")
    for style, data in results.items():
        if style in PARENTING_STYLE_QUESTIONNAIRE:
            bar = "█" * int(data['percentage'] / 5)
            print(f"  {data['name']}: {data['score']}分 ({data['percentage']}%) {bar}")

    print(f"\n【主要风格】: {results['dominant_name']}")
    print(f"\n【建议】: {recommendations[results['dominant_style']]}")
    print("=" * 50)

    return {
        "type": "parenting_style",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "dominant_style": results["dominant_style"],
        "dominant_name": results["dominant_name"],
        "scores": scores,
        "level": results['dominant_name'],
        "advice": recommendations[results['dominant_style']]
    }


# ========================
# 沟通模式评估 (v0.9.55新增)
# ========================

COMMUNICATION_NEGATIVE_PATTERNS = {
    "criticism": {
        "name": "批评",
        "indicators": ["你总是", "你从来不", "你真", "你怎么又", "你怎么这么"],
        "severity": 3
    },
    "contempt": {
        "name": "轻蔑",
        "indicators": ["真笨", "没出息", "像谁", "无语了", "服了"],
        "severity": 4
    },
    "defensive": {
        "name": "防御",
        "indicators": ["那是因为", "我又没", "我不是说了", "那不是我的错"],
        "severity": 2
    },
    "stonewalling": {
        "name": "冷战",
        "indicators": ["随便", "嗯", "哦", "行吧", "知道了", "不说话"],
        "severity": 3
    }
}

COMMUNICATION_POSITIVE_PATTERNS = {
    "empathy": {
        "name": "共情",
        "indicators": ["我理解你的感受", "我知道你很难过", "我理解你为什么"],
        "weight": 2
    },
    "validation": {
        "name": "肯定",
        "indicators": ["你说得有道理", "我听到了", "我理解你的意思"],
        "weight": 1
    },
    "solution": {
        "name": "解决问题",
        "indicators": ["我们一起想想", "有什么办法", "你觉得怎么做好"],
        "weight": 2
    },
    "soft_start": {
        "name": "柔和开场",
        "indicators": ["我想和你聊聊", "我有个想法", "我们可以谈谈吗"],
        "weight": 1
    }
}


# ========================
# 情感分析引擎 (v0.9.55新增)
# 来源: OpenClaw core_v2.py EmotionAnalyzer
# ========================

class EmotionAnalyzer:
    """情感分析引擎 - 检测文本情感倾向和强度"""

    POSITIVE_WORDS = {"开心", "快乐", "幸福", "兴奋", "满足", "爱", "喜欢", "高兴", "愉快", "欣慰", "温暖", "感动", "自豪", "轻松"}
    NEGATIVE_WORDS = {"生气", "愤怒", "伤心", "难过", "焦虑", "恐惧", "绝望", "崩溃", "无助", "委屈", "压抑", "沉重", "紧张", "害怕", "担忧"}
    INTENSITY_MARKERS = ["非常", "极其", "完全", "彻底", "超级", "极度", "太", "好", "真的"]

    @classmethod
    def detect(cls, text: str) -> str:
        """检测情感倾向: positive / negative / neutral"""
        p = sum(1 for w in cls.POSITIVE_WORDS if w in text)
        n = sum(1 for w in cls.NEGATIVE_WORDS if w in text)
        if n > p:
            return "negative"
        elif p > n:
            return "positive"
        return "neutral"

    @classmethod
    def intensity(cls, text: str) -> int:
        """计算情感强度: 1-10"""
        base = 5
        for marker in cls.INTENSITY_MARKERS:
            if marker in text:
                base = min(10, base + 1)
        return base

    @classmethod
    def extract_emotions(cls, text: str) -> List[str]:
        """提取匹配到的情绪词"""
        matched = []
        for word in cls.POSITIVE_WORDS | cls.NEGATIVE_WORDS:
            if word in text:
                matched.append(word)
        return matched


def communication_assessment():
    """沟通模式评估 - 检测4负面+4正面模式
    
    来源: OpenClaw still-growing v1.0.51 communication_analyzer.py
    整合: v0.9.55
    """
    print("\n" + "=" * 50)
    print("亲子沟通模式评估")
    print("=" * 50)
    print("\n请输入您最近与孩子的一次对话（输入'q'结束）：\n")

    text_lines = []
    while True:
        try:
            line = input()
            if line.lower() == 'q':
                break
            text_lines.append(line)
        except EOFError:
            break

    if not text_lines:
        print("未输入内容，使用默认测试文本演示...")
        text_lines = ["孩子: 我不想上学了", "家长: 你又来这套！"]

    text = "\n".join(text_lines)
    text_lower = text.lower()

    print("\n" + "-" * 40)
    print("分析中...")
    print("-" * 40)

    # 检测模式
    negative_found = []
    positive_found = []
    total_negative = 0
    total_positive = 0

    for pattern_id, pattern in COMMUNICATION_NEGATIVE_PATTERNS.items():
        matches = [ind for ind in pattern["indicators"] if ind in text_lower]
        if matches:
            negative_found.append({
                "pattern_id": pattern_id,
                "name": pattern["name"],
                "matches": matches,
                "severity": pattern["severity"]
            })
            total_negative += pattern["severity"]

    for pattern_id, pattern in COMMUNICATION_POSITIVE_PATTERNS.items():
        matches = [ind for ind in pattern["indicators"] if ind in text]
        if matches:
            positive_found.append({
                "pattern_id": pattern_id,
                "name": pattern["name"],
                "matches": matches,
                "weight": pattern["weight"]
            })
            total_positive += pattern["weight"]

    # 情感分析 (v0.9.55新增)
    emotion_result = EmotionAnalyzer.detect(text)
    emotion_intensity = EmotionAnalyzer.intensity(text)
    detected_emotions = EmotionAnalyzer.extract_emotions(text)

    # 计算健康比例
    if total_positive > 0 or total_negative > 0:
        ratio = total_positive / (total_positive + total_negative)
        health_ratio = round(ratio * 100, 1)
    else:
        health_ratio = 50
        ratio = 0.5

    # 建议
    if ratio >= 0.8:
        recommendation = "优秀的沟通模式！继续保持"
    elif ratio >= 0.6:
        recommendation = "良好的沟通，可以继续改进"
    elif ratio >= 0.4:
        recommendation = "需要关注和改进沟通方式"
    else:
        recommendation = "建议学习非暴力沟通技巧"

    # 打印结果
    print("\n" + "=" * 50)
    print("沟通模式分析结果")
    print("=" * 50)

    print(f"\n【输入文本】:\n{text[:200]}{'...' if len(text) > 200 else ''}")

    if negative_found:
        print(f"\n检测到 {len(negative_found)} 种负面模式:")
        for p in negative_found:
            print(f"  ⚠️ {p['name']}: {', '.join(p['matches'])} (严重度: {p['severity']})")

    if positive_found:
        print(f"\n检测到 {len(positive_found)} 种正面模式:")
        for p in positive_found:
            print(f"  ✅ {p['name']}: {', '.join(p['matches'])}")

    print(f"\n沟通健康度: {health_ratio}%")
    print(f"评估: {recommendation}")

    # 情感分析结果 (v0.9.55新增)
    emotion_emoji = {"positive": "😊", "negative": "😢", "neutral": "😐"}
    print(f"\n情感分析: {emotion_emoji.get(emotion_result, '')} {emotion_result} (强度: {emotion_intensity}/10)")
    if detected_emotions:
        print(f"情绪词: {', '.join(detected_emotions)}")
    print("=" * 50)

    return {
        "type": "communication",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "negative_count": len(negative_found),
        "positive_count": len(positive_found),
        "health_ratio": health_ratio,
        "level": recommendation,
        "negative_patterns": [p["name"] for p in negative_found],
        "positive_patterns": [p["name"] for p in positive_found],
        "emotion": emotion_result,
        "emotion_intensity": emotion_intensity,
        "detected_emotions": detected_emotions
    }


# ========================
# 原有评估函数
# ========================

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
            if 'total' in r:
                pct = r['total'] / r['max'] * 100
                print(f"  {r['date']}: {r['total']}/{r['max']} ({pct:.0f}%) - {r['level']}")
            elif 'health_ratio' in r:
                print(f"  {r['date']}: 健康度{r['health_ratio']}% - {r['level']}")
            elif 'dominant_name' in r:
                print(f"  {r['date']}: {r['dominant_name']}")


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
    elif "--parenting" in args:
        result = parenting_style_assessment()
    elif "--communication" in args:
        result = communication_assessment()
    elif "--all" in args:
        results = []
        results.append(stress_assessment())
        print("\n按Enter继续亲子关系评估...")
        input()
        results.append(relation_assessment())
        print("\n按Enter继续自我慈悲评估...")
        input()
        results.append(self_compassion_check())
        print("\n按Enter继续教养风格评估...")
        input()
        results.append(parenting_style_assessment())
        print("\n按Enter继续沟通模式评估...")
        input()
        results.append(communication_assessment())

        # 汇总
        print("\n" + "=" * 50)
        print("五维度综合评估摘要")
        print("=" * 50)
        for r in results:
            if 'total' in r:
                pct = r['total'] / r['max'] * 100
                print(f"  {r['type']}: {r['total']}/{r['max']} ({pct:.0f}%) - {r['level']}")
            elif 'health_ratio' in r:
                print(f"  {r['type']}: 健康度{r['health_ratio']}% - {r['level']}")
            elif 'dominant_name' in r:
                print(f"  {r['type']}: {r['dominant_name']}")
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
