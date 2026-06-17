import chess.pgn


def load_game(pgn_path: str):
    with open(pgn_path) as pgn_file:
        game = chess.pgn.read_game(pgn_file)

    return game