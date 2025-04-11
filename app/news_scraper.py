import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
import time
from typing import List, Dict
import concurrent.futures

class NewsArticle:
    def __init__(self, title: str, content: str, url: str, source: str, timestamp: str = None):
        self.title = title
        self.content = content
        self.url = url
        self.source = source
        self.timestamp = timestamp

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "content": self.content,
            "url": self.url,
            "source": self.source,
            "timestamp": self.timestamp
        }

class FinancialNewsScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def _get_moneycontrol_news(self) -> List[NewsArticle]:
        try:
            urls = [
                "https://www.moneycontrol.com/news/business/markets/",
                "https://www.moneycontrol.com/news/business/stocks/"
            ]
            articles = []
            
            for url in urls:
                response = requests.get(url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for article in soup.select("li.clearfix"):
                    try:
                        title_elem = article.find("h2")
                        if not title_elem:
                            continue
                            
                        title = title_elem.text.strip()
                        link = title_elem.find("a")["href"] if title_elem.find("a") else None
                        
                        if link:
                            # Get full article content
                            article_response = requests.get(link, headers=self.headers, timeout=10)
                            article_soup = BeautifulSoup(article_response.text, 'html.parser')
                            content_div = article_soup.find("div", {"class": "content_wrapper"})
                            content = " ".join([p.text.strip() for p in content_div.find_all("p")]) if content_div else title
                            
                            articles.append(NewsArticle(
                                title=title,
                                content=content,
                                url=link,
                                source="MoneyControl"
                            ))
                    except Exception as e:
                        print(f"Error processing MoneyControl article: {str(e)}")
                        continue
                        
            return articles
        except Exception as e:
            print(f"Error fetching MoneyControl news: {str(e)}")
            return []

    def _get_economic_times_news(self) -> List[NewsArticle]:
        try:
            # ET RSS feed for markets
            rss_url = "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms"
            feed = feedparser.parse(rss_url)
            
            articles = []
            for entry in feed.entries[:10]:  # Get top 10 articles
                try:
                    # Get full article content
                    response = requests.get(entry.link, headers=self.headers, timeout=10)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    content_div = soup.find("div", {"class": "artText"})
                    content = " ".join([p.text.strip() for p in content_div.find_all("p")]) if content_div else entry.summary
                    
                    articles.append(NewsArticle(
                        title=entry.title,
                        content=content,
                        url=entry.link,
                        source="Economic Times",
                        timestamp=entry.published
                    ))
                except Exception as e:
                    print(f"Error processing ET article: {str(e)}")
                    continue
                    
            return articles
        except Exception as e:
            print(f"Error fetching Economic Times news: {str(e)}")
            return []

    def _get_livemint_news(self) -> List[NewsArticle]:
        try:
            # Livemint RSS feed for markets
            rss_url = "https://www.livemint.com/rss/markets"
            feed = feedparser.parse(rss_url)
            
            articles = []
            for entry in feed.entries[:10]:
                try:
                    response = requests.get(entry.link, headers=self.headers, timeout=10)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    content_div = soup.find("div", {"class": "mainArea"})
                    content = " ".join([p.text.strip() for p in content_div.find_all("p")]) if content_div else entry.summary
                    
                    articles.append(NewsArticle(
                        title=entry.title,
                        content=content,
                        url=entry.link,
                        source="Livemint",
                        timestamp=entry.published
                    ))
                except Exception as e:
                    print(f"Error processing Livemint article: {str(e)}")
                    continue
                    
            return articles
        except Exception as e:
            print(f"Error fetching Livemint news: {str(e)}")
            return []

    def _get_business_standard_news(self) -> List[NewsArticle]:
        try:
            url = "https://www.business-standard.com/markets"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = []
            for article in soup.select(".article-list li"):
                try:
                    title_elem = article.find("h2")
                    if not title_elem:
                        continue
                        
                    title = title_elem.text.strip()
                    link = "https://www.business-standard.com" + title_elem.find("a")["href"] if title_elem.find("a") else None
                    
                    if link:
                        article_response = requests.get(link, headers=self.headers, timeout=10)
                        article_soup = BeautifulSoup(article_response.text, 'html.parser')
                        content_div = article_soup.find("div", {"class": "article-content"})
                        content = " ".join([p.text.strip() for p in content_div.find_all("p")]) if content_div else title
                        
                        articles.append(NewsArticle(
                            title=title,
                            content=content,
                            url=link,
                            source="Business Standard"
                        ))
                except Exception as e:
                    print(f"Error processing Business Standard article: {str(e)}")
                    continue
                    
            return articles
        except Exception as e:
            print(f"Error fetching Business Standard news: {str(e)}")
            return []

    def get_all_news(self) -> List[Dict]:
        """Fetch news from all sources concurrently"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all scraping tasks
            future_to_source = {
                executor.submit(self._get_moneycontrol_news): "MoneyControl",
                executor.submit(self._get_economic_times_news): "Economic Times",
                executor.submit(self._get_livemint_news): "Livemint",
                executor.submit(self._get_business_standard_news): "Business Standard"
            }

            all_articles = []
            for future in concurrent.futures.as_completed(future_to_source):
                source = future_to_source[future]
                try:
                    articles = future.result()
                    all_articles.extend([article.to_dict() for article in articles])
                except Exception as e:
                    print(f"Error fetching news from {source}: {str(e)}")

        # Sort articles by timestamp if available
        all_articles.sort(
            key=lambda x: datetime.strptime(x["timestamp"], "%a, %d %b %Y %H:%M:%S %z") if x["timestamp"] else datetime.now(),
            reverse=True
        )
        
        return all_articles[:15]  # Return top 15 most recent articles

def scrape_moneycontrol():
    """Legacy function for compatibility"""
    scraper = FinancialNewsScraper()
    return scraper.get_all_news()