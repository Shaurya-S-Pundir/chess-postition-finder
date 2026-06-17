import sqlite3

from parser import load_game
from database import (
    create_database,
    insert_position,
    insert_occurrences,
)
from material import calculate_material
from occurrences import extract_piece_occurrences
from query_engine import count_rook_on_square

def main():
    create_database()

    conn = sqlite3.connect("positions.db")

    game = load_game("data/raw/sample.pgn")

    board = game.board()

    moves = list(game.mainline_moves())

    snapshots_stored = 0

    # Store initial position
    white_material, black_material = calculate_material(board)

    snapshot = {
        "ply": 0,
        "fen": board.fen(),
        "white_material": white_material,
        "black_material": black_material,
    }

    position_id = insert_position(conn, snapshot)

    occurrences = extract_piece_occurrences(board)

    insert_occurrences(
        conn,
        position_id,
        occurrences,
    )

    snapshots_stored += 1

    # Store positions after each move
    for ply, move in enumerate(moves, start=1):
        board.push(move)

        white_material, black_material = calculate_material(board)

        snapshot = {
            "ply": ply,
            "fen": board.fen(),
            "white_material": white_material,
            "black_material": black_material,
        }

        position_id = insert_position(conn, snapshot)

        occurrences = extract_piece_occurrences(board)

        insert_occurrences(
            conn,
            position_id,
            occurrences,
        )

        snapshots_stored += 1

    conn.commit()
    conn.close()

    print(f"Stored {snapshots_stored} positions")

    # Querying 
    rook_count = count_rook_on_square("b5")
    print(f"Number of positions with a white rook on h1: {rook_count}")


if __name__ == "__main__":
    main()