#!/bin/bash
# 父母的功课 研究批次启动器
# 防止并发运行
LOCK="/tmp/fu-mu-gong-ke-research.lock"
LOG="/tmp/fu-mu-gong-ke-research.log"

if [ -f "$LOCK" ]; then
    echo "[$(date)] 已有批次在运行，退出" >> "$LOG"
    exit 0
fi

echo $$ > "$LOCK"
trap "rm -f $LOCK" EXIT

cd /Users/apple/.hermes/skills/mark-still-growing
python3 scripts/batch_research.py >> "$LOG" 2>&1
