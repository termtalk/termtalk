'''
This module contains the functions to parse and execute the commands entered by the user.
'''
import argparse
import os
import uuid
from core.storage import Storage
from utils.utils import is_text_file
from core.cmds.conversations import list_conversations as cmd_list_conversations, switch_conv as cmd_switch_conv
from core.cmds.messages import show_history as cmd_show_history
from core.cmds.stats import get_stats_conv as cmd_get_stats_conv, get_stats_conv_by_conv_id as cmd_get_stats_conv_by_conv_id
from core.parser import get_parser

def show_help():
    '''
    Show the help message
    '''
    print("")
    print("Help - Available Commands")
    print("=========================")
    print("")
    print("  ?, /help, /h, /?        - Display this help message")
    print("  exit, bye, quit, q, :q! - Exit the application")
    print("")
    print("Conversation Management:")
    print("")
    print("  /new, /n                - Start a new conversation")
    print("  /stats <conv_id>|all|a, /st <conv_id>|all|a ")
    print("                          - Show statistics of a specific conversation or all")
    print("                            conversations")
    print("  /history, /hst, /hist   - Display conversation history")
    print("")
    print("  /list, /l               - List all conversations")
    print("  /switch <conv_id>, /s <conv_id>")
    print("                          - Switch to a specific conversation by ID")
    print("")
    print("Attachments:")
    print("")
    print("  /file <filename>, /f <filename>")
    print("                          - Load the contents of a file")
    print("  /rmfile, /rmf           - Unload the file contents")
    print("  /ls <dir>               - List files in a specified directory")
    print("")


# def say(message):
#     '''
#     Say a message
#     '''
#     print(f"Saying: {message}")

def setfile(filename):
    '''
    Load content of the file
    '''
    storage = Storage()
    storage.set('filename', filename)

    if not os.path.exists(filename):
        print("File not found. Please provide a valid file path.")
        storage.remove('filename')
        return
    with open(filename, 'r', encoding='utf-8') as file:
        if is_text_file(filename):
            file_content = file.read()
            file_name = os.path.basename(filename)
            storage.set('filecontent', file_content)
            storage.set('filename', file_name)
            print(f"Loaded content of the file: {filename}")
        else:
            print("Invalid file format. Please provide a text file.")
            storage.remove('filename')
        return

def rmfile():
    '''
    Unload content of the file
    '''
    storage = Storage()
    storage.remove('filename')
    storage.remove('filecontent')
    print("Unloaded content of the file")

def list_conv():
    '''
    List conversations
    '''
    cmd_list_conversations()

def switch_conv(conv_id):
    '''
    Switch to a conversation by ID
    '''
    cmd_switch_conv(conv_id)

def list_files(dir = None):
    '''
    List files in the directory
    '''
    if dir is None:
        dir = os.getcwd()

    print("")
    print(f"Listing files in {dir}")
    try:
        files = os.listdir(dir)
        files.sort()
        for file in files:
            if os.path.isdir(os.path.join(dir, file)):
                print(f"{file}/")
            else:
                print(file)

    except FileNotFoundError:
        print(f"Directory {dir} not found.")
    except PermissionError:
        print(f"Permission denied to access {dir}.")
    print("")


def show_history():
    '''
    Show the history of the conversation
    '''
    cmd_show_history()

def show_stats(conv_id = None):
    '''
    Show the statistics of the conversation
    '''
    storage = Storage()
    if conv_id is None:
        session_id = storage.get("session_id")
        cmd_get_stats_conv(session_id)
    else:
        cmd_get_stats_conv_by_conv_id(conv_id)


def new_conv():
    '''
    Start a new conversation
    '''
    print("Starting a new conversation")
    storage = Storage()
    session_id = str(uuid.uuid4())
    storage.set("session_id", session_id)

def parse_command(command):
    '''
    Parse the command entered by the user and execute the appropriate function
    '''

    command = command.strip()

    if not command.startswith("/"):
        if command in ["h", "?"]:
            show_help()
            return True
        return False

    args = command.split()

    if not args:
        return False


    parser = get_parser()

    try:
        # Parse the arguments
        parsed_args = parser.parse_args(args)

        # Call the appropriate function based on the command
        if parsed_args.command in ["/help", "/h", "/?"]:
            show_help()

        elif parsed_args.command in ["/quit", "/q", "/exit"]:
            raise KeyboardInterrupt

        # elif parsed_args.command == "/say":
        #     if parsed_args.message:
        #         say(" ".join(parsed_args.message))
        #     else:
        #         print("Error: '/say' command requires a message.")

        elif parsed_args.command in ["/ls"]:
            if parsed_args.dir and len(parsed_args.dir) > 0:
                list_files(parsed_args.dir[0])
            else:
                list_files()

        elif parsed_args.command in ["/file", "/f"]:
            if parsed_args.filename and len(parsed_args.filename) > 0:
                setfile(parsed_args.filename[0])
            else:
                print("Error: '/file' command requires a filename. Use /ls <dir> to list files.")

        elif parsed_args.command in ["/rmfile", "/rmf"]:
            rmfile()

        elif parsed_args.command in ["/list", "/l"]:
            list_conv()

        elif parsed_args.command in ["/switch", "/s"]:
            if parsed_args.conv_id and len(parsed_args.conv_id) > 0:
                switch_conv(parsed_args.conv_id[0])
            else:
                print("Error: '/switch' command requires a conversation id.")

        elif parsed_args.command in ["/history", "/hst", "/hist"]:
            show_history()

        elif parsed_args.command in ["/stats", "/st"]:
            if parsed_args.conv_id and len(parsed_args.conv_id) > 0:
                show_stats(parsed_args.conv_id[0])
            else:
                show_stats()

        elif parsed_args.command in ["/new", "/n"]:
            new_conv()

        else:
            print(f"Unknown command: {args[0]}. Type /help for available commands.")
    except argparse.ArgumentError:
        # Handle unknown commands with a custom message
        print(f"Unknown command: {args[0]}. Type /help for available commands.")

    except SystemExit:
        print(f"Unknown command: {args[0]}. Type /help for available commands.")

    return True
