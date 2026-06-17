# Chess Position Finder

A command-line tool that parses PGN chess games, stores every position snapshot in a SQLite database, and lets you query positions by piece placement and material constraints.

---

## Features

- Parse PGN files using `python-chess`
- Evaluate material for both sides at every ply
- Store position snapshots and piece-square occurrences in SQLite
- Query positions by piece location (e.g. rook on a specific square)
- Filter positions by material thresholds (min/max for white and black)

---

## Requirements

- Python 3.9+
- [`python-chess`](https://python-chess.readthedocs.io/)

---

## Setup

```bash
# Clone the repository
git clone https://github.com/Shaurya-S-Pundir/chess-position-finder.git
cd chess-position-finder

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running

Place a PGN file at `data/raw/sample.pgn`, then run:

```bash
cd src
python main.py
```

This will:
1. Create `positions.db` (SQLite) if it does not exist
2. Parse the game from the PGN file
3. Store a snapshot for every ply (initial position + after each move)
4. Print the total number of positions stored
5. Run example queries and print results

---

## Project Structure

```
chess-position-finder/
├── data/
│   └── raw/
│       └── sample.pgn        # Input PGN file
├── src/
│   ├── main.py               # Entry point
│   ├── parser.py             # PGN loading
│   ├── material.py           # Material evaluation
│   ├── snapshot.py           # Position snapshot generation
│   ├── database.py           # SQLite schema and insert helpers
│   ├── occurrences.py        # Piece-square occurrence extraction
│   └── query_engine.py       # Query functions
├── tests/
│   └── test_material.py      # Unit tests for material counting
├── requirements.txt
└── README.md
```

---

## Database Schema

### `positions`

Stores one row per ply per game.

| Column           | Type    | Description                        |
|------------------|---------|------------------------------------|
| `id`             | INTEGER | Primary key                        |
| `ply`            | INTEGER | Half-move number (0 = start)       |
| `fen`            | TEXT    | Full FEN string of the position    |
| `white_material` | INTEGER | White's total material value       |
| `black_material` | INTEGER | Black's total material value       |

### `piece_occurrences`

Stores one row per piece per position.

| Column        | Type    | Description                              |
|---------------|---------|------------------------------------------|
| `id`          | INTEGER | Primary key                              |
| `position_id` | INTEGER | Foreign key → `positions.id`             |
| `piece_type`  | TEXT    | `pawn`, `knight`, `bishop`, `rook`, `queen`, `king` |
| `color`       | TEXT    | `white` or `black`                       |
| `square`      | TEXT    | Algebraic square name, e.g. `e4`         |

### Material values

| Piece   | Value |
|---------|-------|
| Pawn    | 1     |
| Knight  | 3     |
| Bishop  | 3     |
| Rook    | 5     |
| Queen   | 9     |
| King    | 0     |

---

## API Reference

### `find_positions(conn, ...)` — `src/query_engine.py`

Queries the `positions` table with optional filters. All parameters are optional; omitted parameters are not added to the `WHERE` clause.

```python
import sqlite3
from query_engine import find_positions

conn = sqlite3.connect("positions.db")

positions = find_positions(
    conn,
    rook_square="e5",          # filter by rook on this square
    side="white",              # "white" or "black" (required with rook_square)
    min_white_material=30,     # white_material >= 30
    max_white_material=39,     # white_material <= 39
    min_black_material=25,     # black_material >= 25
    max_black_material=35,     # black_material <= 35
)

for row in positions:
    print(row)
```

Each returned row is a tuple: `(id, ply, fen, white_material, black_material)`.

---

### `count_rook_on_square(square, db_path)` — `src/query_engine.py`

Returns the total number of times any rook appeared on the given square across all stored positions.

```python
from query_engine import count_rook_on_square

count = count_rook_on_square("h1")
print(f"Rook on h1 appeared {count} times")
```

---

## Usage Examples

### Example 1 — Positions where white has at least 30 material

```python
conn = sqlite3.connect("positions.db")
positions = find_positions(conn, min_white_material=30)
print(f"Found {len(positions)} positions")
```

### Example 2 — Late endgame: both sides below 15 material

```python
conn = sqlite3.connect("positions.db")
positions = find_positions(
    conn,
    max_white_material=15,
    max_black_material=15,
)
print(f"Found {len(positions)} endgame positions")
```

### Example 3 — White rook on d5, white material advantage

```python
conn = sqlite3.connect("positions.db")
positions = find_positions(
    conn,
    rook_square="d5",
    side="white",
    min_white_material=20,
    max_black_material=15,
)
for row in positions:
    position_id, ply, fen, white_mat, black_mat = row
    print(f"Ply {ply}: white={white_mat}, black={black_mat}")
    print(f"  FEN: {fen}")
```

### Example 4 — How often did a rook visit b5?

```python
from query_engine import count_rook_on_square

print(count_rook_on_square("b5"))
```

---

## Running Tests

```bash
# From the project root
python -m unittest tests/test_material.py -v
```

---

## License

MIT