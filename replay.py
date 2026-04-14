import re
from typing import List, Tuple, Dict, Optional

# a move is ((from_row, from_col), (to_row, to_col))
Move = Tuple[Tuple[int, int], Tuple[int, int]]
Grid = List[List[int]]


_MOVE_RE = re.compile(r"\((\d+)\s*,\s*(\d+)\)\s*->\s*\((\d+)\s*,\s*(\d+)\)")


def _format_grid(grid: Grid) -> List[str]:
    """create a 2D grid"""
    lines = ["# Board State:"]
    for row in grid:
        cells = " ".join(f"{val:>2}" for val in row)
        lines.append(f"# {cells}")
    return lines


def _parse_grid(grid_lines: List[str]) -> Grid:
    """parse the commented grid lines back into a 2D list of ints"""
    grid: Grid = []
    for line in grid_lines:
        cleaned = line.lstrip("#").strip()
        if not cleaned:
            continue
        row = [int(x) for x in cleaned.split()]
        grid.append(row)
    return grid


def format_record(
    result: str,
    mode: str,
    board_type: str,
    size: int,
    moves: List[Move],
    start_grid: Optional[Grid] = None,
) -> str:



    lines = [
        f"# Result: {result}",
        f"# Mode: {mode}",
        f"# Board: {board_type}",
        f"# Size: {size}",
        f"# Total Moves: {len(moves)}",
    ]
    if start_grid is not None:
        lines.extend(_format_grid(start_grid))
    lines.append("-" * 30)
    for i, (src, dst) in enumerate(moves, start=1):
        lines.append(f"Move {i}: ({src[0]},{src[1]}) -> ({dst[0]},{dst[1]})")
    return "\n".join(lines)


def save_record(
    path: str,
    result: str,
    mode: str,
    board_type: str,
    size: int,
    moves: List[Move],
    start_grid: Optional[Grid] = None,
) -> None:
    """write a game record to disk as a .txt file."""
    content = format_record(result, mode, board_type, size, moves, start_grid)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)




def load_replay(path: str) -> Tuple[Dict[str, str], Optional[Grid], List[Move]]:
    meta: Dict[str, str] = {}
    moves: List[Move] = []
    grid_lines: List[str] = []
    in_grid = False

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if set(line) <= {"-"}:
                in_grid = False
                continue
            if line.startswith("#"):
                stripped = line.lstrip("#").strip()
                if stripped.lower().startswith("board state"):
                    in_grid = True
                    continue
                if in_grid:
                    grid_lines.append(line)
                    continue
                key, sep, val = stripped.partition(":")
                if sep:
                    meta[key.strip()] = val.strip()
                continue
            m = _MOVE_RE.search(line)
            if m:
                r1, c1, r2, c2 = map(int, m.groups())
                moves.append(((r1, c1), (r2, c2)))

    start_grid = _parse_grid(grid_lines) if grid_lines else None
    return meta, start_grid, moves
