from __future__ import annotations

import itertools
import sys
import time
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass


# TOTAL и DELAY вынесены в константы, чтобы все примеры работали одинаково.
# Хочешь ускорить демонстрацию - уменьши DELAY. Хочешь длиннее бар - увеличь TOTAL.
TOTAL = 40
DELAY = 0.03


def fake_work(delay: float = DELAY) -> None:
    """Имитируем маленькую операцию: загрузку, обработку файла, обучение модели."""
    # В реальном коде здесь была бы полезная работа: скачивание файла,
    # обработка строки, обучение одной эпохи модели и т.д.
    time.sleep(delay)


def clear_line() -> None:
    # \r возвращает курсор в начало текущей строки.
    # Затем мы печатаем много пробелов, чтобы стереть старый текст.
    # Последний \r снова ставит курсор в начало очищенной строки.
    sys.stdout.write("\r" + " " * 90 + "\r")
    # flush нужен, чтобы терминал показал текст сразу, а не ждал буферизации.
    sys.stdout.flush()


def demo_percent_only(total: int = TOTAL) -> None:
    """Самый простой вариант: только проценты."""
    # range(total + 1) нужен, чтобы пройти от 0 до total включительно.
    # Иначе последний шаг был бы total - 1, и мы не увидели бы 100%.
    for step in range(total + 1):
        # step / total дает долю выполненной работы от 0 до 1.
        # Умножаем на 100, чтобы получить проценты.
        percent = step / total * 100
        # \r перезаписывает одну и ту же строку вместо печати новой строки.
        # :6.2f значит: ширина 6 символов, 2 знака после точки.
        sys.stdout.write(f"\rПроценты: {percent:6.2f}%")
        sys.stdout.flush()
        fake_work()

    # После завершения переводим курсор на новую строку,
    # чтобы следующий print не прилип к прогрессбару.
    print()


def demo_ascii_bar(total: int = TOTAL, width: int = 30) -> None:
    """Классический прогрессбар из символов # и -."""
    for step in range(total + 1):
        # width - визуальная длина бара в символах.
        # Если выполнена половина работы, filled будет примерно width / 2.
        filled = round(width * step / total)
        empty = width - filled
        percent = step / total * 100
        # Заполненную часть показываем #, пустую часть - дефисами.
        # Такой вариант хорошо работает даже в старых терминалах.
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
        # Идея та же, что в ASCII-варианте, но символы красивее.
        # Минус: в некоторых старых терминалах Unicode может отображаться криво.
        bar = "█" * filled + "░" * empty
        sys.stdout.write(f"\rUnicode:  |{bar}| {percent:6.2f}%")
        sys.stdout.flush()
        fake_work()

    print()


def demo_with_eta(total: int = TOTAL, width: int = 30) -> None:
    """Прогрессбар с прошедшим временем, ETA и скоростью."""
    # perf_counter лучше подходит для измерения коротких промежутков времени,
    # чем обычное time.time().
    started_at = time.perf_counter()

    for step in range(total + 1):
        elapsed = time.perf_counter() - started_at
        # speed - сколько шагов выполняется за секунду.
        # На первом шаге elapsed может быть почти 0, поэтому проверяем деление.
        speed = step / elapsed if elapsed else 0
        # ETA считаем так: оставшиеся шаги / скорость.
        # Если скорость еще неизвестна, показываем 0.
        remaining = (total - step) / speed if speed else 0
        filled = round(width * step / total)
        bar = "#" * filled + "." * (width - filled)

        # Несколько f-строк рядом автоматически склеиваются Python.
        # Это удобнее, чем делать одну очень длинную строку.
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
    # Генератор хорош тем, что не меняет основной код цикла.
    # Вместо for item in data пишем for item in progress_iterable(data, total=len(data)).
    for index, item in enumerate(iterable, start=1):
        # enumerate(..., start=1) делает счетчик с 1, потому что человеку
        # привычнее видеть "1/40", а не "0/40".
        filled = round(width * index / total)
        bar = "#" * filled + "-" * (width - filled)
        sys.stdout.write(f"\r{title}: [{bar}] {index}/{total}")
        sys.stdout.flush()
        # yield возвращает элемент наружу, а потом продолжает выполнение
        # со следующей строки, когда цикл запросит следующий item.
        yield item

    print()


