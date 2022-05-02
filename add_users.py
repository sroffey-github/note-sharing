from dotenv import load_dotenv
import sqlite3, hashlib, os

load_dotenv()

DB_PATH = os.getenv('DB_PATH')

usern = input('Username >>> ')
passwd = input('Password >>> ')

passwd = hashlib.sha256(passwd.encode()).hexdigest()
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('INSERT INTO Users(Username, Password) VALUES(?, ?)', (passwd, passwd))
conn.commit()
c.close()
conn.close()

print('[i] Complete')