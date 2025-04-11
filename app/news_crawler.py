import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import time
from typing import List, Dict, Any

def get_default_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }

def scrape_moneycontrol() -> List[Dict[str, Any]]:
    """
    Scrapes latest market news from MoneyControl
    Returns a list of dictionaries containing news articles
    """
    urls = [
        "https://www.moneycontrol.com/news/business/markets/",
        "https://www.moneycontrol.com/news/business/stocks/",
        "https://www.moneycontrol.com/news/business/markets/stock-market-updates/",
    ]
    
    news_list = []
    headers = get_default_headers()

    for base_url in urls:
        try:
            response = requests.get(base_url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all news articles
            articles = soup.find_all(['li', 'div'], class_=['clearfix', 'article-list'])
            
            for article in articles[:5]:  # Get latest 5 articles from each section
                try:
                    # Find title and link
                    title_element = article.find(['h2', 'h3']) or article.find('a')
                    if not title_element:
                        continue
                        
                    title = title_element.text.strip()
                    link = title_element.find('a')['href'] if title_element.find('a') else None
                    if not link and hasattr(title_element, 'href'):
                        link = title_element['href']
                    
                    # Skip if no title or link
                    if not title or not link:
                        continue
                    
                    # Get article timestamp
                    time_element = article.find(['span', 'time'], class_=['ago', 'date'])
                    timestamp = time_element.text.strip() if time_element else datetime.now(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Get article content
                    content = ""
                    if link:
                        try:
                            article_response = requests.get(link, headers=headers, timeout=10)
                            article_soup = BeautifulSoup(article_response.text, 'html.parser')
                            
                            # Try different content selectors
                            content_div = (
                                article_soup.find('div', class_='content_wrapper') or
                                article_soup.find('div', class_='article-content') or
                                article_soup.find('div', class_='article_content')
                            )
                            
                            if content_div:
                                paragraphs = content_div.find_all('p')
                                content = ' '.join([p.text.strip() for p in paragraphs if p.text.strip()])
                            
                            # Fallback to meta description if no content
                            if not content:
                                meta_desc = article_soup.find('meta', {'name': 'description'})
                                if meta_desc:
                                    content = meta_desc.get('content', '')
                        except Exception as e:
                            print(f"Error fetching article content: {str(e)}")
                            # Use title as fallback content
                            content = title
                    
                    # Only add if we have minimum viable content
                    if title and (content or link):
                        news_list.append({
                            'title': title,
                            'content': content or title,  # Fallback to title if no content
                            'url': link,
                            'timestamp': timestamp,
                            'source': 'MoneyControl'
                        })
                    
                    # Add delay between requests
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"Error processing article: {str(e)}")
                    continue

            # If we have enough articles, break
            if len(news_list) >= 10:
                break

        except Exception as e:
            print(f"Error scraping {base_url}: {str(e)}")
            continue

    # Return collected news or fallback content
    if not news_list:
        # Provide fallback content
        return [{
            'title': 'Market Analysis Update',
            'content': 'Analysis based on recent market trends and general financial indicators.',
            'url': 'https://www.moneycontrol.com/markets/',
            'timestamp': datetime.now(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S"),
            'source': 'System'
        }]
    
    return news_list 