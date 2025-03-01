import sqlite3

def create_connection():
    conn = sqlite3.connect('contacts.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_contact(name, phone, email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
    conn.commit()
    conn.close()

def edit_contact(contact_id, name, phone, email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?', (name, phone, email, contact_id))
    conn.commit()
    conn.close()

def delete_contact(contact_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    conn.close()

def search_contacts(query):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?', ('%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    conn.close()
    return results 