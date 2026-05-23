#!/usr/bin/env python3
"""
统一版本同步脚本
用法: python version_sync.py [new_version]
示例: python version_sync.py 0.8.9
如果不带参数，只显示当前版本
"""
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
VERSION_FILE = SKILL_DIR / "VERSION"
SKILL_MD = SKILL_DIR / "SKILL.md"
VERSION_RULE = SKILL_DIR / "VERSION_RULE.md"


def get_current_version():
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    return None


def set_version(version):
    # 计算下一个版本
    parts = version.split('.')
    next_patch = int(parts[2]) + 1
    next_version = f"{parts[0]}.{parts[1]}.{next_patch}"
    
    # 1. 更新VERSION文件（唯一真相源）
    VERSION_FILE.write_text(version + "\n")
    
    # 2. 更新SKILL.md frontmatter
    content = SKILL_MD.read_text()
    content = re.sub(
        r'^version: \S+$',
        f'version: {version}',
        content,
        flags=re.MULTILINE
    )
    SKILL_MD.write_text(content)
    
    # 3. 更新VERSION_RULE.md
    rule_content = VERSION_RULE.read_text()
    rule_content = re.sub(
        r'\*\*当前版本：v\d+\.\d+\.\d+\*\*',
        f'**当前版本：v{version}**',
        rule_content
    )
    rule_content = re.sub(
        r'\*\*下一个版本：v\d+\.\d+\.\d+\*\*',
        f'**下一个版本：v{next_version}**',
        rule_content
    )
    VERSION_RULE.write_text(rule_content)
    
    print(f"✓ 版本已更新为: {version}")
    print(f"  下一个版本: {next_version}")


def main():
    if len(sys.argv) > 1:
        new_version = sys.argv[1]
        if not re.match(r'^\d+\.\d+\.\d+$', new_version):
            print("错误: 版本格式应为 X.Y.Z (如 0.8.9)")
            sys.exit(1)
        set_version(new_version)
    else:
        current = get_current_version()
        if current:
            print(f"当前版本: {current}")
        else:
            print("未找到VERSION文件")


if __name__ == "__main__":
    main()
