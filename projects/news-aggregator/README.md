# AI + Crypto 热点聚合器

## 项目结构
```
news-aggregator/
├── src/
│   ├── fetchers/          # 各个信息源的抓取器
│   │   ├── ai/            # AI 相关源
│   │   └── crypto/        # Crypto 相关源
│   ├── storage/           # 数据存储
│   ├── generator/         # 网页生成器
│   └── scheduler.py       # 定时任务调度
├── data/                  # 抓取的数据
├── web/                   # 生成的网页
├── config/                # 配置文件
└── requirements.txt
```

## 信息源规划

### AI 热点源
1. **Twitter/X** - AI 大佬推文
2. **Reddit** - r/artificial, r/MachineLearning
3. **GitHub Trending** - AI 项目
4. **Hacker News** - AI 相关帖子
5. **Papers With Code** - 最新论文
6. **ArXiv** - AI 论文更新
7. **Product Hunt** - AI 新产品
8. **Google AI Blog**
9. **OpenAI Blog**
10. **Anthropic Blog**

### Crypto 热点源
1. **CoinMarketCap** - 市场数据
2. **CoinGecko** - 市场数据
3. **Crypto Twitter** - 大佬动态
4. **Reddit** - r/cryptocurrency, r/bitcoin
5. **DeFiLlama** - DeFi 数据
6. **The Block** - 新闻
7. **CoinDesk** - 新闻
8. **Decrypt** - 新闻
9. **链上数据** - 大额转账、聪明钱动向

## 技术栈
- Python 3.11+
- aiohttp / httpx - 异步抓取
- SQLite - 数据存储
- Jinja2 - 网页模板
- APScheduler - 定时任务
