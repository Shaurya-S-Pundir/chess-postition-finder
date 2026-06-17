import chess


def extract_piece_occurrences(board):
    occurrences = []

    for square, piece in board.piece_map().items():
        occurrences.append(
            {
                "piece_type": piece.piece_type,
                "color": "white" if piece.color else "black",
                "square": chess.square_name(square),
            }
        )

    return occurrences