# 技能升级协议 (v0.9.22)

> 研究驱动技能升级的标准流程。每次升级版本号+0.0.1。

---

## 触发条件

当搜索到以下类型的新内容时，应启动升级流程：

1. **新研究论文**：儿童心理学、代际创伤、育儿干预相关的2025-2026年新研究
2. **新数据**：中国父母教育焦虑数据、政策变化、流行病学数据
3. **新场景对话**：实际亲子冲突案例的解决方案
4. **新技术/工具**：情绪调节技术、临床干预方法

---

## 升级流程

### 1. 版本号管理

```
VERSION 文件 → +0.0.1
SKILL.md frontmatter version → +0.0.1
CHANGELOG.md → 新增 [x.x.x] 条目
```

### 2. SKILL.md 主文献章节更新

将新研究发现写入"学术研究支撑"章节（`### 1.` `### 2.` ... 编号段落）：

```markdown
### N. 论文简称（简短）
- **论文**：*Full Title* (Journal, Year-MM-DD)
- **数据**：样本量、研究设计
- **核心发现**：
  - 要点1
  - 要点2
- **印证**：对本技能框架的具体支撑
```

### 3. CHANGELOG.md 记录

```markdown
## [x.x.x] — YYYY-MM-DD

### 变更类型
- 变更描述
```

### 4. GitHub 同步

```bash
cd ~/.hermes/skills/mark-still-growing
git add -A
git commit -m "v{x.x.x}: 变更摘要"
git push origin main
```

---

## 核心哲学保留规则

**不可修改**：
- 慈悲是体、爱是用
- "恨比爱更原始" → 临床版"防御比反应更原始"
- 觉察→接纳→暂停→选择 核心路径
- 错位诊断框架

**可扩展**：
- 新研究支撑
- 新场景对话
- 新技术工具

---

## 参考：本次 v0.9.22 变更

- 新增研究6：Unpacking Parenting Intervention (Child Abuse & Neglect, 2026-05-06)
- 新增研究7：Intergenerational transmission of mental health, first 1000 days (Nature Reviews Psychology, 2026.1.6)
- 新增研究8：儿童情感忽视循证干预 (PCIT/CPP/PRF)
- GitHub: commit 9bcdb12