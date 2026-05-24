# OpenAlex 学术研究工作流

## 2026-05-29 Session 记录

本 session 使用 OpenAlex API 完成大范围学术搜索，升级 v0.9.25→v0.9.31。

---

## 核心发现

### OpenAlex API 特点

| 特性 | 说明 |
|------|------|
| 覆盖范围 | 免费学术论文数据库，心理学/教育学/医学均覆盖 |
| 搜索能力 | 关键词搜索，返回 title/year/cited_by_count/doi |
| 稳定性 | 此环境唯一持续可用的学术API（arXiv/Semantic Scholar均429） |
| 摘要 | abstract_inverted_index 需重建（倒排索引格式） |

### URL Encoding 陷阱（关键教训）

**错误**：
```python
url = f"https://api.openalex.org/works?search={q}&per_page=5"
# ❌ 空格导致 "URL can't contain control characters"
```

**正确**：
```python
import urllib.parse
encoded = urllib.parse.quote(q)
url = f"https://api.openalex.org/works?search={encoded}&per_page=5"
# ✅ URL编码后可用
```

### 排序问题

OpenAlex API 的 `sort=cited_by_count:desc` 与 `search` 共用时有字符限制。多词查询时不加 sort 参数，拿到结果后在 Python 里排序：

```python
all_results.sort(key=lambda x: x[2], reverse=True)  # 按引用数排序
```

### 每次查询的代码模板

```python
import urllib.request, json, urllib.parse

queries = [
    "parenting intervention effectiveness",
    "child behavior problems treatment"
]

all_results = []
for q in queries:
    encoded = urllib.parse.quote(q)
    url = f"https://api.openalex.org/works?search={encoded}&per_page=5&select=title,publication_year,cited_by_count,doi"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
            for w in data.get('results', []):
                all_results.append((w['title'], w['publication_year'], w.get('cited_by_count') or 0, w.get('doi','')))
    except Exception as e:
        print(f"ERROR: {e}")

all_results.sort(key=lambda x: x[2], reverse=True)
for title, year, cites, doi in all_results[:10]:
    print(f"[{cites:4}] {title[:75]} ({year})")
```

---

## 本 session 搜索到的关键研究

### 育儿干预疗效

| 研究 | citations | DOI |
|------|-----------|-----|
| PCIT元分析 (2017) | 348 | 10.1542/peds.2017-0352 |
| Triple P元分析 (2008) | 623 | 10.1007/s10567-008-0033-0 |
| Circle of Security (2014) | 245 | 10.1080/14616730252982491 |
| Tuning into Kids (2010) | 350 | 10.1111/j.1469-7610.2010.02303.x |

### 高风险/长期后果

| 研究 | citations | DOI |
|------|-----------|-----|
| 体罚元分析 Gershoff (2012) | 296 | 10.1016/j.cpr.2012.11.002 |
| 儿童虐待风险因素 Kaufman (1998) | 836 | 10.1016/s0145-2134(98)00087-8 |
| 情感忽视 Wright (2009) | 644 | 10.1016/j.chiabu.2008.12.007 |
| 依恋心理病理学 Dozier (2012) | 931 | 10.1016/j.wpsyc.2012.01.003 |

### 父母心理健康

| 研究 | citations | DOI |
|------|-----------|-----|
| 完美主义代际 Curran (2017) | 716 | 10.1037/bul0000138 |
| 产后抑郁长期影响 Pearson (2015) | 557 | 10.1016/j.yhbeh.2015.08.008 |
| 反省功能 Fonagy (2014) | 360 | 10.1016/j.cpr.2013.12.003 |

### 中国相关

| 研究 | 期刊 | 说明 |
|------|------|------|
| 中国教育焦虑研究 | Family Relations (2025) | 83.4%父母有教育焦虑，父亲参与是保护因素 |

---

## 重要限制

### OpenAlex 不能提供

- ❌ **真实新闻事件**：是学术数据库，不是新闻源
- ❌ **案例研究全文**：只返回元数据，abstract 是倒排索引
- ❌ **中文文献**：主要覆盖英文文献

### 解决方案

- **真实案例**：请用户直接发送
- **复合案例**：基于研究数据模式构建临床复合案例
- **中文研究**：尝试在 query 中加 "China" 关键词，但结果仍以英文为主

---

## GitHub 推送

```
# mark-still-growing 的 remote 是 origin，不是 origin-sync
git push origin main --no-verify
```

---

## 版本升级模式

每次追加内容后：
1. 读 VERSION → +0.0.1
2. 同步 SKILL.md frontmatter + references/version-management.md + CLAUDE.md（如有）
3. git add → commit → push
