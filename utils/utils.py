'''
This module contains utility functions that are used in the application.
'''
import uuid
import chardet

def is_valid_uuid(uuid_string):
    '''
    Check if the given string is a valid UUID
    '''
    try:
        val = uuid.UUID(uuid_string, version=4)
    except ValueError:
        return False
    return str(val) == uuid_string

def is_text_file(file_path, sample_size=1024):
    '''
    Check if the given file is a text file
    '''
    with open(file_path, 'rb') as file:
        raw_data = file.read(sample_size)
        result = chardet.detect(raw_data)
        return result['encoding'] is not None
