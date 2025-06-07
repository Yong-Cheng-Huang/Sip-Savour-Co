#!/bin/bash

# 當任何指令返回非零的退出碼時，立即停止執行腳本
set -o errexit

echo "Building the project..."

# 1. 安裝 Python 依賴
pip install -r requirements.txt

# 2. 收集靜態檔案
# --noinput 會自動回答 'yes'
python manage.py collectstatic --noinput

# 3. 執行資料庫遷移 (非常重要的一步！)
python manage.py migrate

echo "Build finished!"