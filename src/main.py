import os
import sqlite3

# Project root is one level above this file (src/)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from parser import load_game
from database import (
    create_database,
    insert_position,
    insert_occurrences,
)
from material import calculate_material
from occurrences import extract_piece_occurrences
from query_engine import count_rook_on_square, find_positions

def main():
    db_path = os.path.join(ROOT_DIR, "positions.db")
    pgn_path = os.path.join(ROOT_DIR, "data", "raw", "sample.pgn")

    create_database(db_path)

    conn = sqlite3.connect(db_path)

    game = load_game(pgn_path)

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

    conn = sqlite3.connect(db_path)

    # Querying
    rook_count = count_rook_on_square("b5", db_path=db_path)
    print(f"Number of positions with a white rook on h1: {rook_count}")

    # Find positions with white rook on g5, black on a8, white material >= 35, black material <= 40
    positions = find_positions(
        conn,
        rook_square="g5",
        side="white",
        min_white_material=35,
        max_black_material=40,
    )   

    print(f"\nFound {len(positions)} positions matching criteria:")
    for pos in positions:
        print(pos)


if __name__ == "__main__":
    main()