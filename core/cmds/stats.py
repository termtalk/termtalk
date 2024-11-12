'''
Stats commands
'''

from core.db.stats import get_all_stats as db_get_all_stats, get_stats_by_session_id as db_get_stats_by_session_id
from core.db.conversations import get_conversation_by_id as db_get_conversation_by_id, get_conversation_by_session as db_get_conversation_by_session
from core.storage import Storage

def get_all_stats():
    '''
    Get all stats from the database
    '''
    storage = Storage()
    db_path = storage.get("db_path")

    stats = db_get_all_stats(db_path)
    print_stats(stats, 'All Conversations')

def get_stats_conv(session_id):
    '''
    Get conversation statistics by session ID
    '''

    storage = Storage()
    db_path = storage.get("db_path")
    curr_session_id = storage.get("session_id")

    conv = None
    if session_id != curr_session_id:
        conv = db_get_conversation_by_session(db_path, session_id)

    stats = db_get_stats_by_session_id(db_path, session_id)

    text = None
    if session_id == curr_session_id:
        text = "Current Conversation"
    else:
        text = f"({conv[0]}) {conv[2]}"

    print_stats(stats, text)


def print_stats(stats, text=None):
    '''
    Print the conversation statistics
    '''

    # print(f"Conversation Stats for session {session_id}:")
    print("Conversation Statistics" + (f" - {text}" if text is not None else "") + ":")
    print("")

    total_messages = 0
    total_tokens = 0
    prompt_tokens = 0
    completion_tokens = 0
    model_name = None
    model_called = None


    storage = Storage()
    config = storage.get("config")

    model_price_input = config.get_model_price_input()
    model_amount_input = config.get_model_amount_input()
    model_price_output = config.get_model_price_output()
    model_amount_output = config.get_model_amount_output()

    for stat in stats:
        total_messages += 1

        total_messages += 1
        total_tokens += int(stat[1])
        prompt_tokens += int(stat[2])
        completion_tokens += int(stat[3])
        model_name = stat[4]
        model_called = stat[5]

    if total_messages == 0:
        print("No messages found in this conversation. The cost is $0.00")
        return

    print(f"            Model: {model_name} ({model_called})")
    print("")
    print(f"   Total messages: {total_messages}")
    print(f"     Total tokens: {total_tokens}")
    print(f"    Prompt tokens: {prompt_tokens}")
    print(f"Completion tokens: {completion_tokens}")
    print("")
    print(f"   Average tokens per Message: {(total_tokens / total_messages):.2f}")
    print(f"    Average tokens per Prompt: {(prompt_tokens / total_messages):.2f}")
    print(f"Average tokens per Completion: {(completion_tokens / total_messages):.2f}")
    print("")

    cost_prompt = model_price_input * prompt_tokens / model_amount_input
    cost_completion = model_price_output * completion_tokens / model_amount_output
    cost_total = cost_prompt + cost_completion

    print(f"     Total cost of Prompts: ${cost_prompt:.2f} (${cost_prompt:.7f}, {prompt_tokens} tokens)")
    print(f" Total cost of Completions: ${cost_completion:.2f} (${cost_completion:.7f}, {completion_tokens} tokens)")
    print( "                            ------------------")
    print(f"Total cost of Conversation: ${cost_total:.2f} (${cost_total:.7f}, {total_tokens} tokens)")
    print("")

def get_stats_conv_by_conv_id(conv_id):
    '''
    Get conversation statistics by conversation ID
    '''
    storage = Storage()
    db_path = storage.get("db_path")

    if conv_id.lower() in ["all", "a"]:
        get_all_stats()
        return

    session_id = None
    conv = db_get_conversation_by_id(db_path, conv_id)
    if conv is not None:
        session_id = conv[1]

    if session_id is None:
        print("No conversation selected. Please switch to a conversation.")
        return

    get_stats_conv(session_id)
