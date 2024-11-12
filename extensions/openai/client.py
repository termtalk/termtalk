'''
This module is responsible for sending messages to the OpenAI API.
'''
import sys
from openai import OpenAI

def send_message(api_key, message, model="gpt-4"):
    '''
    Send a message to the OpenAI API
    '''
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
        )
        return response
    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        sys.exit(1)
