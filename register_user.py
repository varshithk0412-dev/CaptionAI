import sqlite3

DB_FILE = 'users.db'

def user_exists(email) : 
    conn = sqlite3.connect(DB_FILE)
    
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    try : 
        cursor.execute('SELECT id,name,email,password from USERS WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user : 
            return user
        else :
            return None
    finally : 
        conn.close()

def init_db() : 
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS USERS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(name,email,password) : 
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('INSERT INTO USERS (name,email,password) VALUES (?,?,?)',(name,email,password))
    conn.commit()
    conn.close()

if __name__ == "__main__" : 
    init_db()
else : 
    init_db()