import os

import requests


# Функция для суммаризации текста
def summarize_text(API_KEY, MODEL_URI, URL, full_text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}",
    }

    prompt = {
        "modelUri": MODEL_URI,
        "completionOptions": {"stream": False, "temperature": 0.3, "maxTokens": None},
        "messages": [
            {
                "role": "system",
                "text": "Вы профессиональный ассистент для суммаризации лекций по Истории Античности в университете. Создайте содержание на русском языке, выделяя ключевые идеи и тезисы, но сохраняя подробную информацию о фактах и понятиях. Ответ должен быть четким и структурированным, не слишком кратким.",
            },
            {
                "role": "user",
                "text": f"Cуммируйте следующий текст, верните ответ в формате markdown:\n\n{full_text}",
            },
        ],
    }

    print("Отправка запроса на суммаризацию...")
    response = requests.post(URL, headers=headers, json=prompt)

    if response.status_code == 200:
        result = response.json()
        return result["result"]["alternatives"][0]["message"]["text"]
    else:
        print(f"Ошибка API: {response.status_code}")
        print(f"Ответ сервера: {response.text}")
        raise Exception(f"Ошибка при выполнении запроса: {response.status_code}")


def process_file():
    source_dir = "/Users/vladimir/"
    target_dir = "/Users/vladimir/Ancient history/"

    source_file = "lec1_transcription.txt"
    target_file = "lec1_summary.ms"
    # Конфигурация
    API_KEY = os.environ.get("YANDEX_API_KEY")
    if not API_KEY:
        raise RuntimeError("YANDEX_API_KEY is not set")

    FOLDER_ID = os.environ.get("YANDEX_CATALOG")
    if not FOLDER_ID:
        raise RuntimeError("YANDEX_CATALOG is not set")

    MODEL_URI = f"gpt://{FOLDER_ID}/yandexgpt"
    URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    # Чтение текста из файла
    with open(source_dir + source_file, "r", encoding="utf-8") as file:
        text = file.read()

    print("Начало суммаризации...")
    final_summary = summarize_text(API_KEY, MODEL_URI, URL, text)

    with open(target_dir + target_file, "w", encoding="utf-8") as output_file:
        output_file.write(final_summary)

    print("Суммаризация завершена успешно!")
    print(f"Размер исходного текста: {len(text)} символов")
    print(f"Размер суммаризации: {len(final_summary)} символов")
    print(f"Результат сохранен в файл {target_dir + target_file}")


if __name__ == "__main__":
    process_file()
