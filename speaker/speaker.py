from gtts import gTTS
import pygame
import tempfile
import os

def main():
    text = "Привет! Как дела?"

    # Создание объекта gTTS
    tts = gTTS(text=text, lang='ru')

    # Используем временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        tts.save(temp_file.name)
        temp_file_path = temp_file.name

    try:
        # Инициализация pygame
        pygame.mixer.init()
        pygame.mixer.music.load(temp_file_path)
        pygame.mixer.music.play()

        # Ожидание окончания воспроизведения
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        # Удаление временного файла после воспроизведения
        os.remove(temp_file_path)

if __name__ == '__main__':
    main()
