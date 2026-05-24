# mark-still-growing 升级工作流

## 版本规则
- 每次新增一个主题章节 → +0.0.1
- 满10次升级 → 合并推送一次 GitHub
- VERSION 是唯一真相源

## 大型 SKILL.md（>2000行）插入模式

1. 找到最后一个主要章节和 `## 可运行工具` 之间的断点
2. 用 `patch` 工具插入新内容（不要用 write_file 覆盖全文）
3. 同步三处：
   - `VERSION` 文件
   - `SKILL.md` frontmatter `version:`
   - 检查其他引用处是否需要更新

## 插入点定位
```
# 在 SKILL.md 中搜索最后一个 ## 标题（如"## 📊 科学研究支撑"）
# 找到该章节末尾的空白行
# 下一行是 ## 可运行工具
# 在空白行和 ## 可运行工具之间插入
```

## 插件注意事项
- 心虫插件名：`heartflow-memory`（连字符，非下划线）
- 路径：`~/.hermes/plugins/heartflow-memory/`
- 启用命令：`hermes plugins enable heartflow-memory`

## 五个升级方向（已计划）
1. ✅ 离婚与单亲家庭（v0.9.23）
2. ✅ 多子女家庭（v0.9.23）
3. ✅ 祖辈育儿（v0.9.23）
4. ✅ 父母脆弱时刻（v0.9.23）
5. ⬜ 扩充学术研究（2024-2025最新数据）
