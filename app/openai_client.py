# app/openai_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def ask_openai(question: str, context: str) -> str:
    """
    Ask OpenAI a question with context and get a response
    """
    try:
        # Create the prompt with context and question
        prompt = f"""You are a financial expert and market analyst. Analyze the latest news and market data to provide a detailed, data-driven response about {question}

Context from recent news:
{context}

Requirements for your response:
1. Focus on specific funds, ETFs, and stocks that are directly impacted
2. Include actual prices, percentages, and YTD performance where available
3. Organize information into clear sections with numerical data
4. Provide actionable insights and recommendations
5. Use exact numbers and current market data
6. Keep the analysis focused and relevant to the question

Your response MUST follow this EXACT format:

Based on your question about [topic], the following [assets/funds/sectors] are affected:

1. Directly Impacted Funds:
[List each relevant fund/ETF with the following data points]
- Fund Name (TICKER): [YTD performance]%. Current Price: $[price]
[Brief explanation of why this fund is impacted]
[Continue listing relevant funds in the same format]

2. Key Impact Metrics:
- Direct Impact: [Specific impact on prices/performance]
- Sector Exposure: [Relevant sector exposures]
- Risk Assessment: [Key risk metrics and data]

3. Actionable Insights:
- [First key insight with specific recommendation]
- [Second key insight with specific recommendation]
- [Third key insight with specific recommendation]

Would you like specific details about any of these [assets/funds]?"""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial analyst expert focused on providing accurate, data-driven analysis with specific numbers, current prices, and actionable insights. Always include actual market data and performance metrics in your responses."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        response_text = response.choices[0].message.content.strip()
        return response_text

    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return "I apologize, but I'm having trouble analyzing the market data. Please try again shortly."