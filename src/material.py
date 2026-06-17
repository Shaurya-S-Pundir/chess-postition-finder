import chess

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,  # King has no material value
}

def calculate_material(board: chess.Board) -> dict:
    white_material = 0
    black_material = 0
    for piece_type, value in PIECE_VALUES.items():
        white_material += value * len(board.pieces(piece_type, chess.WHITE))
        black_material += value * len(board.pieces(piece_type, chess.BLACK))
    
    return white_material, black_material

    