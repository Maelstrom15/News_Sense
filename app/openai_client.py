# app/openai_client.py
import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from functools import lru_cache

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def extract_price_change(text: str) -> tuple[float, str]:
    """
    Extract price change percentage and symbol from text
    """
    # Look for patterns like "down X%" or "up X%"
    down_match = re.search(r'down\s+([\d.]+)%', text, re.IGNORECASE)
    up_match = re.search(r'up\s+([\d.]+)%', text, re.IGNORECASE)
    
    # Look for symbol patterns (ETF, stock symbols)
    symbol_match = re.search(r'(?:ETF|stock)\s+([A-Z]+)', text, re.IGNORECASE)
    symbol = symbol_match.group(1) if symbol_match else "Unknown"
    
    if down_match:
        return -float(down_match.group(1)), symbol
    elif up_match:
        return float(up_match.group(1)), symbol
    return 0.0, symbol

@lru_cache(maxsize=100)  # Cache up to 100 most recent responses
def ask_openai(question: str, context: str) -> dict:
    """
    Ask OpenAI a question with context and get a response
    """
    try:
        # Create a more flexible prompt
        prompt = f"""You are a senior financial analyst with expertise in stocks, ETFs, and market trends. 
        Provide a concise, data-driven response to the following question:

        Question: {question}

        Context from recent news:
        {context}

        Guidelines for your response:
        1. FIRST analyze what type of question this is (about a stock, ETF, sector, or general market concept)
        2. For stock-specific questions:
           - Focus on that stock's performance, key metrics, and news
           - Only mention related funds if they're highly relevant
        3. For fund/ETF questions:
           - Provide current price, YTD performance, and key holdings
           - Explain sector exposures and risk factors
        4. Always include:
           - Current market data (price, change, volume)
           - Relevant timeframes (YTD, 1-month, etc.)
           - Clear, actionable insights
        5. Structure your response logically based on the question type
        6. Be concise but include all key numbers and data points

        Important: Do NOT force a rigid structure. Adapt to the question.
        If asking about a specific stock, don't list unrelated funds.
        """

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a top financial analyst who provides precise, data-rich responses tailored to each question. You adapt your style based on whether the question is about stocks, ETFs, sectors, or general concepts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,  # Lower for more factual responses
            max_tokens=800
        )

        content = response.choices[0].message.content.strip()
        percentage, symbol = extract_price_change(content)

        return {
            "content": content,
            "price_change": {
                "percentage": percentage,
                "symbol": symbol
            }
        }

    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return {
            "content": "I apologize, but I'm having trouble accessing the market data. Please try again shortly.",
            "price_change": {
                "percentage": 0.0,
                "symbol": "Unknown"
            }
        }