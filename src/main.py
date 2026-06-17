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

import glob


def ingest_game(conn, pgn_path):
    """Parse one PGN file and store all position snapshots into the DB."""
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
    insert_occurrences(conn, position_id, occurrences)
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
        insert_occurrences(conn, position_id, occurrences)
        snapshots_stored += 1

    return snapshots_stored


def main():
    db_path = os.path.join(ROOT_DIR, "positions.db")
    pgn_dir = os.path.join(ROOT_DIR, "data", "raw")

    create_database(db_path)

    conn = sqlite3.connect(db_path)

    pgn_files = sorted(glob.glob(os.path.join(pgn_dir, "*.pgn")))

    total_snapshots = 0

    for pgn_path in pgn_files:
        count = ingest_game(conn, pgn_path)
        print(f"  {os.path.basename(pgn_path)}: stored {count} positions")
        total_snapshots += count

    conn.commit()
    conn.close()

    print(f"\nTotal positions stored: {total_snapshots}")

    conn = sqlite3.connect(db_path)

    # Querying
    rook_count = count_rook_on_square("b5", db_path=db_path)
    print(f"Rook on b5 appeared {rook_count} time(s) across all positions")

    # Find positions with white rook on g5, white material >= 35, black material <= 40
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

    conn.close()


if __name__ == "__main__":
    main()