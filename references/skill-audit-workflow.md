# 技能审计与 Git 同步工作流

## 核心原则

**写完代码 ≠ 完成审计。必须验证实际状态，不假设。**

---

## 标准审计序列（每次升级/合并后必须执行）

### 第 1 步：文件结构检查
```python
import os
skill_path = "/path/to/skill"
for root, dirs, files in os.walk(skill_path):
    for f in files:
        fp = os.path.join(root, f)
        size = os.path.getsize(fp)
        rel = fp.replace(skill_path + "/", "")
        print(f"{size:>8} {rel}")
```

### 第 2 步：Frontmatter 审计
- 读取 SKILL.md 前 50 行
- 验证 `name`, `version`, `description`, `triggers` 存在
- 检查 version 与 VERSION 文件一致

### 第 3 步：重复内容检测
- 搜索重复的二级标题（如 `## 场景对话` 出现两次）
- 找近似重复段落（MD5 窗口法，窗口=5行）

### 第 4 步：红线合规检查
- `content.count('听见恨')` 应为 0（或其他红词）
- 检查所有红词是否仅出现在"规则解释表格"中，不在正文叙述中

### 第 5 步：Python 脚本语法检查
```bash
python3 -m py_compile scripts/*.py
```

### 第 6 步：Git 验证（关键！必须实际检查）
```bash
git status --short   # 看实际变更了什么
git log -1 --oneline  # 确认最后一次提交
```

---

## 本次教训

### 教训 1：rm 命令未验证
**错误**：
```python
# ❌ 错误做法：假设 rm 成功了
subprocess.run(["git", "rm", "-r", "--cached", "scripts/__pycache__"], ...)
shutil.rmtree("/path/to/delete")  # 没检查返回值
```

**正确做法**：
```python
# ✅ 验证目标确实存在，然后删除
if os.path.exists(target):
    shutil.rmtree(target)
    # 删除后立即验证
    if not os.path.exists(target):
        print("✅ 删除成功")
    else:
        print("❌ 删除失败")
```

### 教训 2：merge 后未验证内容
**错误**：
```python
# ❌ 错误做法：假设合并成功了
content = read_file(target)
# 修改了 content
write_file(target, content)
# 没验证写入的内容是否真的包含预期章节
```

**正确做法**：
```python
# ✅ 合并后立即验证
content = read_file(target)
safety_markers = ['危机信号', '四级信任度', '专业性自检']
for m in safety_markers:
    found = m in content
    print(f"  {m}: {'✅' if found else '❌'}")
```

### 教训 3：未区分"文件存在"和"内容正确"
- `os.path.exists()` 只检查路径是否存在
- `content.count('关键词')` 才能验证内容是否真的在里面
- **两者都需要检查**

---

## 常见问题与修复

### .pyc 文件在 git 里
```bash
# 从 git 移除（保留本地）
git rm -r --cached scripts/__pycache__
# 删除本地
find . -type d -name __pycache__ -exec rm -rf {} +
# 确认
git status --short
```

### 重复二级标题（复制粘贴错误）
```python
# 修复两个连续的相同标题
content = content.replace(
    "## 标题\n## 标题",  # 中间只有换行符
    "## 标题",
    1  # 只替换第一个
)
```

### 红线词汇未清理干净
```python
# 搜索所有违规词出现位置
for m in re.finditer(r'听见恨', content):
    snippet = content[max(0,m.start()-50):m.start()+50]
    print(f"@ {m.start()}: ...{snippet}...")

# 批量替换
content = content.replace("听见恨", "听见防御信号")
```

---

## Git 同步检查清单

- [ ] `git add -A` 后 `git status --short` 确认变更内容
- [ ] commit message 描述清楚做了什么
- [ ] push 后验证 remote 返回 success
- [ ] 确认 GitHub 仓库页面显示最新 commit
