from __future__ import annotations

import itertools
import sys
import time
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass


TOTAL = 40
DELAY = 0.03


def fake_work(delay: float = DELAY) -> None:
    """Имитируем маленькую операцию: загрузку, обработку файла, обучение модели."""
    time.sleep(delay)


def clear_line() -> None:
    sys.stdout.write("\r" + " " * 90 + "\r")
    sys.stdout.flush()


def demo_percent_only(total: int = TOTAL) -> None:
    """Самый простой вариант: только проценты."""
    for step in range(total + 1):
        percent = step / total * 100
        sys.stdout.write(f"\rПроценты: {percent:6.2f}%")
        sys.stdout.flush()
        fake_work()

    print()


def demo_ascii_bar(total: int = TOTAL, width: int = 30) -> None:
    """Классический прогрессбар из символов # и -."""
    for step in range(total + 1):
        filled = round(width * step / total)
        empty = width - filled
        percent = step / total * 100
        bar = "#" * filled + "-" * empty
        sys.stdout.write(f"\rASCII:    [{bar}] {percent:6.2f}%")
        sys.stdout.flush()
        fake_work()

    print()


def demo_unicode_bar(total: int = TOTAL, width: int = 30) -> None:
    """Более приятная версия для терминалов, которые поддерживают Unicode."""
    for step in range(total + 1):
        filled = round(width * step / total)
        empty = width - filled
        percent = step / total * 100
        bar = "█" * filled + "░" * empty
        sys.stdout.write(f"\rUnicode:  |{bar}| {percent:6.2f}%")
        sys.stdout.flush()
        fake_work()

    print()


def demo_with_eta(total: int = TOTAL, width: int = 30) -> None:
    """Прогрессбар с прошедшим временем, ETA и скоростью."""
    started_at = time.perf_counter()

    for step in range(total + 1):
        elapsed = time.perf_counter() - started_at
        speed = step / elapsed if elapsed else 0
        remaining = (total - step) / speed if speed else 0
        filled = round(width * step / total)
        bar = "#" * filled + "." * (width - filled)

        sys.stdout.write(
            f"\rETA:      [{bar}] {step:>2}/{total} "
            f"elapsed={elapsed:4.1f}s eta={remaining:4.1f}s speed={speed:4.1f}/s"
        )
        sys.stdout.flush()
        fake_work()

    print()


def progress_iterable(
    iterable: Iterable[int],
    *,
    total: int,
    title: str = "Итератор",
    width: int = 30,
) -> Iterator[int]:
    """Обертка-генератор: можно использовать вокруг любого цикла for."""
    for index, item in enumerate(iterable, start=1):
        filled = round(width * index / total)
        bar = "#" * filled + "-" * (width - filled)
        sys.stdout.write(f"\r{title}: [{bar}] {index}/{total}")
        sys.stdout.flush()
        yield item

    print()


def demo_generator_wrapper(total: int = TOTAL) -> None:
    """Пример использования своей функции progress_iterable."""
    for _ in progress_iterable(range(total), total=total, title="Wrapper "):
        fake_work()


def demo_spinner(total: int = TOTAL) -> None:
    """Spinner удобен, когда неизвестно, сколько работы осталось."""
    frames = itertools.cycle("|/-\\")

    for step in range(total):
        sys.stdout.write(f"\rSpinner:  {next(frames)} шаг {step + 1}/{total}")
        sys.stdout.flush()
        fake_work()

    clear_line()
    print("Spinner:  готово")


def demo_tqdm(total: int = TOTAL) -> None:
    """Популярная библиотека tqdm: pip install tqdm."""
    try:
        from tqdm import tqdm
    except ImportError:
        print("tqdm:     пропущено. Установить: pip install tqdm")
        return

    for _ in tqdm(range(total), desc="tqdm", unit="step"):
        fake_work()


def demo_rich(total: int = TOTAL) -> None:
    """Красивые терминальные интерфейсы через Rich: pip install rich."""
    try:
        from rich.progress import (
            BarColumn,
            Progress,
            TextColumn,
            TimeElapsedColumn,
            TimeRemainingColumn,
        )
    except ImportError:
        print("rich:     пропущено. Установить: pip install rich")
        return

    with Progress(
        TextColumn("[bold cyan]rich"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>5.1f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    ) as progress:
        task_id = progress.add_task("work", total=total)

        while not progress.finished:
            fake_work()
            progress.update(task_id, advance=1)


def demo_alive_progress(total: int = TOTAL) -> None:
    """Анимированный прогрессбар: pip install alive-progress."""
    try:
        from alive_progress import alive_bar
    except ImportError:
        print("alive:    пропущено. Установить: pip install alive-progress")
        return

    with alive_bar(total, title="alive") as bar:
        for _ in range(total):
            fake_work()
            bar()


@dataclass(frozen=True)
class ProgressExample:
    title: str
    description: str
    run: Callable[[], None]


EXAMPLES = [
    ProgressExample(
        "1. Только проценты",
        "Минимальный вариант через \\r: перезаписываем одну строку терминала.",
        demo_percent_only,
    ),
    ProgressExample(
        "2. ASCII bar",
        "Работает почти везде: # для заполненной части, - для пустой.",
        demo_ascii_bar,
    ),
    ProgressExample(
        "3. Unicode bar",
        "Красивее в современных терминалах, но зависит от поддержки символов.",
        demo_unicode_bar,
    ),
    ProgressExample(
        "4. ETA и скорость",
        "Полезно для долгих задач: показывает время, остаток и скорость.",
        demo_with_eta,
    ),
    ProgressExample(
        "5. Обертка-генератор",
        "Удобная функция progress_iterable для любых циклов for.",
        demo_generator_wrapper,
    ),
    ProgressExample(
        "6. Spinner",
        "Подходит, когда общего количества шагов нет или оно неизвестно.",
        demo_spinner,
    ),
    ProgressExample(
        "7. tqdm",
        "Самый простой библиотечный вариант для циклов и pandas/numpy-задач.",
        demo_tqdm,
    ),
    ProgressExample(
        "8. Rich",
        "Хорош для красивых CLI-приложений, таблиц, цветов и нескольких задач.",
        demo_rich,
    ),
    ProgressExample(
        "9. alive-progress",
        "Очень живые анимации и приятный вывод для терминала.",
        demo_alive_progress,
    ),
]


def print_header(example: ProgressExample) -> None:
    print("=" * 80)
    print(example.title)
    print(example.description)
    print()


def main() -> None:
    print("Варианты прогрессбаров в Python: без библиотек и с библиотеками.")
    print("Для библиотечных примеров можно поставить пакеты:")
    print("pip install tqdm rich alive-progress")
    print()

    for example in EXAMPLES:
        print_header(example)
        example.run()
        print()


if __name__ == "__main__":
    main()
