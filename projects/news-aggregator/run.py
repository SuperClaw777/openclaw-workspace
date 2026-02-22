import asyncio
import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fetchers.ai_fetcher import AIFetcher
from fetchers.crypto_fetcher import CryptoFetcher
from storage.database import DataStore
from generator.web_generator import WebGenerator

async def main():
    """主程序：抓取并生成网页"""
    print("🚀 开始抓取 AI + Crypto 热点...")
    
    # 初始化组件
    db = DataStore("data/news.db")
    web_gen = WebGenerator("web")
    
    # 抓取 AI 新闻
    print("🤖 抓取 AI 热点...")
    async with AIFetcher() as ai_fetcher:
        ai_news = await ai_fetcher.fetch_all()
    
    if ai_news:
        db.save_ai_news(ai_news)
        print(f"   ✅ 保存了 {len(ai_news)} 条 AI 新闻")
    
    # 抓取 Crypto 新闻
    print("₿ 抓取 Crypto 热点...")
    crypto_fetcher = CryptoFetcher()
    crypto_news = await crypto_fetcher.fetch_all()
    
    if crypto_news:
        db.save_crypto_news(crypto_news)
        print(f"   ✅ 保存了 {len(crypto_news)} 条 Crypto 新闻")
    
    # 从数据库读取最近的新闻
    ai_recent = db.get_recent_ai_news(hours=48)
    crypto_recent = db.get_recent_crypto_news(hours=48)
    
    # 生成网页
    print("🎨 生成网页...")
    output_path = web_gen.generate(ai_recent, crypto_recent)
    print(f"   ✅ 网页已生成: {output_path}")
    
    print(f"\n📊 总计: {len(ai_recent)} 条 AI + {len(crypto_recent)} 条 Crypto")
    print("✨ 完成!")

if __name__ == "__main__":
    asyncio.run(main())
