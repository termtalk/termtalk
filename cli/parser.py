'''
Command line args parser
'''

import argparse

def get_parser():
    '''
    Get the command line arguments parser
    '''

    parser = argparse.ArgumentParser(prog='./tt', description="TermTalk")
    # parser.add_argument(
    #     "-l", "--list",
    #     action="store_true",
    #     help="List conversations"
    # )
    # parser.add_argument(
    #     "-s", "--search",
    #     type=str,
    #     help="Seach in conversations"
    # )
    # parser.add_argument(
    #     "--show",
    #     type=str,
    #     help="Show conversation"
    # )
    parser.add_argument(
        "--session-id",
        type=str,
        help="UUID for continuing an existing session"
    )
    parser.add_argument(
        "-np", "--no-prompts",
        action="store_true",
        help="Disable additional prompts"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose mode for additional output details"
    )
    parser.add_argument(
        "-nmd", "--no-markdown",
        action="store_true",
        help="Disable markdown formatting"
    )    
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="File containing the message to send to the assistant"
    )
    parser.add_argument(
        "message",
        nargs="?",
        type=str,
        help="Message to send to the assistant"
    )
    return parser
