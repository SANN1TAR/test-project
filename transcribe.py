# Транскрибирует MP4 вебинар и выдаёт поминутную разбивку что где говорилось
# Вход: путь к MP4 файлу
# Выход: .txt файл рядом с видео

import os
import sys
from faster_whisper import WhisperModel

def transcribe(video_path):
    if not os.path.exists(video_path):
        print(f"Файл не найден: {video_path}")
        return

    print("Загружаю модель... (первый раз скачает ~500 МБ, потом быстро)")
    model = WhisperModel("small", device="cpu", compute_type="int8")

    print("Распознаю речь, жди...")
    segments, info = model.transcribe(video_path, language="ru", beam_size=5)

    print(f"Язык определён: {info.language}, длина: {info.duration:.0f} сек")

    minutes = {}
    for segment in segments:
        minute = int(segment.start // 60)
        if minute not in minutes:
            minutes[minute] = []
        minutes[minute].append(segment.text.strip())

    output_path = os.path.splitext(video_path)[0] + "_таймкоды.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        for minute in sorted(minutes.keys()):
            timestamp = f"[{minute:02d}:{0:02d}]"
            text = " ".join(minutes[minute])
            f.write(f"{timestamp} — {text}\n\n")

    print(f"\nГотово! Файл сохранён: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_path = " ".join(sys.argv[1:])
    else:
        video_path = input("Перетащи MP4 файл сюда и нажми Enter: ").strip().strip('"')

    transcribe(video_path)
