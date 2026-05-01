from __future__ import annotations

import importlib
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def import_python_chess() -> tuple[Any, Any]:
    """Import python-chess even when this file is named chess.py."""
    current_dir = Path(__file__).resolve().parent
    removed_paths: list[str] = []

    for path in list(sys.path):
        if Path(path or ".").resolve() == current_dir:
            sys.path.remove(path)
            removed_paths.append(path)

    try:
        chess_module = importlib.import_module("chess")
        variant_module = importlib.import_module("chess.variant")
    finally:
        for path in reversed(removed_paths):
            sys.path.insert(0, path)

    return chess_module, variant_module


chess, variant = import_python_chess()


@dataclass(frozen=True)
class BoardExample:
    title: str
    create_board: Callable[[], Any]
    code: str


BOARD_EXAMPLES = [
    BoardExample(
        "Обычные шахматы",
        chess.Board,
        "chess.Board()",
    ),
    BoardExample(
        "Chess960 / шахматы Фишера",
        lambda: chess.Board.from_chess960_pos(42),
        "chess.Board.from_chess960_pos(42)",
    ),
    BoardExample(
        "Пустая доска для своей расстановки",
        lambda: chess.Board(None),
        "chess.Board(None)",
    ),
    BoardExample(
        "Доска из FEN",
        lambda: chess.Board(
            "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
        ),
        "chess.Board('FEN-строка')",
    ),
    BoardExample(
        "Crazyhouse",
        variant.CrazyhouseBoard,
        "chess.variant.CrazyhouseBoard()",
    ),
    BoardExample(
        "Suicide",
        variant.SuicideBoard,
        "chess.variant.SuicideBoard()",
    ),
    BoardExample(
        "Giveaway",
        variant.GiveawayBoard,
        "chess.variant.GiveawayBoard()",
    ),
    BoardExample(
        "Antichess",
        variant.AntichessBoard,
        "chess.variant.AntichessBoard()",
    ),
    BoardExample(
        "Atomic",
        variant.AtomicBoard,
        "chess.variant.AtomicBoard()",
    ),
    BoardExample(
        "King of the Hill",
        variant.KingOfTheHillBoard,
        "chess.variant.KingOfTheHillBoard()",
    ),
    BoardExample(
        "Racing Kings",
        variant.RacingKingsBoard,
        "chess.variant.RacingKingsBoard()",
    ),
    BoardExample(
        "Horde",
        variant.HordeBoard,
        "chess.variant.HordeBoard()",
    ),
    BoardExample(
        "Three-check",
        variant.ThreeCheckBoard,
        "chess.variant.ThreeCheckBoard()",
    ),
]


def side_name(board: Any) -> str:
    return "белые" if board.turn == chess.WHITE else "черные"


def print_board(example: BoardExample) -> None:
    board = example.create_board()

    print("=" * 80)
    print(example.title)
    print(f"Код: {example.code}")
    print(f"Ходят: {side_name(board)}")
    print(f"FEN: {board.fen()}")
    print(f"Легальных ходов: {board.legal_moves.count()}")
    print()
    print(board.unicode())
    print()


def main() -> None:
    print("Все основные типы досок, которые есть в python-chess:")
    print()

    for example in BOARD_EXAMPLES:
        print_board(example)

    print("Важно: через FEN можно создать почти бесконечно много разных позиций.")
    print("Например: board = chess.Board('твоя FEN-строка')")


if __name__ == "__main__":
    main()
