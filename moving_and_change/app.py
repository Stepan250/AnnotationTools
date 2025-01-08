import os
import time
import shutil
from pathlib import Path
import msvcrt

# Папка, которую нужно отслеживать
source_folder = Path("~/Downloads").expanduser()

# Папка, куда перемещать файлы
destination_folder = Path("../target_folder").resolve()

# Префикс имени файла
file_prefix = "test_"

# Начальное значение для номера
base_number = "00025"

# Время запуска скрипта
script_start_time = time.time()

# Создаем папку назначения, если её нет
destination_folder.mkdir(parents=True, exist_ok=True)


# Функция для получения следующего доступного номера
def get_next_count(base_number):
    existing_files = os.listdir(destination_folder)
    existing_numbers = set()

    for file in existing_files:
        if file.startswith(f"{file_prefix}{base_number}_") and file.endswith(".jpg"):
            parts = file[len(file_prefix):-4].split("_")
            if len(parts) == 2 and parts[1].isdigit():
                existing_numbers.add(int(parts[1]))

    # Найти первый отсутствующий номер
    count = 1
    while count in existing_numbers:
        count += 1

    return count


# Функция для перемещения всех файлов
def move_all_files():
    files = os.listdir(source_folder)

    for file_name in files:
        source_path = source_folder / file_name

        # Проверяем, является ли объект файлом и имеет ли расширение .jpg
        if source_path.is_file() and source_path.suffix.lower() == ".jpg":
            # Получаем следующий порядковый номер
            count = get_next_count(base_number)

            # Формируем новое имя файла
            new_file_name = f"{file_prefix}{base_number}_{count:02d}.jpg"
            destination_path = destination_folder / new_file_name

            # Проверяем, существует ли файл с таким именем (на случай ошибок)
            if not destination_path.exists():
                # Перемещаем файл
                shutil.move(str(source_path), str(destination_path))
                print(f"Moved and renamed: {file_name} -> {new_file_name}")
            else:
                print(f"File already exists: {new_file_name}, skipping.")


# Основной цикл
while True:
    # Проверяем, есть ли команда в консоли
    if msvcrt.kbhit():
        command = input().strip()
        if command == "move_all":
            print("Moving all files...")
            move_all_files()
            continue

    # Получаем список файлов в исходной папке
    files = os.listdir(source_folder)

    for file_name in files:
        source_path = source_folder / file_name

        # Проверяем, является ли объект файлом и имеет ли расширение .jpg
        if source_path.is_file() and source_path.suffix.lower() == ".jpg":
            # Проверяем, был ли файл создан после запуска скрипта
            file_creation_time = source_path.stat().st_ctime
            if file_creation_time > script_start_time:
                # Получаем следующий порядковый номер
                count = get_next_count(base_number)

                # Формируем новое имя файла
                new_file_name = f"{file_prefix}{base_number}_{count:02d}.jpg"
                destination_path = destination_folder / new_file_name

                # Проверяем, существует ли файл с таким именем (на случай ошибок)
                if not destination_path.exists():
                    # Перемещаем файл
                    shutil.move(str(source_path), str(destination_path))
                    print(f"Moved and renamed: {file_name} -> {new_file_name}")
                else:
                    print(f"File already exists: {new_file_name}, skipping.")

    time.sleep(1)
