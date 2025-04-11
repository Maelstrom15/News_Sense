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
        # Create the prompt with context and question
        prompt = f"""You are a financial expert and market analyst. Analyze the following news and provide a data-focused response about {question}

Context from recent news:
{context}

Requirements for your response:
1. Format EXACTLY as shown below with all sections
2. MUST include specific numbers, percentages, and metrics
3. Each key factor must start with a relevant metric or number
4. Include market sentiment indicators
5. Highlight critical dates and timelines
6. Each section must be separated by a blank line

Your response MUST follow this EXACT format:

Article Date:
[Date of the most recent article in DD-MM-YYYY format]

Source:
[Source name and URL if available]

Market Sentiment:
[BULLISH/BEARISH/NEUTRAL] with [X%] confidence

Key Metrics:
• [Specific number/percentage] - [Key metric explanation]
• [Specific number/percentage] - [Key metric explanation]
• [Specific number/percentage] - [Key metric explanation]
• [Specific number/percentage] - [Key metric explanation]

Impact Factors:
• [Quantified impact] - [Factor with specific numbers]
• [Quantified impact] - [Factor with specific numbers]
• [Quantified impact] - [Factor with specific numbers]

Technical Indicators:
• [Indicator name]: [Specific value/range]
• [Indicator name]: [Specific value/range]
• [Indicator name]: [Specific value/range]

Outlook:
[Data-driven prediction with specific numbers and timeframes]"""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert financial analyst. Focus on providing specific numbers, metrics, and quantifiable data. Always include dates, sentiment analysis, and source information. Format response exactly as requested with all sections."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return "I apologize, but I'm having trouble analyzing the market data at the moment. Please try again shortly."
