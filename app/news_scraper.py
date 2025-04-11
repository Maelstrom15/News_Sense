import requests
from bs4 import BeautifulSoup

def scrape_moneycontrol():
    url = "https://www.moneycontrol.com/news/business/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    articles = []

    for tag in soup.select("h2"):
        title = tag.get_text()
        link = tag.find("a")['href'] if tag.find("a") else ""
        articles.append({"title": title, "url": link, "content": title})  # Dummy content

    return articles