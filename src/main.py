from parser import load_game


def main():
    game = load_game("data/raw/sample.pgn")

    print(f"White: {game.headers['White']}")
    print(f"Black: {game.headers['Black']}")
    print(f"Opening: {game.headers['Opening']}")
    print()

    board = game.board()

    move_count = 1

    for move in game.mainline_moves():
        print(move_count, move.uci())

        board.push(move)
        move_count += 1


if __name__ == "__main__":
    main()