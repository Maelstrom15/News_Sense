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
        prompt = f"""You are a financial expert and market analyst. Analyze the latest news and provide a structured analysis about {question}

Context from recent news:
{context}

Requirements for your response:
1. Format EXACTLY as shown below with all sections
2. Include specific numbers and metrics
3. Each section must be separated by a blank line
4. Focus on actionable insights

Your response MUST follow this EXACT format:

Article Date:
[Current date in DD-MM-YYYY format]

Source:
[Source name and URL if available]

Market Sentiment:
[BULLISH/BEARISH/NEUTRAL] with [X%] confidence - Include justification

Key Metrics:
• [Key metric 1] - [Explanation]
• [Key metric 2] - [Explanation]
• [Key metric 3] - [Explanation]
• [Key metric 4] - [Explanation]

Impact Factors:
• [Factor 1] - [Impact explanation with numbers]
• [Factor 2] - [Impact explanation with numbers]
• [Factor 3] - [Impact explanation with numbers]

Technical Indicators:
• [Indicator 1]: [Current value and interpretation]
• [Indicator 2]: [Current value and interpretation]
• [Indicator 3]: [Current value and interpretation]

Outlook:
[Data-driven prediction with specific numbers and timeframes]"""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert financial analyst. Focus on providing clear, data-driven analysis with specific numbers and actionable insights."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        response_text = response.choices[0].message.content.strip()
        
        # Add current date if not present
        if "Article Date:" in response_text and "DD-MM-YYYY" in response_text:
            current_date = datetime.now().strftime("%d-%m-%Y")
            response_text = response_text.replace("[Current date in DD-MM-YYYY format]", current_date)

        return response_text

    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return "I apologize, but I'm having trouble analyzing the market data. Please try again shortly."