from datetime import datetime
from pathlib import Path
from jinja2 import Template
import json

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI + Crypto 热点聚合 | {{ update_time }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eaeaea;
            line-height: 1.6;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            text-align: center;
            padding: 40px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 30px;
        }
        h1 {
            font-size: 2.5rem;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .update-time {
            color: #888;
            font-size: 0.9rem;
        }
        .stats {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 20px;
        }
        .stat-item {
            text-align: center;
        }
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #00d4ff;
        }
        .stat-label {
            color: #888;
            font-size: 0.85rem;
        }
        .columns {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        @media (max-width: 900px) {
            .columns { grid-template-columns: 1fr; }
        }
        .column {
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .column-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .column-icon {
            font-size: 1.8rem;
        }
        .column-title {
            font-size: 1.4rem;
            font-weight: 600;
        }
        .column-count {
            margin-left: auto;
            background: rgba(0,212,255,0.2);
            color: #00d4ff;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
        }
        .news-item {
            padding: 15px;
            margin-bottom: 12px;
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            border-left: 3px solid transparent;
            transition: all 0.3s ease;
        }
        .news-item:hover {
            background: rgba(255,255,255,0.08);
            transform: translateX(5px);
        }
        .news-item.ai { border-left-color: #00d4ff; }
        .news-item.crypto { border-left-color: #f7931a; }
        .news-title {
            font-size: 1rem;
            font-weight: 500;
            margin-bottom: 8px;
            line-height: 1.5;
        }
        .news-title a {
            color: #eaeaea;
            text-decoration: none;
        }
        .news-title a:hover {
            color: #00d4ff;
        }
        .news-meta {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 0.8rem;
            color: #888;
        }
        .news-source {
            background: rgba(255,255,255,0.1);
            padding: 2px 8px;
            border-radius: 4px;
        }
        .news-summary {
            margin-top: 10px;
            font-size: 0.9rem;
            color: #aaa;
            line-height: 1.5;
        }
        .tag {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            margin-right: 5px;
        }
        .tag-hot { background: rgba(247,147,26,0.2); color: #f7931a; }
        .tag-new { background: rgba(0,212,255,0.2); color: #00d4ff; }
        footer {
            text-align: center;
            padding: 40px;
            color: #666;
            font-size: 0.85rem;
            border-top: 1px solid rgba(255,255,255,0.1);
            margin-top: 40px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 AI + Crypto 热点聚合</h1>
            <p class="update-time">最后更新: {{ update_time }}</p>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value">{{ ai_count }}</div>
                    <div class="stat-label">AI 动态</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{ crypto_count }}</div>
                    <div class="stat-label">Crypto 动态</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{ total_sources }}</div>
                    <div class="stat-label">信息源</div>
                </div>
            </div>
        </header>
        
        <div class="columns">
            <div class="column">
                <div class="column-header">
                    <span class="column-icon">🤖</span>
                    <span class="column-title">AI 热点</span>
                    <span class="column-count">{{ ai_count }}</span>
                </div>
                {% for item in ai_news %}
                <div class="news-item ai">
                    <div class="news-title">
                        <a href="{{ item.url }}" target="_blank">{{ item.title }}</a>
                    </div>
                    <div class="news-meta">
                        <span class="news-source">{{ item.source }}</span>
                        <span>{{ item.published_at[:10] }}</span>
                        {% if item.metadata and item.metadata.score %}
                        <span class="tag tag-hot">🔥 {{ item.metadata.score }}</span>
                        {% endif %}
                    </div>
                    {% if item.summary %}
                    <div class="news-summary">{{ item.summary[:150] }}...</div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
            
            <div class="column">
                <div class="column-header">
                    <span class="column-icon">₿</span>
                    <span class="column-title">Crypto 热点</span>
                    <span class="column-count">{{ crypto_count }}</span>
                </div>
                {% for item in crypto_news %}
                <div class="news-item crypto">
                    <div class="news-title">
                        <a href="{{ item.url }}" target="_blank">{{ item.title }}</a>
                    </div>
                    <div class="news-meta">
                        <span class="news-source">{{ item.source }}</span>
                        <span>{{ item.published_at[:10] if item.published_at else 'Today' }}</span>
                        {% if item.metadata and item.metadata.price_change_24h %}
                        <span class="tag {% if item.metadata.price_change_24h > 0 %}tag-hot{% else %}tag-new{% endif %}">
                            {{ "+%.2f"|format(item.metadata.price_change_24h) if item.metadata.price_change_24h > 0 else "%.2f"|format(item.metadata.price_change_24h) }}%
                        </span>
                        {% endif %}
                    </div>
                    {% if item.summary %}
                    <div class="news-summary">{{ item.summary[:150] }}...</div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </div>
        
        <footer>
            <p>Auto-generated by Kimi Claw | 每 4 小时自动更新</p>
            <p>Sources: Hacker News, ArXiv, CoinDesk, Decrypt, CoinGecko, and more...</p>
        </footer>
    </div>
</body>
</html>
'''

class WebGenerator:
    """网页生成器"""
    
    def __init__(self, output_dir: str = "web"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.template = Template(HTML_TEMPLATE)
    
    def generate(self, ai_news: list, crypto_news: list) -> str:
        """生成网页"""
        html = self.template.render(
            update_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ai_news=ai_news[:50],  # 最多显示50条
            crypto_news=crypto_news[:50],
            ai_count=len(ai_news),
            crypto_count=len(crypto_news),
            total_sources=15
        )
        
        output_path = self.output_dir / "index.html"
        output_path.write_text(html, encoding='utf-8')
        
        return str(output_path)
