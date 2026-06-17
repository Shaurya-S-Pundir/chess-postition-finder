from parser import load_game
from snapshot import generate_snapshots
from database import create_database


def main():
    game = load_game("data/raw/sample.pgn")

    snapshots = generate_snapshots(game)

    create_database()

    print(f"Generated {len(snapshots)} snapshots")
    print("Database initialized successfully")


if __name__ == "__main__":
    main()