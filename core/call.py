'''
This module is responsible for the core functionality of the application.
'''

from core.db.messages import save_message, get_messages
from core.db.conversations import add_conversation, get_conversation_by_session
from core.db.stats import save_stats
from extensions.openai.client import send_message as openai_send_message
from core.storage import Storage

def call_model(user_message):
    '''
    Call the AI model with the user message
    '''

    storage = Storage()
    db_path = storage.get("db_path")
    session_id = storage.get("session_id")
    show_prompts = storage.get("show_prompts")
    verbose = storage.get("verbose")
    config = storage.get("config")
    ai = config.get_ai()
    model = config.get_model(ai)


    db_conv_limit = config.get_db_conv_limit(ai)

    CONV_HISTORY = config.get_conv_history()


    messages = get_messages(db_path, session_id, db_conv_limit)

    if len(messages) > 0:
        conv_history = ""
        for message in messages:
            msg_id, role, ai, content, timestamp = message[:5]
            conv_history += f"{role.capitalize()}: {content}\n"

        user_message = user_message + "\n\n" + CONV_HISTORY + ":\n\n" + conv_history

    msg_id = save_message(db_path, session_id, ai, 'user', user_message)

    if verbose:
        print(f"[ INFO ] Calling AI: {ai} with model: {model}...")

    completion_data = send_msg_to_ai(config, user_message, model)
    save_stats(db_path, completion_data, session_id, msg_id, user_message, model)

    assistant_response = get_content_from_completion(completion_data)
    assistant_response.strip()

    if verbose:
        print("[ INFO ] Response received.")

    save_message(db_path, session_id, ai, 'assistant', assistant_response)

    conv = get_conversation_by_session(db_path, session_id)
    if conv is None:
        conv_msg = "Find a short title for this conversation. Keep it in the same language as the following lines.\n\n" + user_message + "\n\n" + assistant_response 

        if verbose:
            print("[ INFO ] Getting conversation title...")
            print(f"[ INFO ] Calling AI: {ai} with model: {model}...")

        completion_data = send_msg_to_ai(config, conv_msg, model)
        save_stats(db_path, completion_data, session_id, 0, conv_msg, model)

        conv_title = get_content_from_completion(completion_data)
        conv_title.strip()
        add_conversation(db_path, session_id, conv_title)

        if verbose:
            print("[ INFO ] Title received: " + conv_title)

    return assistant_response


def send_msg_to_ai(config, user_message, model):
    '''
    Send the user message to the AI
    '''

    ai = config.get_ai()

    api_key = config.get_api_key(ai)

    switcher = {
        'openai': openai_send_message
    }
    send_message = switcher.get(ai, lambda: "Invalid AI")

    response = send_message(api_key, user_message, model)

    return response

def get_content_from_completion(completion_data):
    '''
    Get the title from the completion data
    '''
    return completion_data.choices[0].message.content
