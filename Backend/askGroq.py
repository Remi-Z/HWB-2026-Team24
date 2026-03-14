# groq_ai_utils.py
import os
from groq import Groq
from dotenv import load_dotenv

# Load API key from keys.env
load_dotenv('keys.env')
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    raise ValueError("GROQ_API_KEY not found in keys.env")

# Initialize Groq client
client = Groq(api_key=api_key)

def send_ai_message(system_prompt: str, bias: str, message_array: list) -> str:
    """
    Sends a chat request to Groq with a system prompt and message history.
    
    Args:
        system_prompt (str): The system role instructions (bias / AI behavior)
        message_array (list): List of messages with 'role' and 'content', e.g.,
            [{"role": "user", "content": "Hello"}]
    
    Returns:
        str: The AI's reply text
    """
    # Prepend system prompt to message array
    messages = [{"role": "system", "content": (system_prompt + " " + bias)}] + message_array

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages
        )
        # Extract AI reply text
        return response.choices[0].message.content

    except Exception as e:
        print("Error calling Groq API:", e)
        return ""
    
if __name__ == "__main__":
    bias = "Your bias is that you love Superman. You love nothing but superman. MAKE IT VERY OBVIOUS"
    generic_system_prompt = "You are a conversational AI that interacts with a user in a neutral and informative way. Your responses should be concise and limited to 5 sentences. Be aware that a bias may be applied, but do not include any bias from your own knowledge. Focus on answering clearly, respectfully, and helpfully."
    messages = [
        {"role": "user", "content": "Hi! Who is the coolest superhero?"}
    ]
    
    reply = send_ai_message(generic_system_prompt, bias, messages)
    print("AI Reply:\n", reply)