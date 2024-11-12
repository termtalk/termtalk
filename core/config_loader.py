import os
import configparser
from core import defaults
from core.config import ExtendedConfig

# Define paths for configuration files
# local_config_path = os.path.expanduser('~/.config/termtalk/talk.conf')
# global_config_path = '/etc/termtalk/talk.conf'
local_config_path = os.path.expanduser(defaults.LOCAL_CONFIG)
global_config_path = defaults.GLOBAL_CONFIG

config_directory = os.path.dirname(local_config_path)
db_directory = os.path.expanduser(defaults.DB_DIRECTORY)

# Define a function to create a default config file
def create_default_config(path, api_key):
    config = configparser.ConfigParser()
    config['global'] = {
        'ai': defaults.AI_DEFAULT,
        'file_content': defaults.FILE_CONTENT,
        'file_name': defaults.FILE_NAME,
        'stdin_data': defaults.STDIN_DATA,
        'conv_history': defaults.CONV_HISTORY,
        'db_directory': db_directory,
        'db_filename': defaults.DB_FILENAME,
        'log_level': 'info'
    }

    config['openai'] = {
        'api_key': api_key,
        'model': defaults.OPENAI_MODEL,
        'db_conv_limit': defaults.DB_CONV_LIMIT,
    }

    config['openai:' + defaults.OPENAI_MODEL] = {
        'model_price_input': defaults.MODEL_PRICE_INPUT,
        'model_amount_input': defaults.MODEL_AMOUNT_INPUT,
        'model_price_output': defaults.MODEL_PRICE_OUTPUT,
        'model_amount_output': defaults.MODEL_AMOUNT_OUTPUT,
    }

    # Ensure the directory exists
    os.makedirs(config_directory, exist_ok=True)

    # Write the default configuration to the specified path
    with open(path, 'w') as configfile:
        config.write(configfile)
    print(f"Configuration file created at: {path}")

# Define a function to load configuration
def load_config(verbose=False):

    config = ExtendedConfig()

    # Load a config file
    # config.read('config.ini')


    # config = configparser.ConfigParser()

    # Check if the local config file exists
    if os.path.exists(local_config_path):
        config.read(local_config_path)
        if verbose:
            print(f"Loaded configuration from {local_config_path}")
    # Check if the global config file exists
    elif os.path.exists(global_config_path):
        config.read(global_config_path)
        if verbose:
            print(f"Loaded configuration from {global_config_path}")
    else:
        # If no config file is found, prompt for API key and create config file
        print("No configuration file found.")
        api_key = input("Please enter your OpenAI API key: ").strip()

        # Validate that API key is not empty
        if not api_key:
            print("API key cannot be empty.")
            return None

        # Create the config file with default settings
        create_default_config(local_config_path, api_key)
        config.read(local_config_path)

    return config
