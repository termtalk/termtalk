'''
Commands related to messages
'''
from datetime import datetime, timedelta
from core.db.conversations import get_all_conversations, get_conversation_by_id
from core.storage import Storage

def list_conversations():
    '''
    List all conversations
    '''

    storage = Storage()
    db_path = storage.get("db_path")
    convs = get_all_conversations(db_path)

    if not convs:
        print("No conversations found.")
        return

    display_conversations(convs)
    # print("Conversations:")

    # for conv in convs:
    #     print(f"({conv[0]}) {conv[2]}")



def display_conversations(convs):
    if not convs:
        print("No conversations found.")
        return

    print("Conversations:")

    # Define date thresholds
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    seven_days_ago = today - timedelta(days=7)
    two_weeks_ago = today - timedelta(days=14)

    # Track current year and section headers
    current_year = today.year
    last_displayed_year = None
    last_section = None

    for conv in convs:
        conv_id, session_id, title, created_at_str, updated_at_str = conv
        updated_at = datetime.fromisoformat(updated_at_str)

        # Determine the section based on the date
        if updated_at.date() == today.date():
            section = "Today"
        elif updated_at.date() == yesterday.date():
            section = "Yesterday"
        elif seven_days_ago < updated_at <= yesterday:
            section = "In last 7 days"
        elif two_weeks_ago < updated_at <= seven_days_ago:
            section = "In last 2 weeks"
        elif updated_at.year == current_year:
            section = updated_at.strftime("%B")  # e.g., "March"
        else:
            # For previous years, include the year as a header only if it changes
            if updated_at.year != last_displayed_year:
                print(f"\n{updated_at.year}")
                print("=" * len(str(updated_at.year)))  # Print underline for the year
                last_displayed_year = updated_at.year
            section = updated_at.strftime("%B")  # e.g., "March"

        # Print the section header if it is new
        if section != last_section:
            print(f"\n{section}")
            print("=" * len(section))  # Underline the section header
            last_section = section

        # Print each conversation entry under the current section
        print(f"({conv_id}) {title}")
    print("")

def switch_conv(conv_id):
    '''
    Switch to a conversation by ID
    '''

    storage = Storage()
    db_path = storage.get("db_path")

    conv = get_conversation_by_id(db_path, conv_id)
    if conv is None:
        print("Conversation not found.")
        return

    print(f"Switching to conversation {conv_id}: " + conv[2])

    storage.set("session_id", conv[1])
