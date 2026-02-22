#!/bin/bash
# 运行新闻聚合器

cd "$(dirname "$0")"

# 激活虚拟环境（如果有）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 运行主程序
python3 run.py

# 可选：部署到 GitHub Pages 或其他服务
# cp web/index.html /var/www/html/
