import re
from striprtf.striprtf import rtf_to_text  # For reading RTF files / Для чтения RTF файлов

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
def process_string(string, valid_urls, invalid_urls):
    string = string.strip()
    # Replace delimiters with spaces
    # Заменяем разделители на пробелы
    string = string.replace(',', ' ')
    string = string.replace(';', ' ')
    string = string.replace('http', ' http')  # Add space before "http" for proper splitting / Добавляем пробел перед "http" для корректного разделения
    split_strings = string.split(' ')  # Split the line into parts / Разбиваем строку на части

    for url in split_strings:
        if not url:
            continue
        if not is_valid_url(url):
            continue

        # Normalize links to https and replace mobile versions of sites
        # Приводим ссылки к https и заменяем мобильные версии сайтов
        url = url.replace('http:', 'https:')
        url = url.replace('m.ok.ru', 'ok.ru')
        url = url.replace('m.vk.com', 'vk.com')
        url = url.replace('vk.ru', 'vk.com')  # Replace vk.ru with vk.com / Заменяем vk.ru на vk.com

        # Check social networks and normalize the format
        # Проверяем соцсети и приводим к формату
        if "vk.com" in url:
            processed_url = normalize_vk_url(url)
            if processed_url:
                valid_urls.append(processed_url)
            else:
                invalid_urls.append(url)
        elif url.startswith("https://ok.ru/"):
            valid_urls.append("https://ok.ru/")
        elif url.startswith("https://t.me/"):
            valid_urls.append("https://t.me/")
        else:
            invalid_urls.append(url)


# Function to read the file and process URLs
# Функция для чтения файла и обработки ссылок
def handle_file(filepath, valid_urls, invalid_urls):
    with open(filepath, "r", encoding='UTF-8') as file:
        if filepath.endswith(".rtf"):
            content = file.read()
            content = rtf_to_text(content)  # Convert RTF to text / Преобразуем RTF в текст
        else:
            content = file.read()

        lines = content.splitlines()  # Split content into lines / Разделяем текст на строки
        for line in lines:
            process_string(line, valid_urls, invalid_urls)


# Main lists for valid and invalid URLs
# Основные списки для корректных и некорректных ссылок
valid_urls = []
invalid_urls = []

# List of files to process
# Список файлов для обработки
files_to_process = ["file_1_rtf.rtf", "file_1_txt.txt", "file_2_rtf.rtf", "file_2_txt.txt"]

# Processing each file in the list
# Обработка каждого файла в списке
for filepath in files_to_process:
    print(f"Processing file: {filepath}")
    handle_file(filepath, valid_urls, invalid_urls)

# Remove duplicates and sort URLs
# Удаляем дубликаты и сортируем ссылки
valid_urls = sorted(set(valid_urls))

# Save valid URLs to result.txt
# Запись корректных ссылок в файл result.txt
with open("result.txt", "w", encoding='UTF-8') as result_file:
    for url in valid_urls:
        result_file.write(url + "\n")
        print(f"Recorded valid URL: {url}")

# Save invalid URLs to error.txt
# Запись некорректных ссылок в файл error.txt
with open("error.txt", "w", encoding='UTF-8') as error_file:
    for url in invalid_urls:
        error_file.write(url + "\n")
        print(f"Recorded invalid URL: {url}")
