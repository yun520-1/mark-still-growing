# OpenClaw → mark-still-growing 吸收工作流

## 适用场景
从 `~/.jvs/.openclaw/skills/skills/still-growing/` 吸收代码到 `~/.hermes/skills/mark-still-growing/`

## 标准流程

### 1. 分析阶段（可并行）
```python
# 并发分析多个模块
delegate_task([
  {"goal": "分析 core_v2.py IntentEngine"},
  {"goal": "分析 communication_analyzer.py"},
  {"goal": "对比 mark-still-growing 已有功能"}
])
```

### 2. 代码集成
- 读取 OpenClaw 源文件
- 适配 mark-still-growing 风格（中文注释、DATA_DIR 路径）
- 新功能添加到 `scripts/`
- 新类添加到 `assessment.py` 或独立文件

### 3. 版本更新（同步三处）
```bash
# VERSION 文件
echo "0.9.xx" > VERSION

# SKILL.md frontmatter
sed -i 's/version: 0.9.xx/version: 0.9.xx/' SKILL.md

# CHANGELOG.md
```

### 4. GitHub 推送
```bash
git add -A
git commit -m "v0.9.xx: 升级说明"
git push origin main
# 网络超时则重试
```

## 关键路径
- OpenClaw 源码: `~/.jvs/.openclaw/skills/skills/still-growing/scripts/`
- mark-still-growing: `~/.hermes/skills/mark-still-growing/`
- GitHub remote: `origin` (https://github.com/yun520-1/mark-still-growing)

## 已吸收模块记录
| 版本 | 模块 | 来源 |
|------|------|------|
| v0.9.55 | parenting_assessment, communication_analyzer | OpenClaw |
| v0.9.56 | EmotionAnalyzer | core_v2.py |
| v0.9.57 | IntentEngine, PatternLibrary | core_v2.py |
| v0.9.58 | goal_tracker | goal_tracker.py |

## 常见问题
- **语法错误**: `python3 -m py_compile scripts/xxx.py`
- **GitHub push 超时**: 等待10-30秒后重试
- **类型错误**: 使用 `Optional[T]` 而非 `T = None`
