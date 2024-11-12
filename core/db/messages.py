'''
This module provides functions to interact with the SQLite database that stores messages.
'''

import sqlite3
from datetime import datetime

def init_db(cursor):
    '''
    Initialize the database
    '''
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            msg_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            ai TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

def save_message(db_path, session_id, ai, role, content):
    '''
    Save a message to the database
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (session_id, role, ai, content, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (session_id, role, ai, content, datetime.now()))
    msg_id = cursor.lastrowid  # Capture the ID of the inserted message
    conn.commit()
    conn.close()
    return msg_id

def get_messages(db_path, session_id, limit=None):
    '''
    Get messages from the database
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = '''
        SELECT msg_id, role, ai, content, timestamp
        FROM messages
        WHERE session_id = ?
    '''
    params = [session_id]
    if limit is not None:
        query += ' ORDER BY timestamp DESC'
        query += ' LIMIT ?'
        params.append(limit)
    else:
        query += ' ORDER BY timestamp ASC'

    cursor.execute(query, params)
    messages = cursor.fetchall()
    conn.close()
    return messages

def delete_messages(db_path, session_id):
    '''
    Delete messages from the database
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM messages
        WHERE session_id = ?
    ''', (session_id,))
    conn.commit()
    conn.close()
