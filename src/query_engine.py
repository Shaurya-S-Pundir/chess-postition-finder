import sqlite3


def count_rook_on_square(square, db_path="positions.db"):
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM piece_occurrences
        WHERE piece_type = 'rook'
        AND square = ?
        """,
        (square,),
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count