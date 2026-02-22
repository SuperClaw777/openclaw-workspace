import asyncio
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import aiohttp
import feedparser
from bs4 import BeautifulSoup

class DataStore:
    """SQLite 数据存储"""
    
    def __init__(self, db_path: str = "data/news.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_db()
    
    def init_db(self):
        """初始化数据库"""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS ai_news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    source TEXT NOT NULL,
                    url TEXT,
                    summary TEXT,
                    published_at TIMESTAMP,
                    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    category TEXT,
                    metadata TEXT
                );
                
                CREATE TABLE IF NOT EXISTS crypto_news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    source TEXT NOT NULL,
                    url TEXT,
                    summary TEXT,
                    published_at TIMESTAMP,
                    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    category TEXT,
                    metadata TEXT
                );
                
                CREATE INDEX IF NOT EXISTS idx_ai_time ON ai_news(fetched_at);
                CREATE INDEX IF NOT EXISTS idx_crypto_time ON crypto_news(fetched_at);
            ''')
    
    def save_ai_news(self, items: List[Dict[str, Any]]):
        """保存 AI 新闻"""
        with sqlite3.connect(self.db_path) as conn:
            for item in items:
                conn.execute('''
                    INSERT OR IGNORE INTO ai_news 
                    (title, source, url, summary, published_at, category, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item.get('title'),
                    item.get('source'),
                    item.get('url'),
                    item.get('summary'),
                    item.get('published_at'),
                    item.get('category'),
                    json.dumps(item.get('metadata', {}))
                ))
            conn.commit()
    
    def save_crypto_news(self, items: List[Dict[str, Any]]):
        """保存 Crypto 新闻"""
        with sqlite3.connect(self.db_path) as conn:
            for item in items:
                conn.execute('''
                    INSERT OR IGNORE INTO crypto_news 
                    (title, source, url, summary, published_at, category, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item.get('title'),
                    item.get('source'),
                    item.get('url'),
                    item.get('summary'),
                    item.get('published_at'),
                    item.get('category'),
                    json.dumps(item.get('metadata', {}))
                ))
            conn.commit()
    
    def get_recent_ai_news(self, hours: int = 24) -> List[Dict]:
        """获取最近的 AI 新闻"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM ai_news 
                WHERE fetched_at > datetime('now', '-{} hours')
                ORDER BY published_at DESC
            '''.format(hours))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_recent_crypto_news(self, hours: int = 24) -> List[Dict]:
        """获取最近的 Crypto 新闻"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM crypto_news 
                WHERE fetched_at > datetime('now', '-{} hours')
                ORDER BY published_at DESC
            '''.format(hours))
            return [dict(row) for row in cursor.fetchall()]
