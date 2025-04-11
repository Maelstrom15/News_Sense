from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from app.news_crawler import scrape_moneycontrol
from app.openai_client import ask_openai
from datetime import datetime
import pytz

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        
        # Prepare context from news articles
        if news_articles:
            context = "\n\n".join([
                f"Title: {article['title']}\nContent: {article['content'][:500]}..."  # Truncate long articles
                for article in news_articles[:5]  # Use top 5 articles
            ])
        else:
            # Fallback context if no articles are available
            context = f"""
Title: Market Analysis Update
Content: Analyzing current market conditions and trends. The analysis will be based on general market indicators and recent trends.
Timestamp: {datetime.now(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")}
Source: System Generated
"""
        
        # Get analysis from OpenAI
        analysis = ask_openai(question, context)
        
        if not analysis:
            return {
                "status": "error",
                "message": "Unable to generate analysis at this time."
            }
        
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
            ] if news_articles else []
        }
        
    except Exception as e:
        print(f"API Error: {str(e)}")  # Log the error
        return {
            "status": "error",
            "message": "An error occurred while processing your request. Please try again.",
            "analysis": "I apologize, but I'm having trouble analyzing the market data right now. Please try asking your question again."
        }