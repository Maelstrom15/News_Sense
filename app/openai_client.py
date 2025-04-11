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
        prompt = f"""You are a financial expert and market analyst in 2025. Analyze the latest news and provide a forward-looking, data-focused response about {question}

Context from recent news:
{context}

Requirements for your response:
1. Format EXACTLY as shown below with all sections
2. MUST include specific numbers, percentages, and metrics
3. Each key factor must start with a relevant metric or number
4. Include market sentiment indicators with forward projections
5. Use the LATEST date from the news context (must be in 2025)
6. Each section must be separated by a blank line
7. Focus on future implications and trends

Your response MUST follow this EXACT format:

Article Date:
[Use LATEST date from news context, must be in 2025. If no specific date in context, use current date in 2025]

Source:
[Source name and URL if available]

Market Sentiment:
[BULLISH/BEARISH/NEUTRAL] with [X%] confidence - Include forward-looking justification

Key Metrics:
• [Current number/percentage] → [Projected number/percentage] - [Forward-looking metric explanation]
• [Current number/percentage] → [Projected number/percentage] - [Forward-looking metric explanation]
• [Current number/percentage] → [Projected number/percentage] - [Forward-looking metric explanation]
• [Current number/percentage] → [Projected number/percentage] - [Forward-looking metric explanation]

Impact Factors:
• [Current impact] → [Projected impact by 2025] - [Factor with specific numbers]
• [Current impact] → [Projected impact by 2025] - [Factor with specific numbers]
• [Current impact] → [Projected impact by 2025] - [Factor with specific numbers]

Technical Indicators:
• [Indicator name]: [Current value] → [Projected range for 2025]
• [Indicator name]: [Current value] → [Projected range for 2025]
• [Indicator name]: [Current value] → [Projected range for 2025]

Outlook:
[Data-driven prediction with specific numbers and timeframes, focused on 2025 and beyond]"""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert financial analyst in 2025. Focus on providing forward-looking analysis with specific numbers and projections. Always use the latest available date (must be in 2025) and include future-focused metrics. Make all predictions and analysis from a 2025 perspective."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        # Ensure the response contains a 2025 date
        response_text = response.choices[0].message.content.strip()
        if "2025" not in response_text:
            # Add current date in 2025 if no date is found
            current_2025_date = datetime.now().replace(year=2025).strftime("%d-%m-2025")
            response_text = response_text.replace("Article Date:", f"Article Date:\n{current_2025_date}")

        return response_text

    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return "I apologize, but I'm having trouble analyzing the latest market data. Please try again shortly."