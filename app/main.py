from fastapi import FastAPI, Query
from app.news_crawler import scrape_moneycontrol
from app.openai_client import ask_openai

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Market Analysis API"}

@app.get("/analyze")
async def analyze_market(
    question: str = Query(..., description="Your question about the market (e.g., 'Why is Nifty down today?')")
):
    try:
        # Fetch latest news
        news_articles = scrape_moneycontrol()
        
        if not news_articles:
            return {
                "status": "error",
                "message": "Unable to fetch news articles at the moment."
            }
        
        # Prepare context from news articles
        context = "\n\n".join([
            f"Title: {article['title']}\nContent: {article['content'][:500]}..."  # Truncate long articles
            for article in news_articles[:5]  # Use top 5 articles
        ])
        
        # Get analysis from OpenAI
        analysis = ask_openai(question, context)
        
        return {
            "status": "success",
            "question": question,
            "analysis": analysis,
            "sources": [
                {
                    "title": article["title"],
                    "url": article["url"],
                    "timestamp": article["timestamp"]
                }
                for article in news_articles[:5]
            ]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }
