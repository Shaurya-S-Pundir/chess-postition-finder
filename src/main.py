from parser import load_game
from material import calculate_material


def main():
    game = load_game("data/raw/sample.pgn")

    board = game.board()

    white_material, black_material = calculate_material(board)

    print(
        f"Initial Material -> White: {white_material}, Black: {black_material}"
    )

    for move in game.mainline_moves():
        board.push(move)

        white_material, black_material = calculate_material(board)

        print(
            f"{move.uci()} -> White: {white_material}, Black: {black_material}"
        )


if __name__ == "__main__":
    main()