'''
Config module for termtalk
'''

import configparser
from . import defaults

class ExtendedConfig(configparser.ConfigParser):
    '''
    Extended configuration class
    '''

    def __init__(self, *args, **kwargs):
        # Call the base class initializer
        super().__init__(*args, **kwargs)

    def get_file_content(self):
        '''
        Get the file content
        '''
        section="global"
        option="file_content"
        default=defaults.FILE_CONTENT
        if self.has_option(section, option):
            return self.get(section, option)
        return default

    def get_file_name(self):
        '''
        Get the file name
        '''
        section="global"
        option="file_name"
        default=defaults.FILE_NAME
        if self.has_option(section, option):
            return self.get(section, option)
        return default

    def get_stdin_data(self):
        '''
        Get the stdin data
        '''
        section="global"
        option="stdin_data"
        default=defaults.STDIN_DATA
        if self.has_option(section, option):
            return self.get(section, option)
        return default

    def get_conv_history(self):
        '''
        Get the conversation history
        '''
        section="global"
        option="conv_history"
        default=defaults.CONV_HISTORY
        if self.has_option(section, option):
            return self.get(section, option)
        return default

    def get_ai(self):
        '''
        Get the AI
        '''
        section="global"
        option="ai"
        default=defaults.AI_DEFAULT
        if self.has_option(section, option):
            return self.get(section, option)
        return default

    def get_log_level(self):
        '''
        Get the log level
        '''
        section="global"
        option="log_level"
        default="INFO"
        if self.has_option(section, option):
            return self.get(section, option).upper()
        return default

    def get_db_directory(self):
        '''
        Get the database directory
        '''
        section="global"
        option="db_directory"
        default=defaults.DB_DIRECTORY
        if self.has_option(section, option):
            return self.get(section, option)
        return default

    def get_db_filename(self):
        '''
        Get the database filename
        '''
        section="global"
        option="db_filename"
        default=defaults.DB_FILENAME
        if self.has_option(section, option):
            return self.get(section, option)
        return default


    def get_api_key(self, section="openai"):
        '''
        Get the API key
        '''
        option="api_key"
        default=None
        if self.has_option(section, option):
            return self.get(section, option)
        return default

    def get_model(self, section="openai"):
        '''
        Get the model
        '''
        option="model"
        default=defaults.OPENAI_MODEL
        if self.has_option(section, option):
            return self.get(section, option)
        return default

    def get_db_conv_limit(self, section="openai"):
        '''
        Get the database conversation limit
        '''
        option="db_conv_limit"
        default=defaults.DB_CONV_LIMIT
        if self.has_option(section, option):
            return self.getint(section, option)
        return default

    def get_model_price_input(self, section="openai", model=defaults.OPENAI_MODEL):
        '''
        Model price for input tokens
        '''
        option="model_price_input"
        default=defaults.MODEL_PRICE_INPUT
        section_name = section + ":" + model
        if self.has_option(section_name, option):
            return self.getfloat(section_name, option)
        return default

    def get_model_amount_input(self, section="openai", model=defaults.OPENAI_MODEL):
        '''
        Model amount for input tokens
        '''
        option="model_amount_input"
        default=defaults.MODEL_AMOUNT_INPUT
        section_name = section + ":" + model
        if self.has_option(section_name, option):
            return self.getint(section_name, option)
        return default

    def get_model_price_output(self, section="openai", model=defaults.OPENAI_MODEL):
        '''
        Model price for output tokens
        '''
        option="model_price_output"
        default=defaults.MODEL_PRICE_OUTPUT
        section_name = section + ":" + model
        if self.has_option(section_name, option):
            return self.getfloat(section_name, option)
        return default

    def get_model_amount_output(self, section="openai", model=defaults.OPENAI_MODEL):
        '''
        Model amount for output tokens
        '''
        option="model_amount_output"
        default=defaults.MODEL_AMOUNT_OUTPUT
        section_name = section + ":" + model
        if self.has_option(section_name, option):
            return self.getint(section_name, option)
        return default

    def list_keys_in_section(self, section):
        '''
        List the keys in a section
        '''
        if self.has_section(section):
            return self.options(section)
        return []

    def set_defaults(self, section, default_values):
        '''
        Set the default_values for a section
        '''
        if not self.has_section(section):
            self.add_section(section)
        for option, value in default_values.items():
            if not self.has_option(section, option):
                self.set(section, option, value)
