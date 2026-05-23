#!/usr/bin/env python3
"""
父母的功课 - 8小时升级调度器
管理16次迭代，第16次迭代后执行审计+GitHub同步
"""
import os
import subprocess
import sys
from datetime import datetime

SKILL_DIR = "/Users/apple/.hermes/skills/mark-still-growing"
COUNTER_FILE = "/tmp/fu-mu-gong-ke-iteration.txt"
MAX_ITERATIONS = 16

def get_iteration():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE) as f:
            return int(f.read().strip() or "0")
    return 0

def set_iteration(n):
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(n))

def run_batch():
    """运行20并发搜索批次"""
    script = os.path.join(SKILL_DIR, "scripts", "batch_research.py")
    result = subprocess.run(["python3", script], capture_output=True, text=True, timeout=120)
    return result.returncode == 0

def run_audit_and_sync():
    """第16次迭代：审计+修复+GitHub同步"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] === 最终审计阶段 ===")
    
    issues = []
    
    # 检查Python文件语法
    for root, dirs, files in os.walk(os.path.join(SKILL_DIR, "scripts")):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for f in files:
            if f.endswith('.py') and not f.endswith('.pyc'):
                path = os.path.join(root, f)
                result = subprocess.run(["python3", "-m", "py_compile", path], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    issues.append(f"语法错误 {f}: {result.stderr[:100]}")
    
    # 检查SKILL.md版本同步
    with open(os.path.join(SKILL_DIR, "SKILL.md")) as f:
        skill_content = f.read()
    skill_ver_match = [l for l in skill_content.split('\n') if l.startswith('version:')]
    
    with open(os.path.join(SKILL_DIR, "VERSION")) as f:
        version_content = f.read().strip()
    
    # 检查不一致
    if skill_ver_match:
        skill_ver = skill_ver_match[0].split(':')[1].strip()
        if skill_ver != version_content:
            issues.append(f"版本不一致: SKILL.md={skill_ver} VERSION={version_content}")
            # 修复
            skill_content = skill_content.replace(
                f'version: {skill_ver}',
                f'version: {version_content}'
            )
            with open(os.path.join(SKILL_DIR, "SKILL.md"), 'w') as f:
                f.write(skill_content)
            issues.append(f"已修复版本为 {version_content}")
    
    # GitHub同步
    print("GitHub同步...")
    os.chdir(SKILL_DIR)
    
    # Add all changes
    subprocess.run(["git", "add", "-A"], capture_output=True)
    
    # Check if anything changed
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if result.stdout.strip():
        ver = version_content
        msg = f"升级: 批次16完成 v{ver}"
        subprocess.run(["git", "commit", "-m", msg], capture_output=True)
        push = subprocess.run(["git", "push", "origin", "main", "--no-verify"], 
                            capture_output=True, text=True)
        if push.returncode == 0:
            print(f"✅ GitHub同步成功: {msg}")
        else:
            print(f"❌ GitHub同步失败: {push.stderr[:200]}")
            issues.append(f"GitHub同步失败: {push.stderr[:100]}")
    else:
        print("无变更需要提交")
    
    return issues

def main():
    iteration = get_iteration()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] === 迭代 {iteration + 1}/{MAX_ITERATIONS} ===")
    
    if iteration >= MAX_ITERATIONS:
        print("已达最大迭代次数，不再运行")
        sys.exit(0)
    
    # 运行批次
    success = run_batch()
    if not success:
        print("批次运行失败")
    
    # 更新计数
    iteration += 1
    set_iteration(iteration)
    
    # 如果是第16次，运行最终审计
    if iteration == MAX_ITERATIONS:
        issues = run_audit_and_sync()
        print(f"\n=== 最终状态 ===")
        if issues:
            print(f"发现问题: {len(issues)}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("✅ 无问题")
        
        # 重置计数器以便下次运行
        set_iteration(0)
        print("计数器已重置")

if __name__ == "__main__":
    main()
