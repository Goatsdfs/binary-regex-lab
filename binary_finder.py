"""
Модуль для проверки и поиска чисел в двоичной системе счисления.

Поддерживает форматы:
- Стандартный: 1010, 0, 111.01
- Программный (с префиксом): 0b1010, 0B110.1
- Суффиксный (математический): 1010b, 1010B, 1010_2
- Знаковый: -101, +0b11
"""

import re
from typing import List

import requests

# Регулярное выражение для поиска двоичных чисел
BINARY_PATTERN = re.compile(  # compile - компиляция происходит один раз, быстро и удобно
    r"(?<![\w.])"  # 1. левая граница: \w покрывает _ и Unicode-буквы
    r"[+-]?"  # 2. знак
    r"(?!0[bB](?![01]))"  # 3. блок префикс-мусора ПОСЛЕ знака
    r"(?:"
    r"0[bB][01]+(?:\.[01]+)?"  # 4. с префиксом
    r"|"
    r"[01]+(?:\.[01]+)?"  # 5. без префикса
    r"(?:_2|[bB])?"  # 6. суффикс
    r")"
    r"(?![\w]|\.[\w])"  # 7. правая граница: \w + точка-перед-словом
)


def is_valid_binary(value: str) -> bool:
    """
    Проверяет, является ли переданная строка корректным двоичным числом.
    """
    if not isinstance(value, str):
        return False
    # fullmatch гарантирует, что вся строка целиком является числом
    return bool(BINARY_PATTERN.fullmatch(value.strip()))


def find_binaries_in_text(text: str) -> List[str]:
    """
    Находит все двоичные числа в переданном тексте.
        Возвращает List[str] - Список найденных двоичных чисел.
    """
    if not isinstance(text, str):
        return []
    return BINARY_PATTERN.findall(text)


def find_binaries_in_file(filepath: str) -> List[str]:
    """
    Читает файл и возвращает список всех найденных в нем двоичных чисел.

    Args:
        filepath (str): Путь к текстовому файлу.

    Returns:
        List[str]: Список найденных двоичных чисел.

    Raises:
        FileNotFoundError: Если файл не найден.
        IOError: При других ошибках чтения файла.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
    return find_binaries_in_text(content)


def find_binaries_on_webpage(url: str, timeout: int = 10) -> List[str]:
    """
    Загружает HTML-страницу по URL и ищет на ней двоичные числа.

    Args:
        url (str): Адрес веб-страницы.
        timeout (int): Таймаут ожидания ответа сервера в секундах.

    Returns:
        List[str]: Список найденных двоичных чисел.

    Raises:
        requests.RequestException: При ошибках сети или некорректном URL.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()

    # Удаляем HTML-теги, чтобы не искать числа внутри атрибутов разметки
    clean_text = re.sub(r"<[^>]+>", " ", response.text)
    return find_binaries_in_text(clean_text)


def main() -> None:
    """Консольный интерфейс для работы с программой."""
    while True:
        print("\n--- Поиск и проверка двоичных чисел ---")
        print("1. Проверить конкретное число (валидация)")
        print("2. Найти двоичные числа в введенном тексте")
        print("3. Найти двоичные числа в файле")
        print("4. Найти двоичные числа на веб-странице (по URL)")
        print("0. Выход")

        choice = input("Выберите действие (0-4): ").strip()

        if choice == "1":
            user_input = input("Введите строку для проверки: ")
            if is_valid_binary(user_input):
                print(f"'{user_input}' — корректное двоичное число.")
            else:
                print(f"'{user_input}' — НЕ является двоичным числом.")

        elif choice == "2":
            user_text = input("Введите текст для поиска: ")
            results = find_binaries_in_text(user_text)
            print(f"Найдено чисел ({len(results)}): {results}")

        elif choice == "3":
            path = input("Введите путь к файлу (например, sample.txt): ").strip()
            try:
                results = find_binaries_in_file(path)
                print(f"Найдено чисел в файле ({len(results)}): {results}")
            except FileNotFoundError:
                print("Ошибка: Файл по указанному пути не найден.")
            except Exception as error:
                print(f"Ошибка при чтении файла: {error}")

        elif choice == "4":
            url = input("Введите URL страницы (с http:// или https://): ").strip()
            try:
                results = find_binaries_on_webpage(url)
                print(f"Найдено чисел на странице ({len(results)}): {results}")
            except requests.RequestException as error:
                print(f"Ошибка при загрузке страницы: {error}")

        elif choice == "0":
            print("Завершение работы.")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
