# 吸码工作流：从项目源码或文档库提取内容并整合进技能

> 触发条件：用户说"读取X项目，吸收代码"或"从X项目学习"。
> **也可用于：从文档库/论文章库吸收内容（如 /Users/apple/Documents/HeartFlow 的PDF集合）。**

---

## 工作流

### Step 0：判断来源优先级（用户明确指定时优先用户指定的）

| 优先级 | 来源 | 何时用 | 读取工具 |
|--------|------|--------|---------|
| **1** | **HeartFlow源码**（`~/.hermes/skills/ai/mark-heartflow-skill/src/`） | 用户说"从心虫吸收"或涉及心理/认知/情绪模式 | `find + cat`直接读.ts/.js文件 |
| 2 | 文档库（PDF/markdown） | 用户提到具体项目或文档库 | pdftotext / glob + read_file |
| 3 | Web搜索（OpenAlex等） | 需要学术研究支撑但源码无相关内容 | OpenAlex API（免费无限制） |

> **优先级原则**：当用户说"可以从X吸收"时，X就是1号优先级。心虫源码包含83个模块，涵盖具身认知、自我疗愈、盲区破解等完整模式，比搜索更快更准。

**⚠️ HeartFlow源码扫描策略（83个文件）：**
```python
# 先grep关键词定位相关模块
files = subprocess.run(['find', HF_SRC, '-name', '*.js'], capture_output=True).stdout.split()
for f in files:
    content = open(f).read()
    if keyword in content:  # 心理学关键词
        print(f)  # 定位到的文件

# 高价值模块：
# blind-spot-breaker.js  → 评估/觉察协议
# embodied-core.js         → 具身认知/按停技术
# spontaneous-restraint.js → 克制引擎/无为判断
# self-healing-rl.js      → 自愈模式
# psychology/engine.js    → 心理学引擎
```

**⚠️ 读取PDF的陷阱：**
- `pdftotext`（系统工具）优先：更快，但可能未安装
- `pdfminer`（Python库）是备用：`from pdfminer.high_level import extract_text`
- 学术论文前100行通常包含：摘要、引言、结论 → 够判断相关性
- 全文太长的用关键词搜索定位关键段：`for i, line in enumerate(lines): if 'keyword' in line.lower()`

**946个PDF的过滤策略（HeartFlow教训）：**
```python
keywords = [
    'consciousness', 'emotion', 'parenting', 'child', 'development',
    'trauma', 'mindful', 'meditat', 'memory', 'sleep', 'dream',
    'attachment', 'regulat', 'wellbeing', 'mental health',
    'psychology', 'psychological', 'stress', 'anxiety',
    'therap', 'intervention', 'infant', 'maternal', 'phenomenon'
]
# 扫描所有PDF，按关键词命中数排序
# 取前10-20个最相关的深入读取
```

**为什么过滤有效：**
- 946个PDF中，99%是AI/ML论文，只有1%与心理学/养育直接相关
- 关键词过滤能快速定位真正相关的论文
- 深入读4个相关PDF，比扫描全部946个更有价值

### Step 1：探索项目结构

```bash
ls /Users/apple/Projects/
find /path -name "*.json" | grep -i template  # agent模板
find /path -name "*.md" | grep -i convention   # 规范文档
```

**判断项目类型：**
- `agent/*.json` 或 `agenttmpl/templates/` → agent指令模板项目
- `packages/` + `apps/` → monorepo（有共享模式）
- `internal/` → 有内部包共享模式

### Step 2：识别可吸收的模式

| 项目特征 | 值得找什么 | 吸收目标 |
|---------|-----------|---------|
| agent模板项目 | `tutor.json`, `brainstormer.json` | 指令结构格式 |
| monorepo | `CLAUDE.md`, `conventions.md` | 命名规范/架构原则 |
| 产品文档 | `product-overview.md` | 文档结构/受众分层 |

### Step 3：读取最有价值的文件

```python
# agent模板：找instructions字段（不是instruction）
with open("tutor.json") as f:
    data = json.load(f)
instructions = data["instructions"]  # 模板内容
name = data["name"]  # 模板名称
```

### Step 4：判断吸收目标

**不值得吸收的：**
- 项目特定的业务逻辑
- 环境配置（.env, Docker等）

**值得吸收的：**
- 指令模板格式（role + steps + defaults + do-not）
- 文档结构（受众分层 + 单一真相源）
- 命名规范（如果足够通用）

### Step 5：整合进技能

1. SKILL.md直接嵌入 → 技能核心行为
2. references/支持文件 → 参考资料/模式库
3. 同步：version+0.0.1 → VERSION → git push

---

## Tutor格式（tutor.json）

```
You teach the user... You are NOT a wikipedia page...

Method (Feynman-inspired):
1. **Open with the smallest understandable version.**
2. **Add one concept at a time.**
3. **Anchor every abstraction to a concrete example.**
4. **Stop and check.**
5. **Name the thing they're allowed to forget.**
6. **End with the test they can give themselves.**

Defaults:
1. **Start at the user's level, not yours.**
...

Do NOT:
- dump the whole topic in one wall of text
- use "obviously", "clearly", "trivially"
...
```

**核心结构：** role定义 + 方法步骤 + 默认行为 + 禁止行为

## Brainstormer格式（brainstormer.json）

```
You generate options. Lots of them. Divergence > convergence.

Defaults:
1. **Default to 15-20 options.**
2. **Span the design space deliberately.**
3. **Label each option with its angle.** (literal), (contrarian), (metaphor)...
4. **Include one or two deliberately bad ones.**

Intake: Brief? Hard constraints? Already tried?

Output:
**Brief**: <one-line>

1. <option> — (angle)
...

Do NOT:
- collapse to 5 "best" options
- pre-rank or pre-recommend
...
```

## Writing-Critic格式

```
You critique, not rewrite. Name what's hiding, what's bloated.

Fixed scaffold:
**这句话在传递什么？**
**孩子如何接收？**
**有什么值得保留？**
**改进方向？**

Do NOT:
- rewrite the parent's words
- say "you should say..."
- attack the parent's emotion
```

---

## 本次吸收记录

| 项目 | 日期 | 吸收内容 | 目标技能 |
|------|------|---------|---------|
| HeartFlow论文章库 | 2026-05-28 | "父母的大脑"神经科学模块+"科技分心"章节+"青少年大脑"发育事实+执行功能/情绪调节研究数据 | mark-still-growing |
| HeartFlow心虫源码 | 2026-05-29 | 愤怒按停术(STOP Protocol)+BlindSpotBreaker养育反思协议+SpontaneousRestraint克制引擎 → 转化为父母可用的按停步骤和AI对话示例 | mark-still-growing |
