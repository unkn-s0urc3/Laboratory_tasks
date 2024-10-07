import re
import json
from striprtf.striprtf import rtf_to_text  # For reading RTF files / Для чтения RTF файлов
from collections import defaultdict

# Function to check the basic validity of a URL
# Функция для проверки базовой корректности URL
def is_valid_url(string):
    if not ("https://" in string or "http://" in string):
        return False
    if not (".com" in string or ".ru" in string or ".me" in string):
        return False
    return True

# Function to normalize VK links to the required format
# Функция для приведения ссылок VK к нужному формату
def normalize_vk_url(url):
    # Example link: https://vk.com/wall-123456_654321
    # Пример ссылки: https://vk.com/wall-123456_654321
    vk_post_pattern = r'https://vk\.com/wall(-?\d+)_(\d+)'
    match = re.match(vk_post_pattern, url)

    if match:
        community_id = match.group(1)
        post_id = match.group(2)
        return f'https://vk.com/wall{community_id}_{post_id}'

    # Normalize other VK URLs like vk.ru to vk.com
    # Приводим ссылки вида vk.ru к vk.com
    if url.startswith("https://vk.com"):
        return 'https://vk.com/'

    return None

# Function to process text data from a line
# Функция для обработки текстовых данных из строки
def process_string(string, valid_urls):
    string = string.strip().replace(',', ' ').replace(';', ' ')
    string = string.replace('http', ' http')  # Add space before "http" for proper splitting / Добавляем пробел перед "http" для корректного разделения
    split_strings = string.split(' ')  # Split the line into parts / Разбиваем строку на части

    for url in split_strings:
        if not url:
            continue
        if not is_valid_url(url):
            continue

        # Normalize links to https and replace mobile versions of sites
        # Приводим ссылки к https и заменяем мобильные версии сайтов
        url = url.replace('http:', 'https:').replace('m.ok.ru', 'ok.ru').replace('m.vk.com', 'vk.com').replace('vk.ru', 'vk.com')

        if "vk.com" in url:
            processed_url = normalize_vk_url(url)
            if processed_url:
                valid_urls.add(processed_url)

# Function to read the file and process URLs
# Функция для чтения файла и обработки ссылок
def handle_file(filepath, valid_urls):
    with open(filepath, "r", encoding='UTF-8') as file:
        if filepath.endswith(".rtf"):
            content = file.read()
            content = rtf_to_text(content)  # Convert RTF to text / Преобразуем RTF в текст
        else:
            content = file.read()

        lines = content.splitlines()  # Split content into lines / Разделяем текст на строки
        for line in lines:
            process_string(line, valid_urls)

# Function to get the ministry number based on the URL
# Получение номера министерства
def get_ministry_number(url):
    remainder = sum(ord(char) for char in url) % 100
    return remainder

# Main set for valid URLs
# Основной набор для корректных ссылок
valid_urls = set()

# List of files to process
# Список файлов для обработки
files_to_process = ["file_1_rtf.rtf", "file_1_txt.txt", "file_2_rtf.rtf", "file_2_txt.txt"]

# Processing each file in the list
# Обработка каждого файла в списке
for filepath in files_to_process:
    print(f"Processing file: {filepath}")
    handle_file(filepath, valid_urls)

# Grouping URLs by ministry
# Группировка ссылок по министерствам
ministries = defaultdict(set)
for url in valid_urls:
    ministry_number = get_ministry_number(url)
    ministries[ministry_number].add(url)

# Saving results to JSON
# Сохранение в JSON
with open("ministries.json", "w", encoding='UTF-8') as json_file:
    json.dump({k: list(v) for k, v in ministries.items()}, json_file, ensure_ascii=False)

# Output the number of links per ministry
# Вывод количества ссылок по министерствам
ministry_counts = {k: len(v) for k, v in ministries.items()}
sorted_ministry_counts = sorted(ministry_counts.items(), key=lambda item: item[1], reverse=True)

print("\nМинистерства и количество ссылок:")
for ministry, count in sorted_ministry_counts:
    print(f"Министерство {ministry}: {count} ссылок")

# Top 10% ministries
# 10% лидеров
top_10_percent = int(len(sorted_ministry_counts) * 0.1)
top_leaders = sorted_ministry_counts[:top_10_percent]

print("\n10% лидеров с максимальным числом ссылок:")
for ministry, count in top_leaders:
    print(f"Министерство {ministry}: {count} ссылок")

# Bottom 10% ministries
# 10% антилидеров
bottom_10_percent = int(len(sorted_ministry_counts) * 0.1)
bottom_leaders = sorted_ministry_counts[-bottom_10_percent:]

print("\n10% антилидеров с наименьшим числом ссылок:")
for ministry, count in bottom_leaders:
    print(f"Министерство {ministry}: {count} ссылок")