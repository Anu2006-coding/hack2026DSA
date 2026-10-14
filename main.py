import csv
import random
from collections import deque
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation


INPUT_FILE = "maze.csv"
OUTPUT_FILE = "path_output.csv"


# 1. READ AND VALIDATE MAZE
def read_maze(filename):
    with open(filename, newline="", encoding="utf-8-sig") as f:
        grid = [
            [cell.strip() for cell in row]
            for row in csv.reader(f)
            if row and any(cell.strip() for cell in row)
        ]

    if not grid:
        raise ValueError("Maze file is empty.")

    n = len(grid)

    if any(len(row) != n for row in grid):
        raise ValueError("Maze must be an N x N square grid.")

    allowed = set(".#SEabcdefABCDEF")

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell not in allowed:
                raise ValueError(
                    f"Invalid symbol {cell!r} at row {r + 1}, "
                    f"column {c + 1}."
                )

    for symbol in ("S", "E"):
        count = sum(cell == symbol for row in grid for cell in row)
        if count != 1:
            raise ValueError(
                f"Maze must contain exactly one {symbol}."
            )

    keys = {cell for row in grid for cell in row if cell in "abcdef"}
    doors = {
        cell.lower()
        for row in grid
        for cell in row
        if cell in "ABCDF"
    }

    if keys != doors:
        raise ValueError(
            f"Keys and doors must match. Keys={keys}, doors={doors}"
        )

    return grid, len(keys)


# 2. GENERATE A RANDOM SOLVABLE MAZE
def generate_maze(t, n):
    if not 1 <= t <= 6:
        raise ValueError("T must be between 1 and 6.")

    if n < max(5, t + 2):
        raise ValueError(
            f"Grid size must be at least {max(5, t + 2)}."
        )

    grid = [["#" for _ in range(n)] for _ in range(n)]

    # Guaranteed route: down column 0, then across the bottom row.
    route = [(r, 0) for r in range(n)]
    route.extend((n - 1, c) for c in range(1, n))
    route_set = set(route)

    for r, c in route:
        grid[r][c] = "."

    grid[0][0] = "S"
    grid[n - 1][n - 1] = "E"

    # Place keys and doors in order on the guaranteed route.
    for i in range(t):
        key_index = 1 + 2 * i
        door_index = key_index + 1

        kr, kc = route[key_index]
        dr, dc = route[door_index]

        grid[kr][kc] = chr(ord("a") + i)
        grid[dr][dc] = chr(ord("A") + i)

    # Randomize only cells outside the guaranteed route.
    for r in range(n):
        for c in range(n):
            if (r, c) not in route_set:
                grid[r][c] = (
                    "." if random.random() < 0.60 else "#"
                )

    return grid


# 3. BFS SHORTEST PATH
def bfs(grid):
    n = len(grid)

    start = next(
        (r, c)
        for r in range(n)
        for c in range(n)
        if grid[r][c] == "S"
    )

    end = next(
        (r, c)
        for r in range(n)
        for c in range(n)
        if grid[r][c] == "E"
    )

    # State = row, column, collected-key bitmask.
    initial = (start[0], start[1], 0)
    queue = deque([initial])

    distance = {initial: 0}
    parent = {initial: None}

    directions = [
        (0, 1), (1, 0), (0, -1), (-1, 0)
    ]

    while queue:
        r, c, mask = queue.popleft()
        current = (r, c, mask)

        if (r, c) == end:
            states = []
            state = current

            while state is not None:
                states.append(state)
                state = parent[state]

            states.reverse()
            path = [(r, c) for r, c, _ in states]

            return distance[current], path, states

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if not (0 <= nr < n and 0 <= nc < n):
                continue

            cell = grid[nr][nc]

            if cell == "#":
                continue

            new_mask = mask

            # Door requires its matching key.
            if cell in "ABCDF":
                bit = 1 << (ord(cell.lower()) - ord("a"))

                if not (mask & bit):
                    continue

            # Collect key automatically.
            if cell in "abcdef":
                bit = 1 << (ord(cell) - ord("a"))
                new_mask |= bit

            next_state = (nr, nc, new_mask)

            if next_state not in distance:
                distance[next_state] = distance[current] + 1
                parent[next_state] = current
                queue.append(next_state)

    return -1, [], []


# 4. EXPORT SHORTEST PATH TO CSV
def save_path_csv(grid, path):
    path_cells = set(path)
    output = []

    for r, row in enumerate(grid):
        output_row = []

        for c, cell in enumerate(row):
            if (r, c) in path_cells and cell == ".":
                output_row.append("x")
            else:
                output_row.append(cell)

        output.append(output_row)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(output)

    print("Path CSV saved:", Path(OUTPUT_FILE).resolve())


