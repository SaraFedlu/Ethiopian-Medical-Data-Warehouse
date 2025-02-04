import sqlite3

def create_database():
    conn = sqlite3.connect("data/medical_data.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER PRIMARY KEY,
            channel TEXT,
            date TEXT,
            text TEXT,
            media TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized!")

if __name__ == "__main__":
    create_database()