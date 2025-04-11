# app/openai_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def ask_openai(question: str, context: str) -> str:
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
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a top financial analyst who provides precise, data-rich responses tailored to each question. You adapt your style based on whether the question is about stocks, ETFs, sectors, or general concepts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,  # Lower for more factual responses
            max_tokens=800
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return "I apologize, but I'm having trouble accessing the market data. Please try again shortly."