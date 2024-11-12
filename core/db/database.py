'''
This module is responsible for creating the database and initializing the tables.
'''

import sqlite3
import os
import uuid
from datetime import datetime
from core.db.messages import init_db as init_db_messages
from core.db.conversations import init_db as init_db_conversations
from core.db.stats import init_db as init_db_stats


def init_db(db_directory='data', db_filename='termtalk.db'):
    '''
    Initialize the database
    '''
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)
    db_path = os.path.join(db_directory, db_filename)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    init_db_messages(cursor)
    init_db_conversations(cursor)
    init_db_stats(cursor)

    conn.commit()
    conn.close()
    return db_path
