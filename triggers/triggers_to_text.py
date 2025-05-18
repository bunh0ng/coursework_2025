import os

def merge_sql_files_to_txt(input_directory, output_file):
    """
    Объединяет все SQL-файлы из директории и её поддиректорий в один текстовый файл.
    
    :param input_directory: Путь к директории с SQL-файлами
    :param output_file: Путь к результирующему TXT-файлу
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Рекурсивный поиск всех .sql файлов
        for root, _, files in os.walk(input_directory):
            for filename in files:
                if filename.lower().endswith('.sql'):
                    filepath = os.path.join(root, filename)
                    
                    # Добавляем разделитель с именем файла
                    outfile.write(f"\n\n--- Файл: {filepath} ---\n\n")
                    
                    # Читаем и записываем содержимое SQL-файла
                    with open(filepath, 'r', encoding='utf-8') as sqlfile:
                        outfile.write(sqlfile.read())
    
    print(f"Объединено SQL-файлов из {input_directory} в {output_file}")

# Пример использования
if __name__ == "__main__":
    # Укажите путь к папке с SQL-файлами
    input_dir = "./triggers"
    
    # Укажите путь к результирующему файлу
    output_txt = "./all_triggers.txt"
    
    merge_sql_files_to_txt(input_dir, output_txt)