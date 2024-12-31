import os
import time
import shutil
from pathlib import Path

# Папка, которую нужно отслеживать
source_folder = Path("~/Downloads").expanduser()

# Папка, куда перемещать файлы
destination_folder = Path("../target_folder").resolve()

# Префикс имени файла
file_prefix = "test_"

# Начальное значение для номера (меняется вручную)
base_number = "00005"

# Время запуска скрипта
script_start_time = time.time()

# Создаем папку назначения, если её нет
destination_folder.mkdir(parents=True, exist_ok=True)

# Функция для получения следующего порядкового номера
def get_next_count(base_number):
    existing_files = os.listdir(destination_folder)
    max_count = 0
    for file in existing_files:
        if file.startswith(f"{file_prefix}{base_number}_") and file.endswith(".jpg"):
            parts = file[len(file_prefix):-4].split("_")
            if len(parts) == 2 and parts[1].isdigit():
                max_count = max(max_count, int(parts[1]))
    return max_count + 1

# Основной цикл
while True:
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

    # Ждем перед следующей проверкой
    time.sleep(1)
