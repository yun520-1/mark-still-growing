# OpenClaw 代码吸收工作流

## 何时使用

当需要从 OpenClaw 版本吸收代码到 mark-still-growing 时使用本流程。

## 标准步骤

1. **读取源文件**
   ```bash
   # OpenClaw 路径
   ~/.jvs/.openclaw/skills/skills/still-growing/scripts/
   
   # mark-still-growing 目标路径
   ~/.hermes/skills/mark-still-growing/scripts/
   ```

2. **评估依赖**
   - 优先吸收**独立模块**（无外部依赖）
   - 如有依赖 `core_logic.py`，需一并复制或重构
   - education_system.py 依赖 core_logic.py → 暂不吸收

3. **创建目标文件**
   - 直接复制代码到目标目录
   - **立即运行语法检查**：`python3 -m py_compile scripts/xxx.py`

4. **版本同步**（四文件必须一致）
   - `VERSION` 文件
   - `SKILL.md` frontmatter `version:`
   - `CHANGELOG.md` 新增条目
   - Git commit message

5. **Git 推送**
   ```bash
   cd ~/.hermes/skills/mark-still-growing
   git add -A && git commit -m "vX.Y.Z: 描述" && git push origin main
   ```

## 已吸收模块清单

| 版本 | 模块 | 来源 |
|------|------|------|
| v0.9.55 | parenting_assessment + communication_analyzer | OpenClaw |
| v0.9.56 | EmotionAnalyzer | OpenClaw core_v2.py |
| v0.9.57 | IntentEngine + PatternLibrary | OpenClaw core_v2.py |
| v0.9.58 | goal_tracker.py | OpenClaw |
| v0.9.59 | education_analyzer.py | OpenClaw ai_agent_integration.py |

## 已知陷阱

### 中文引号导致 Python 语法错误

**问题**：`write_file` 保留 Unicode 字符，但当文件中包含 `"text"` 形式的_curly quotes_（中文弯引号 U+201C/U+201D）在 Python 字符串内时，解释器误将其解析为 ASCII 引号导致字符串提前终止。

**错误现象**：
```
SyntaxError: invalid syntax (line N, column X)
```

**解决方案**：
1. 替换为中文书名号 `「」`
2. 或使用单引号 `'`
3. **最佳实践**：创建文件后立即运行 `python3 -m py_compile` 验证

**示例修复**：
```python
# 错误
"logic": "标签会变成孩子的身份认同——"我笨"成为自我定义"

# 正确
"logic": "标签会变成孩子的身份认同——「我笨」成为自我定义"
```

### GitHub Push 网络超时

**现象**：推送失败 `Failed to connect to github.com port 443`

**解决**：等待几秒后重试，通常第二次成功

## 待吸收模块

- `core_logic.py` + `education_system.py`：哲学框架，依赖较多，暂缓
- `ai_agent_integration.py`：已作为 education_analyzer.py 吸收
