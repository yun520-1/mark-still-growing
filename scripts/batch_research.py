#!/usr/bin/env python3
"""
父母的功课 - 20并发研究脚本
使用ThreadPoolExecutor实现20个搜索并发执行
"""
import urllib.request
import urllib.parse
import json
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

SKILL_DIR = "/Users/apple/.hermes/skills/mark-still-growing"
RESEARCH_FILE = os.path.join(SKILL_DIR, "references", "research_data.md")
VERSION_FILE = os.path.join(SKILL_DIR, "VERSION")

# 20个搜索主题（每次全部搜索）
TOPICS = [
    "mindful parenting children anxiety reduction",
    "intergenerational trauma Chinese parents 80s 90s",
    "adverse childhood experiences ACEs long-term health",
    "attachment theory children parenting styles outcomes",
    "emotion coaching children psychology Gottman",
    "parental burnout syndrome children development",
    "corporal punishment children behavioral problems",
    "children mental health trends social media",
    "intergenerational trauma transmission mechanisms",
    "positive discipline parenting effectiveness evidence",
    "parent child family therapy effectiveness",
    "adolescent rebellion parent conflict psychology",
    "child developmental needs psychology stages",
    "parental emotion regulation mindfulness",
    "domestic violence children psychological PTSD",
    "children ADHD learning disabilities support therapy",
    "anxious children cognitive behavioral therapy",
    "adolescent depression family interventions",
    "children social skills peer relationships",
    "parent child communication training effectiveness",
]

def search_openalex(query):
    """搜索OpenAlex"""
    try:
        url = f"https://api.openalex.org/works?search={urllib.parse.quote(query)}&per_page=3&select=title,publication_year,cited_by_count,doi"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
            works = data.get('results', [])
            results = []
            for w in works:
                results.append({
                    'title': w.get('title', 'N/A')[:100],
                    'year': w.get('publication_year', 'N/A'),
                    'cited_by': w.get('cited_by_count', 0),
                    'doi': w.get('doi', ''),
                })
            return query, results
    except Exception as e:
        return query, [{'error': str(e)}]

def read_version():
    with open(VERSION_FILE) as f:
        return f.read().strip()

def update_version():
    ver = read_version()
    parts = ver.split('.')
    parts[-1] = str(int(parts[-1]) + 1)
    new_ver = '.'.join(parts)
    with open(VERSION_FILE, 'w') as f:
        f.write(new_ver)
    return new_ver

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 启动20并发搜索...")
    
    results = {}
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(search_openalex, topic): topic for topic in TOPICS}
        for i, future in enumerate(as_completed(futures), 1):
            topic, papers = future.result()
            results[topic] = papers
            print(f"  [{i}/20] 完成: {topic[:50]}")
    
    # 生成内容
    content = [f"\n## 批次 - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]
    for topic, papers in results.items():
        content.append(f"\n### {topic}\n")
        for p in papers:
            if 'error' in p:
                content.append(f"- 错误: {p['error']}\n")
            else:
                content.append(f"- **{p['title']}** ({p['year']}), 引用:{p['cited_by']}\n")
    
    # 追加
    with open(RESEARCH_FILE, 'a') as f:
        f.write("".join(content))
    
    # 版本+0.0.1
    new_ver = update_version()
    print(f"完成！版本→{new_ver}")

if __name__ == "__main__":
    main()
