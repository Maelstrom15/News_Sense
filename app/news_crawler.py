import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

def scrape_moneycontrol():
    """
    Scrapes latest market news from MoneyControl
    Returns a list of dictionaries containing news articles
    """
    base_url = "https://www.moneycontrol.com/news/business/markets/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all news articles
        articles = soup.find_all('li', class_='clearfix')
        
        news_list = []
        for article in articles[:10]:  # Get latest 10 articles
            try:
                title_element = article.find('h2')
                if not title_element:
                    continue
                    
                title = title_element.text.strip()
                link = title_element.find('a')['href'] if title_element.find('a') else None
                
                # Get article timestamp
                time_element = article.find('span', class_='ago')
                timestamp = time_element.text.strip() if time_element else None
                
                # Get article content
                if link:
                    article_response = requests.get(link, headers=headers)
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')
                    content_div = article_soup.find('div', class_='content_wrapper')
                    content = ' '.join([p.text.strip() for p in content_div.find_all('p')]) if content_div else ''
                else:
                    content = ''

                news_list.append({
                    'title': title,
                    'content': content,
                    'url': link,
                    'timestamp': timestamp,
                    'source': 'MoneyControl'
                })
                
            except Exception as e:
                print(f"Error processing article: {str(e)}")
                continue

        return news_list

    except Exception as e:
        print(f"Error scraping MoneyControl: {str(e)}")
        return [] 