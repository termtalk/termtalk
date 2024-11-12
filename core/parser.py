'''
Core commands parser module
'''
import argparse

def get_parser():
    '''
    Get the parser for the internal commands
    '''

    parser = argparse.ArgumentParser(prog="internal command parser", add_help=False, exit_on_error=False)
    subparsers = parser.add_subparsers(dest="command")

    help_parser = subparsers.add_parser("/help", aliases=["/h", "/?"], help="Show help")

    quit_parser = subparsers.add_parser("/quit", aliases=["/q", "/exit"], help="Quit the application")

    say_parser = subparsers.add_parser("/say", help="Say a message")
    say_parser.add_argument("message", nargs=argparse.REMAINDER, help="Message to echo")

    file_parser = subparsers.add_parser("/file", aliases=["/f"], help="Load content of the file")
    file_parser.add_argument("filename", nargs=argparse.REMAINDER, help="Send content of the file")

    rmfile_parser = subparsers.add_parser("/rmfile", aliases=["/rmf"], help="Unload content of the file")

    list_parser = subparsers.add_parser("/list", aliases=["/l"], help="List conversations")

    switch_parser = subparsers.add_parser("/switch", aliases=["/s"], help="Switch to conversation")
    switch_parser.add_argument("conv_id", nargs=argparse.REMAINDER, help="Conversation id")

    ls_parser = subparsers.add_parser("/ls", help="List files")
    ls_parser.add_argument("dir", nargs=argparse.REMAINDER, help="Directory to list")

    history_parser = subparsers.add_parser("/history", aliases=["/hst", "/hist"], help="Show history")

    stats_parser = subparsers.add_parser("/stats", aliases=["/st"], help="Show stats")
    stats_parser.add_argument("conv_id", nargs=argparse.REMAINDER, help="Conversation id or 'all'")

    new_parser = subparsers.add_parser("/new", aliases=["/n"], help="New conversation")

    return parser
