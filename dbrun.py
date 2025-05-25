import sqlite3

def initialize_database():
    conn = sqlite3.connect('docusortDB.db')
    cursor = conn.cursor()

    # Create documents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_fname TEXT NOT NULL,
            sender_surname TEXT NOT NULL,
            studnum TEXT NOT NULL,
            sender_section TEXT NOT NULL,
            sender_fac TEXT NOT NULL,
            sender_course TEXT NOT NULL,
            sender_email TEXT NOT NULL,
            rcvr_fac TEXT NOT NULL,
            rcvr_name TEXT NOT NULL,
            rcvr_email TEXT NOT NULL,
            doc_description TEXT NOT NULL,
            datetime TEXT NOT NULL,
            doc_type TEXT NOT NULL
        )
    ''')

    # Create admin_users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT UNIQUE NOT NULL,
            admin_email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            date_created TEXT NOT NULL,
            last_login TEXT
        )
    ''')

    # Optional: Insert default admin user if table is empty
    cursor.execute("SELECT COUNT(*) FROM admin_users")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO admin_users (fullname, admin_email, username, password, role, date_created)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        ''', ("Administrator", "admin@example.com", "admin", "admin123", "Super Admin"))

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

# Run the initializer
if __name__ == "__main__":
    initialize_database()
