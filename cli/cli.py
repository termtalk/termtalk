'''
This module is the entry point for the CLI application.
'''

import sys
import select
import os
import uuid
from rich.console import Console
from rich.markdown import Markdown
from core.db.database import init_db
from utils.utils import is_valid_uuid, is_text_file
from core.commands import parse_command
from core.call import call_model
from core.storage import Storage
from core.common import init
from cli.parser import get_parser

def start_cli():
    '''
    Start the CLI application
    '''

    parser = get_parser()
    args = parser.parse_args()

    show_prompts = not args.no_prompts
    verbose = args.verbose
    no_markdown = args.no_markdown

    storage = Storage()
    storage.set("show_prompts", show_prompts)
    storage.set("verbose", verbose)
    storage.set("no_markdown", no_markdown)


    init()


    config = storage.get("config")

    console = None
    if no_markdown is False:
        console = Console()
        storage.set("console", console)

    db_directory = config.get_db_directory()
    db_filename = config.get_db_filename()

    FILE_CONTENT = config.get_file_content()
    FILE_NAME = config.get_file_name()
    STDIN_DATA = config.get_stdin_data()

    if show_prompts:
        print("")

        print("##### ##### ####  #   # #####  ###  #     #   # ")
        print("  #   #     #   # ## ##   #   #   # #     # #   ")
        print("  #   ###   ####  # # #   #   ##### #     ##    ")
        print("  #   #     # #   #   #   #   #   # #     # #   ")
        print("  #   ##### #   # #   #   #   #   # ##### #   # ")

        print("")
        print("Welcome to TermTalk! Talk to AI from Your Terminal.")
        print("")
        print("         https://piotrkepka.com/termtalk           ")
        print("")
        print("Version: 0.1-alpha (12.11.2024) aka 'Weekend Coding Marathon'")
        print("(C) 2024 Piotr Kepka. All rights reserved.")
        print("")
        print("Type 'exit' to quit, '?' for help.")
        print("")

    if args.session_id:
        if not is_valid_uuid(args.session_id):
            print("Invalid session ID format. Please provide a valid UUID.")
            sys.exit(1)
        else:
            if show_prompts:
                print(f"Continuing session with ID: {args.session_id}")
        session_id = args.session_id
    else:
        session_id = str(uuid.uuid4())

    storage.set("session_id", session_id)


    file_content = None
    file_name = None
    stdin_data = None
    if select.select([sys.stdin], [], [], 0.0)[0]:
        stdin_data = sys.stdin.read()

    if args.file:
        if not os.path.exists(args.file):
            print("File not found. Please provide a valid file path.")
            sys.exit(1)
        with open(args.file, 'r', encoding='utf-8') as file:
            if is_text_file(args.file):
                file_content = file.read()
                file_name = os.path.basename(args.file)
            else:
                print("Invalid file format. Please provide a text file.")
                sys.exit(1)



    db_path = init_db(db_directory, db_filename)
    storage.set("db_path", db_path)


    if args.message:
        user_message = args.message

        if file_content:
            user_message = user_message + "\n\n" + FILE_NAME + ":\n\n" + file_name + "\n\n" + FILE_CONTENT + ":\n\n" + file_content
            file_content = None

        if stdin_data:
            user_message = user_message + "\n\n" + STDIN_DATA + ":\n\n" + stdin_data
            stdin_data = None

        assistant_response = call_model(user_message)
        if console is None:
            print(f"" if show_prompts else "", assistant_response, sep="")
            if show_prompts:
                print("")
        else:
            markdown = Markdown(assistant_response)
            console.print(markdown)



    else:

        while True:
            try:

                if stdin_data is None:
                    user_input = input(">>> " if show_prompts else "")
                else:
                    user_input = stdin_data
                    print(f">>> {user_input}")

                if user_input == '' and stdin_data is None:
                    continue
                if user_input.strip().lower() in {'exit', 'quit', 'q', ':q!', 'bye'}:
                    if show_prompts:
                        print("Bye.")
                    break

                if parse_command(user_input) is False:

                    if storage.isset('filename') and storage.isset('filecontent'):
                        file_content = storage.get('filecontent')
                        file_name = storage.get('filename')
                        storage.remove('filename')
                        storage.remove('filecontent')

                    if file_content:
                        user_input = user_input + "\n\n" + FILE_NAME + ":\n\n" + file_name + "\n\n" + FILE_CONTENT + ":\n\n" + file_content
                        file_content = None

                    assistant_response = call_model(user_input)
                    if console is None:
                        print("" if show_prompts else "", assistant_response, sep="")
                        if show_prompts:
                            print("")
                    else:
                        markdown = Markdown(assistant_response)
                        console.print(markdown)

                    if stdin_data:
                        if show_prompts:
                            print("\nBye.")
                        break

            except EOFError:
                if show_prompts:
                    print("\nBye.")
                break

            except KeyboardInterrupt:
                if show_prompts:
                    print("\nBye.")
                break

if __name__ == "__main__":
    start_cli()
