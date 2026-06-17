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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS piece_occurrences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            position_id INTEGER NOT NULL,
            piece_type TEXT NOT NULL,
            color TEXT NOT NULL,
            square TEXT NOT NULL,
            FOREIGN KEY(position_id) REFERENCES positions(id)
        )
    """)

    conn.commit()
    conn.close()
def insert_position(conn, snapshot):
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO positions
        (
            ply,
            fen,
            white_material,
            black_material
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            snapshot["ply"],
            snapshot["fen"],
            snapshot["white_material"],
            snapshot["black_material"],
        ),
    )

    return cursor.lastrowid


def insert_occurrences(
    conn,
    position_id,
    occurrences,
):
    cursor = conn.cursor()

    for occurrence in occurrences:
        piece_names = {
            1: "pawn",
            2: "knight",
            3: "bishop",
            4: "rook",
            5: "queen",
            6: "king",
        }

        cursor.execute(
            """
            INSERT INTO piece_occurrences
            (
                position_id,
                piece_type,
                color,
                square
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                position_id,
                piece_names[
                    occurrence["piece_type"]
                ],
                occurrence["color"],
                occurrence["square"],
            ),
        )