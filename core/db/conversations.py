'''
This module contains functions to interact with the conversations table in the database.
'''
import sqlite3
from datetime import datetime

def init_db(cursor):
    '''
    Initialize the database
    '''
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            conv_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            title TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

def add_conversation(db_path, session_id, title):
    '''
    Add a new conversation to the database
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert a new conversation with created_at and updated_at
    cursor.execute('''
        INSERT INTO conversations (session_id, title, created_at, updated_at)
        VALUES (?, ?, ?, ?)
    ''', (session_id, title, datetime.now(), datetime.now()))

    conn.commit()
    conn.close()

def get_conversation_by_session(db_path, session_id):
    '''
    Get a conversation by session ID
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT conv_id, session_id, title, created_at, updated_at
        FROM conversations
        WHERE session_id = ?
    ''', (session_id,))
    conversation = cursor.fetchone()
    conn.close()
    return conversation

def get_conversation_by_id(db_path, conv_id):
    '''
    Get a conversation by its ID
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT conv_id, session_id, title, created_at, updated_at
        FROM conversations
        WHERE conv_id = ?
    ''', (conv_id,))
    conversation = cursor.fetchone()
    conn.close()
    return conversation

def get_all_conversations(db_path, limit=None):
    '''
    Get all conversations from the database
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = '''
        SELECT conv_id, session_id, title, created_at, updated_at
        FROM conversations
        ORDER BY updated_at DESC
    '''

    params = []
    if limit is not None:
        query += ' LIMIT ?'
        params.append(limit)

    cursor.execute(query, params)
    conversations = cursor.fetchall()
    conn.close()
    return conversations

def update_conversation_title(db_path, session_id, new_title):
    '''
    Update the title of a conversation
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE conversations
        SET title = ?, updated_at = ?
        WHERE session_id = ?
    ''', (new_title, datetime.now(), session_id))

    conn.commit()
    conn.close()

def delete_conversation(db_path, session_id):
    '''
    Delete a conversation from the database
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM conversations
        WHERE session_id = ?
    ''', (session_id,))

    conn.commit()
    conn.close()
