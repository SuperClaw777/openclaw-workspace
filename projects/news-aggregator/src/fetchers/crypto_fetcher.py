import asyncio
import aiohttp
import feedparser
from datetime import datetime
from typing import List, Dict, Any
from bs4 import BeautifulSoup

class CryptoFetcher:
    """Crypto 热点抓取器"""
    
    SOURCES = {
        'coindesk': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
        'decrypt': 'https://decrypt.co/feed',
        'cointelegraph': 'https://cointelegraph.com/rss',
        'theblock': 'https://www.theblock.co/rss.xml',
    }
    
    def __init__(self, proxy: str = None):
        self.proxy = proxy
    
    async def fetch_rss(self, source: str, url: str) -> List[Dict[str, Any]]:
        """抓取 RSS 源"""
        items = []
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:30]:
                items.append({
                    'title': entry.get('title', ''),
                    'source': source,
                    'url': entry.get('link', ''),
                    'summary': entry.get('summary', '')[:500] if entry.get('summary') else '',
                    'category': 'crypto',
                    'published_at': entry.get('published', datetime.now().isoformat()),
                    'metadata': {
                        'tags': entry.get('tags', []),
                        'author': entry.get('author', '')
                    }
                })
        except Exception as e:
            print(f"Error fetching {source}: {e}")
        return items
    
    async def fetch_market_data(self) -> List[Dict[str, Any]]:
        """抓取市场数据（价格变动大的币种）"""
        items = []
        
        # CoinGecko API - 获取24小时涨幅最大的币
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'price_change_percentage_24h_desc',
            'per_page': '20',
            'page': '1'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, proxy=self.proxy) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        for coin in data:
                            change = coin.get('price_change_percentage_24h', 0)
                            if abs(change) > 10:  # 只保留涨跌幅超过10%的
                                items.append({
                                    'title': f"{coin['name']} ({coin['symbol'].upper()}) {change:+.2f}%",
                                    'source': 'CoinGecko',
                                    'url': f"https://www.coingecko.com/en/coins/{coin['id']}",
                                    'summary': f"Price: ${coin.get('current_price', 0):,.2f} | Market Cap: ${coin.get('market_cap', 0):,.0f}",
                                    'category': 'crypto',
                                    'published_at': datetime.now().isoformat(),
                                    'metadata': {
                                        'price_change_24h': change,
                                        'market_cap_rank': coin.get('market_cap_rank'),
                                        'volume_24h': coin.get('total_volume')
                                    }
                                })
        except Exception as e:
            print(f"Error fetching market data: {e}")
        
        return items
    
    async def fetch_fear_greed(self) -> List[Dict[str, Any]]:
        """抓取恐惧贪婪指数"""
        items = []
        url = "https://api.alternative.me/fng/"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy=self.proxy) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get('data'):
                            fg_data = data['data'][0]
                            items.append({
                                'title': f"Fear & Greed Index: {fg_data['value']} - {fg_data['value_classification']}",
                                'source': 'Alternative.me',
                                'url': 'https://alternative.me/crypto/fear-and-greed-index/',
                                'summary': f"Crypto market sentiment indicator. {fg_data['value_classification']} zone.",
                                'category': 'crypto',
                                'published_at': datetime.fromtimestamp(int(fg_data['timestamp'])).isoformat(),
                                'metadata': {
                                    'value': fg_data['value'],
                                    'classification': fg_data['value_classification']
                                }
                            })
        except Exception as e:
            print(f"Error fetching fear & greed: {e}")
        
        return items
    
    async def fetch_all(self) -> List[Dict[str, Any]]:
        """抓取所有 Crypto 源"""
        all_items = []
        
        # RSS 源
        rss_tasks = [
            self.fetch_rss('CoinDesk', self.SOURCES['coindesk']),
            self.fetch_rss('Decrypt', self.SOURCES['decrypt']),
            self.fetch_rss('Cointelegraph', self.SOURCES['cointelegraph']),
            self.fetch_rss('The Block', self.SOURCES['theblock']),
        ]
        
        # API 源
        api_tasks = [
            self.fetch_market_data(),
            self.fetch_fear_greed(),
        ]
        
        results = await asyncio.gather(*rss_tasks, *api_tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                all_items.extend(result)
        
        return all_items
