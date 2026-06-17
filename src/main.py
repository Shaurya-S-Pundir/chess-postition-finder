from parser import load_game
from snapshot import generate_snapshots


def main():
    game = load_game("data/raw/sample.pgn")

    snapshots = generate_snapshots(game)

    print(f"Generated {len(snapshots)} snapshots")

    print("\nFirst Snapshot:")
    print(snapshots[0])

    print("\nLast Snapshot:")
    print(snapshots[-1])


if __name__ == "__main__":
    main()