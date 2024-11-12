'''
Commands related to messages
'''

from core.db.messages import get_messages
from core.storage import Storage
from rich.markdown import Markdown


def show_history():
    '''
    Show the history of the conversation
    '''
    storage = Storage()
    db_path = storage.get("db_path")
    session_id = storage.get("session_id")

    msgs = get_messages(db_path, session_id)

    if not msgs:
        print("No messages found.")
        return

    no_markdown = storage.get("no_markdown")
    console = storage.get("console")

    for message in msgs:
        if message[2] == 'user':
            print(f">>> {message[3]}")
        else:
            if console is None:
                print(f"{message[3]}")
            else:
                markdown = Markdown(message[3])
                console.print(markdown)
        print("")
