import os

import requests

# Конфигурация
API_KEY = os.environ.get("YANDEX_API_KEY")
if not API_KEY:
    raise RuntimeError("YANDEX_API_KEY is not set")

FOLDER_ID = os.environ.get("YANDEX_CATALOG")
if not FOLDER_ID:
    raise RuntimeError("YANDEX_CATALOG is not set")


MODEL_URI = f"gpt://{FOLDER_ID}/gpt-oss-120b/latest"
URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

# Чтение текста из файла
with open("/Users/vladimir/lec1_transcription.txt", "r", encoding="utf-8") as file:
    text = file.read()


# Функция для суммаризации текста
def summarize_text(full_text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}",
    }

    prompt = {
        "modelUri": MODEL_URI,
        "completionOptions": {"stream": False, "temperature": 0.3, "maxTokens": 1000},
        "messages": [
            {
                "role": "system",
                "text": "Вы профессиональный ассистент для суммаризации лекций по Истории Античности в университете. Создайте краткое содержание на русском языке, выделяя ключевые идеи и тезисы. Ответ должен быть четким и структурированным.",
            },
            {
                "role": "user",
                "text": f"Кратко суммируйте следующий текст, выделите основные тезисы и ключевые моменты:\n\n{full_text}",
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


if __name__ == "__main__":
    print("Начало суммаризации...")
    final_summary = summarize_text(text)

    # Сохранение результата
    with open("/Users/vladimir/summary.txt", "w", encoding="utf-8") as output_file:
        output_file.write(final_summary)

    print("Суммаризация завершена успешно!")
    print(f"Размер исходного текста: {len(text)} символов")
    print(f"Размер суммаризации: {len(final_summary)} символов")
    print("Результат сохранен в файл 'summary.txt'")
