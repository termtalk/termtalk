'''
This module contains functions to interact with the database to save and retrieve stats data.
'''

import sqlite3
from datetime import datetime

def init_db(cursor):
    '''
    Initialize the database
    '''
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            completion_id TEXT PRIMARY KEY,
            model TEXT,
            model_called TEXT,
            created TIMESTAMP,
            system_fingerprint TEXT,
            service_tier TEXT,
            session_id TEXT,
            finish_reason TEXT,
            role TEXT,
            content TEXT,
            total_tokens INTEGER,
            prompt_tokens INTEGER,
            completion_tokens INTEGER,
            msg_id INTEGER KEY,
            user_message TEXT
        )
    ''')

def save_stats(db_path, completion_data, session_id, msg_id, user_message, model_called):
    '''
    Save the stats data to the database
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    data = (
        completion_data.id,
        completion_data.model,
        model_called,
        datetime.fromtimestamp(completion_data.created),
        completion_data.system_fingerprint,
        completion_data.service_tier,
        session_id,
        completion_data.choices[0].finish_reason,
        completion_data.choices[0].message.role,
        completion_data.choices[0].message.content,
        completion_data.usage.total_tokens,
        completion_data.usage.prompt_tokens,
        completion_data.usage.completion_tokens,
        msg_id,
        user_message
    )

    cursor.execute('''
        INSERT INTO stats (
            completion_id, model, model_called, created, system_fingerprint, service_tier,
            session_id, finish_reason, role, content,
            total_tokens, prompt_tokens, completion_tokens, msg_id, user_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)

    conn.commit()
    conn.close()

def get_all_stats(db_path):
    '''
    Get all stats from the database
    '''

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT session_id, total_tokens, prompt_tokens, completion_tokens, model, model_called FROM stats')
    completions = cursor.fetchall()

    conn.close()
    return completions

def get_stats_by_session_id(db_path, session_id):
    '''
    Get stats by session ID
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT session_id, total_tokens, prompt_tokens, completion_tokens, model, model_called FROM stats WHERE session_id = ?', (session_id,))
    completions = cursor.fetchall()

    conn.close()
    return completions

def get_stats_by_msg_id(db_path, msg_id):
    '''
    Get stats by message ID
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM stats WHERE msg_id = ?', (msg_id,))
    completions = cursor.fetchall()

    conn.close()
    return completions
