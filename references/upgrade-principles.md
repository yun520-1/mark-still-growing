# Still Growing - 升级原则与教训

## 升级设计原则（来自会话教训，2026-05-28）

1. **可运行代码 > 纯文本描述**：优先编写可执行工具脚本，而非仅有理论描述。GitHub搜索育儿代码仓库质量普遍较低（最高1星），自行编写工具比吸收劣质代码更有价值。

2. **统计意义优先**：需要数据时先搜索学术论文（OpenAlex API: api.openalex.org），不接受未注明来源的数字。搜索时URL-encode空格。

3. **不添加"听起来有用但无法做好"的功能**：用户明确拒绝"5分钟连接检查"（无法客观验证）——这是核心教训。

4. **版本号规则**：frontmatter version是唯一真相源，每次升级同步更新四文件（SKILL.md frontmatter / VERSION / CHANGELOG / README.md如有版本）。

## 本次升级内容（v0.8.5）

- 删除了"5分钟连接检查"章节（用户反馈：无意义、无法做好）
- 新增4个可运行Python脚本（scripts/目录）：
  - `parenting_tracker.py`：情绪追踪器（--log/--view/--stats）
  - `breathing_timer.py`：呼吸练习（--box/--calm/--478）
  - `assessment.py`：养育评估工具（--stress/--relation/--compassion/--all）
  - `reflection.py`：每日反思提示生成器（--deep/--恨/--连接等）
- 新增"可运行工具集"章节到SKILL.md
- 升级路径：v0.8.0 → v0.8.5（从.jvs/.openclaw吸收Adler/CBT/Attachment/Satir/积极养育/学术论文/评估工具）

## 技术发现

- OpenAlex API可用，是唯一可靠的学术论文搜索API
- GitHub育儿相关代码仓库质量普遍较低
- 源文件（~/.jvs/.openclaw/skills/skills/still-growing/）与目标文件（~/.hermes/skills/mark-still-growing/）并行存在，升级时从源读取增量内容