# 5. COLORED MAZE AND ANIMATION
def visualize(grid, states, length):
    if not states:
        print("No path to visualize.")
        return

    n = len(grid)

    colors = [
        "white",       # 0 open
        "black",       # 1 wall
        "green",       # 2 start
        "red",         # 3 exit
        "#4A90E2",     # 4 key
        "#F5A623",     # 5 door
        "#B7E4C7",     # 6 path
        "#D9D9D9",     # 7 collected key / opened door
        "#B9D8FF"      # 8 current position
    ]

    cmap = ListedColormap(colors)
    fig, ax = plt.subplots(figsize=(8, 8))

    def update(frame):
        ax.clear()
        r, c, mask = states[frame]

        values = []

        for rr in range(n):
            row_values = []

            for cc in range(n):
                cell = grid[rr][cc]

                if cell == "#":
                    value = 1
                elif cell == "S":
                    value = 2
                elif cell == "E":
                    value = 3
                elif cell in "abcdef":
                    bit = 1 << (ord(cell) - ord("a"))
                    value = 7 if mask & bit else 4
                elif cell in "ABCDEF":
                    bit = 1 << (ord(cell.lower()) - ord("a"))
                    value = 7 if mask & bit else 5
                else:
                    value = 0

                visited = any(
                    (rr, cc) == (pr, pc)
                    for pr, pc, _ in states[:frame + 1]
                )

                if visited and cell == ".":
                    value = 6

                if (rr, cc) == (r, c):
                    value = 8

                row_values.append(value)

            values.append(row_values)

        ax.imshow(values, cmap=cmap, vmin=0, vmax=8)

        for rr in range(n):
            for cc in range(n):
                cell = grid[rr][cc]
                label = cell

                if cell in "abcdef":
                    bit = 1 << (ord(cell) - ord("a"))
                    if mask & bit:
                        label = ""

                elif cell in "ABCDEF":
                    bit = 1 << (ord(cell.lower()) - ord("a"))
                    if mask & bit:
                        label = "✓"

                if label:
                    ax.text(
                        cc, rr, label,
                        ha="center", va="center",
                        color="white" if cell in "#S" else "black",
                        fontweight="bold"
                    )

        inventory = [
            chr(ord("a") + i)
            for i in range(6)
            if mask & (1 << i)
        ]

        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_xticks(
            [x - 0.5 for x in range(1, n)], minor=True
        )
        ax.set_yticks(
            [y - 0.5 for y in range(1, n)], minor=True
        )
        ax.grid(which="minor", color="gray", linewidth=1)
        ax.tick_params(length=0)

        ax.set_title(
            f"Shortest path: {length} moves | "
            f"Step: {frame} | Keys: {inventory or 'None'}"
        )

    animation = FuncAnimation(
        fig, update,
        frames=len(states),
        interval=500,
        repeat=False,
        cache_frame_data=False
    )

    plt.tight_layout()
    plt.show()


# 6. MAIN PROGRAM
def main():
    print("\n=== MAZE WITH KEYS AND DOORS ===")
    print("1. Read maze from CSV")
    print("2. Generate random solvable maze")

    choice = input("Choose option (1 or 2): ").strip()

    try:
        if choice == "1":
            grid, actual_t = read_maze(INPUT_FILE)

            t = int(input("Number of key/door types (1-6): "))

            if not 1 <= t <= 6:
                raise ValueError("T must be between 1 and 6.")

            if t != actual_t:
                raise ValueError(
                    f"CSV contains {actual_t} key/door types, "
                    f"but you entered {t}."
                )

        elif choice == "2":
            t = int(input("Number of key/door types (1-6): "))
            n = int(input("Grid size N (minimum 5): "))

            grid = generate_maze(t, n)

            with open(INPUT_FILE, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(grid)

            print("Generated maze saved to:", INPUT_FILE)

        else:
            raise ValueError("Enter 1 or 2.")

        print("\nGenerated / loaded maze:")
        for row in grid:
            print(" ".join(row))

        length, path, states = bfs(grid)

        print("\nShortest path length:", length)

        if length == -1:
            print("No valid path exists.")
            return

        print("Shortest path coordinates:", path)

        save_path_csv(grid, path)
        visualize(grid, states, length)

    except (ValueError, OSError, csv.Error) as error:
        print("Error:", error)


if __name__ == "__main__":
    main()