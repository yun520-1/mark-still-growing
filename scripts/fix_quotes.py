#!/usr/bin/env python3
with open('/Users/apple/.hermes/skills/mark-still-growing/scripts/education_analyzer.py', 'r', encoding='utf-8') as f:
    content = f.read()
# 替换单引号为中文书名号
content = content.replace("'我笨'", "『我笨』")
content = content.replace("'听话'", "『听话』")
content = content.replace("'好'", "『好』")
content = content.replace("'操控'", "『操控』")
content = content.replace("'变坏'", "『变坏』")
content = content.replace("'霸凌者'", "『霸凌者』")
with open('/Users/apple/.hermes/skills/mark-still-growing/scripts/education_analyzer.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
