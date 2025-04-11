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
        prompt = f"""Based on the following recent news articles, {question}

Context:
{context}

Please provide a concise and clear explanation based only on the provided news context. If the context doesn't contain relevant information, please state that."""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",  # You can change this to gpt-3.5-turbo for lower cost
            messages=[
                {"role": "system", "content": "You are a financial news analyst who provides clear, concise explanations about market movements based on news articles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return "Sorry, I encountered an error while processing your request."
