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

def find_positions(
    conn,
    rook_square=None,
    side=None,
    min_white_material=None,
    max_white_material=None,
    min_black_material=None,
    max_black_material=None,
):
    query = "SELECT * FROM positions WHERE 1=1"
    params = []

    if rook_square and side:
        column = f"{side}_rooks"
        query += f" AND {column} LIKE ?"
        params.append(f"%{rook_square}%")

    if min_white_material is not None:
        query += " AND white_material >= ?"
        params.append(min_white_material)

    if max_white_material is not None:
        query += " AND white_material <= ?"
        params.append(max_white_material)

    if min_black_material is not None:
        query += " AND black_material >= ?"
        params.append(min_black_material)

    if max_black_material is not None:
        query += " AND black_material <= ?"
        params.append(max_black_material)

    positions = conn.execute(query, params).fetchall()
    return positions