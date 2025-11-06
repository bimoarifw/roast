import os
import httpx
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY")
POLLINATIONS_API_URL = "https://text.pollinations.ai/openai"

celery_app = Celery(
    "roast_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task(rate_limit="1/s", name="roast_tasks.generate_roast")
def generate_roast(name: str) -> str:
    """
    Celery task to generate a roast by calling the Pollinations AI API.
    This task is rate-limited to 1 request per second.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {POLLINATIONS_API_KEY}"
    }

    with open('prompt.txt', 'r') as f:
        content = f.read().strip()
    system_message = {"role": "system", "content": content}
    messages = [
        system_message,
        {"role": "user", "content": f"Roast the name '{name}'."}
    ]
    payload = {
        "model": "evil",
        "messages": messages,
        "temperature": 1.0,
        "max_tokens": 100
    }

    try:
        with httpx.Client(timeout=40.0) as client:
            response = client.post(
                POLLINATIONS_API_URL,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            
            data = response.json()
            roast_text = data['choices'][0]['message']['content']
            return roast_text.strip()

    except httpx.HTTPStatusError as e:
        return f"Error: Failed to get a roast from Pollinations AI. Status: {e.response.status_code}. Response: {e.response.text}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"