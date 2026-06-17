import chess

from material import calculate_material


def generate_snapshots(game):
    board = game.board()

    snapshots = []

    # Initial position
    white_material, black_material = calculate_material(board)

    snapshots.append(
        {
            "ply": 0,
            "fen": board.fen(),
            "white_material": white_material,
            "black_material": black_material,
        }
    )

    ply = 1

    for move in game.mainline_moves():
        board.push(move)

        white_material, black_material = calculate_material(board)

        snapshots.append(
            {
                "ply": ply,
                "fen": board.fen(),
                "white_material": white_material,
                "black_material": black_material,
            }
        )

        ply += 1

    return snapshots