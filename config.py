import sqlite3, os, datetime

DB_FILE = f'{os.getcwd()}/info.db'
LOG_FILE = f'{os.getcwd()}/log.txt'

def log(msg):
    with open(LOG_FILE, 'a') as f:
        f.write(msg)
        f.write('\n')

def init():
    conn  =sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute('CREATE TABLE IF NOT EXISTS Notes(id INTEGER PRIMARY KEY, date TEXT, user TEXT, note TEXT)')
    conn.commit()

def id_exists(id_):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('SELECT date FROM Notes WHERE id=?', (id_,))
    results = c.fetchone()
    if results:
        return True
    else:
        return False

def note_exists(note):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('SELECT date FROM Notes WHERE note=?', (note,))
    results = c.fetchone()
    if results:
        return True
    else:
        return False

def get_data():
    conn  =sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute('SELECT * FROM Notes')
    
    results = c.fetchall()

    if results:
        return results
    else:
        return []

def add_user(date, user, note):
    if note_exists(note) == False:
        try:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()

            c.execute('INSERT INTO Notes(date, user, note) VALUES(?, ?, ?)', (date, user, note))
            conn.commit()
            return True
        except Exception as e:
            log(f'[{datetime.datetime.now()}] {e}')
            return False
    else:
        return False

def delete_user(id_):
    if id_exists(id_):

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        c.execute('DELETE FROM Notes WHERE id=?', (id_))
        conn.commit()
        return True
    else:
        return False

def edit_user(id_, date, user, note):
    if id_exists(id_):
        if date.strip() == "":
            return False
        if user.strip() == "":
            return False
        if note.strip() == "":
            return False
        else:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()

            c.execute('UPDATE Notes SET note=? WHERE id=?', (note, id_))
            conn.commit()
            return True
    else:
        return False

def search(query):
    data = []

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('SELECT * FROM Notes')
    results = c.fetchall()

    for i in results:
        if query in i:
            data.append(i)
        else:
            pass
    
    return data