def demo_generator_wrapper(total: int = TOTAL) -> None:
    """Пример использования своей функции progress_iterable."""
    # Здесь range(total) - это "данные", которые мы оборачиваем прогрессбаром.
    # В реальной задаче вместо range может быть список файлов, строк, URL и т.д.
    for _ in progress_iterable(range(total), total=total, title="Wrapper "):
        fake_work()


def demo_spinner(total: int = TOTAL) -> None:
    """Spinner удобен, когда неизвестно, сколько работы осталось."""
    # cycle бесконечно повторяет символы: |, /, -, \, потом снова |...
    frames = itertools.cycle("|/-\\")

    for step in range(total):
        # Spinner не показывает точный процент, но дает понять,
        # что программа не зависла и продолжает работать.
        sys.stdout.write(f"\rSpinner:  {next(frames)} шаг {step + 1}/{total}")
        sys.stdout.flush()
        fake_work()

    # Перед финальным сообщением очищаем строку со spinner-кадром.
    clear_line()
    print("Spinner:  готово")


def demo_tqdm(total: int = TOTAL) -> None:
    """Популярная библиотека tqdm: pip install tqdm."""
    try:
        # Импорт внутри функции сделан специально:
        # если tqdm не установлен, остальные примеры все равно смогут работать.
        from tqdm import tqdm
    except ImportError:
        print("tqdm:     пропущено. Установить: pip install tqdm")
        return

    # tqdm просто оборачивает любой iterable и сам считает проценты, скорость и ETA.
    for _ in tqdm(range(total), desc="tqdm", unit="step"):
        fake_work()


def demo_rich(total: int = TOTAL) -> None:
    """Красивые терминальные интерфейсы через Rich: pip install rich."""
    try:
        # Rich состоит из колонок. Мы сами выбираем, что показывать:
        # текст, полоску, проценты, прошедшее и оставшееся время.
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

    # Контекстный менеджер with сам красиво запускает и завершает отрисовку.
    with Progress(
        TextColumn("[bold cyan]rich"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>5.1f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    ) as progress:
        # add_task создает задачу и возвращает ее id.
        # По этому id потом обновляем прогресс.
        task_id = progress.add_task("work", total=total)

        while not progress.finished:
            fake_work()
            # advance=1 означает: задача продвинулась на один шаг.
            progress.update(task_id, advance=1)


def demo_alive_progress(total: int = TOTAL) -> None:
    """Анимированный прогрессбар: pip install alive-progress."""
    try:
        # Эта библиотека особенно хороша, когда хочется красивую анимацию
        # без настройки колонок вручную.
        from alive_progress import alive_bar
    except ImportError:
        print("alive:    пропущено. Установить: pip install alive-progress")
        return

    with alive_bar(total, title="alive") as bar:
        for _ in range(total):
            fake_work()
            # Каждый вызов bar() сообщает библиотеке: выполнен еще один шаг.
            bar()


@dataclass(frozen=True)
class ProgressExample:
    # dataclass автоматически создает __init__, поэтому ниже можно писать
    # ProgressExample(title, description, run), не создавая конструктор вручную.
    title: str
    description: str
    run: Callable[[], None]


# Список примеров хранит не только функцию, но и текстовое описание.
# Благодаря этому main остается простым: он просто проходит по EXAMPLES.
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
    # Отдельная функция для заголовка нужна, чтобы оформление не дублировалось
    # перед каждым примером.
    print("=" * 80)
    print(example.title)
    print(example.description)
    print()


def main() -> None:
    # main - точка входа программы: здесь собираем демонстрацию целиком.
    print("Варианты прогрессбаров в Python: без библиотек и с библиотеками.")
    print("Для библиотечных примеров можно поставить пакеты:")
    print("pip install tqdm rich alive-progress")
    print()

    for example in EXAMPLES:
        print_header(example)
        # run - это ссылка на функцию. Скобки вызывают выбранный пример.
        example.run()
        print()


if __name__ == "__main__":
    # Этот блок выполнится только при запуске файла напрямую:
    # python3 tests/progressbar.py
    # Если файл импортировать из другого модуля, main() сам не запустится.
    main()
