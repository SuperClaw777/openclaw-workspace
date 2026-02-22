import asyncio
import aiohttp
import feedparser
from datetime import datetime
from typing import List, Dict, Any
from bs4 import BeautifulSoup

class BaseFetcher:
    """基础抓取器"""
    
    def __init__(self, proxy: str = None):
        self.proxy = proxy
        self.session = None
    
    async def __aenter__(self):
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch(self, url: str) -> str:
        """获取网页内容"""
        try:
            async with self.session.get(url, proxy=self.proxy) as resp:
                if resp.status == 200:
                    return await resp.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return ""

class AIFetcher(BaseFetcher):
    """AI 热点抓取器"""
    
    SOURCES = {
        'hackernews': 'https://news.ycombinator.com/',
        'paperswithcode': 'https://paperswithcode.com/',
        'arxiv_ai': 'https://export.arxiv.org/rss/cs.AI',
        'arxiv_ml': 'https://export.arxiv.org/rss/cs.LG',
        'arxiv_cl': 'https://export.arxiv.org/rss/cs.CL',
    }
    
    async def fetch_hackernews(self) -> List[Dict[str, Any]]:
        """抓取 Hacker News AI 相关帖子"""
        items = []
        html = await self.fetch(self.SOURCES['hackernews'])
        if not html:
            return items
        
        soup = BeautifulSoup(html, 'html.parser')
        stories = soup.find_all('tr', class_='athing')
        
        for story in stories[:30]:
            try:
                title_elem = story.find('span', class_='titleline')
                if not title_elem:
                    continue
                
                link = title_elem.find('a')
                title = link.text if link else ""
                url = link.get('href') if link else ""
                
                # 只保留 AI 相关
                ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 
                              'llm', 'gpt', 'neural', 'deep learning', 'openai',
                              'anthropic', 'claude', 'gemini', 'model']
                if any(kw in title.lower() for kw in ai_keywords):
                    items.append({
                        'title': title,
                        'source': 'Hacker News',
                        'url': url if url.startswith('http') else f"https://news.ycombinator.com/{url}",
                        'category': 'ai',
                        'published_at': datetime.now().isoformat(),
                        'metadata': {'score': self._get_score(story)}
                    })
            except Exception as e:
                continue
        
        return items
    
    def _get_score(self, story) -> int:
        """获取 HN 分数"""
        try:
            score_elem = story.find_next_sibling('tr')
            if score_elem:
                score_text = score_elem.find('span', class_='score')
                if score_text:
                    return int(score_text.text.split()[0])
        except:
            pass
        return 0
    
    async def fetch_arxiv(self, category: str = 'cs.AI') -> List[Dict[str, Any]]:
        """抓取 ArXiv 论文"""
        items = []
        feed_url = f"http://export.arxiv.org/rss/{category}"
        
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:20]:
                items.append({
                    'title': entry.get('title', ''),
                    'source': f'ArXiv {category}',
                    'url': entry.get('link', ''),
                    'summary': entry.get('summary', '')[:500],
                    'category': 'ai',
                    'published_at': entry.get('published', datetime.now().isoformat()),
                    'metadata': {'authors': entry.get('authors', [])}
                })
        except Exception as e:
            print(f"Error fetching arXiv: {e}")
        
        return items
    
    async def fetch_all(self) -> List[Dict[str, Any]]:
        """抓取所有 AI 源"""
        all_items = []
        
        # 并行抓取
        tasks = [
            self.fetch_hackernews(),
            self.fetch_arxiv('cs.AI'),
            self.fetch_arxiv('cs.LG'),
            self.fetch_arxiv('cs.CL'),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                all_items.extend(result)
        
        return all_items
