from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
import sqlite3, os, datetime, logging, hashlib

load_dotenv()

DB_PATH = os.getenv('DB_PATH')
LOG_PATH = os.getenv('LOG_PATH')

def log(msg):
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(LOG_PATH, maxBytes=1024, backupCount=5)
    logger.addHandler(handler)
    
    logger.info(f"[{str(datetime.datetime.now())}] {msg}")

def auth(username, password):
    passwd = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM Users WHERE Username = ? AND Password = ?', (username, passwd))
    results = c.fetchall()
    c.close()
    conn.close()
    if results:
        log(f'{username} logged in')
        return True
    else:
        log(f'{username} failed logged in')
        return False

def create_note(note, username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO Notes(Author, Date, Note) VALUES(?, ?, ?)', (username, str(datetime.datetime.now()), note))
    conn.commit()
    c.close()
    conn.close()
    log(f'Creating Note - ({username}, {note})')
    return True

def delete_note(noteid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT username, note FROM Notes WHERE id = ?', (noteid))
    note = c.fetchone()
    c.execute('DELETE FROM Notes WHERE id = ?', (noteid))
    conn.commit()
    c.close()
    conn.commit()
    log(f'Removing Note - ({note[0]} {note[1]})')
    return True

def get_notes():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM Notes')
    results = c.fetchall()
    c.close()
    conn.close()
    if results:
        return results
    else:
        return []

def init():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    q = ['CREATE TABLE IF NOT EXISTS Users(id INTEGER PRIMARY KEY, Username TEXT, Password TEXT)', 'CREATE TABLE IF NOT EXISTS Notes(id INTEGER PRIMARY KEY, Author TEXT, Date TEXT, Note TEXT)']
    for i in q: c.execute(i)
    conn.commit()
    c.close()
    conn.close()