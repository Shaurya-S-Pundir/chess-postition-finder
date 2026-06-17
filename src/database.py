import sqlite3


def create_database(db_path="positions.db"):
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ply INTEGER NOT NULL,
            fen TEXT NOT NULL,
            white_material INTEGER NOT NULL,
            black_material INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()