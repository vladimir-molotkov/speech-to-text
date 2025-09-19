import os

import requests


class TextSummarizer:
    def __init__(self):
        # Читаем ключи из окружения
        self.api_key = os.environ.get("YANDEX_API_KEY")
        if not self.api_key:
            raise RuntimeError("YANDEX_API_KEY is not set")

        self.folder_id = os.environ.get("YANDEX_CATALOG")
        if not self.folder_id:
            raise RuntimeError("YANDEX_CATALOG is not set")

        self.model_uri = f"gpt://{self.folder_id}/yandexgpt"
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    def _summarize_text(self, full_text: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}",
        }

        prompt = {
            "modelUri": self.model_uri,
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,
                "maxTokens": None,
            },
            "messages": [
                {
                    "role": "system",
                    "text": (
                        "Вы профессиональный ассистент для суммаризации лекций по Истории Античности "
                        "в университете. Создайте содержание на русском языке, выделяя ключевые идеи и тезисы, "
                        "но сохраняя подробную информацию всех о фактах и понятиях. Ответ должен быть четким и "
                        "структурированным и подробным"
                    ),
                },
                {
                    "role": "user",
                    "text": f"Cуммируйте подробно следующий текст, верните ответ в формате markdown:\n\n{full_text}",
                },
            ],
        }

        print("Отправка запроса на суммаризацию...")
        response = requests.post(self.url, headers=headers, json=prompt)

        if response.status_code == 200:
            result = response.json()
            return result["result"]["alternatives"][0]["message"]["text"]
        else:
            print(f"Ошибка API: {response.status_code}")
            print(f"Ответ сервера: {response.text}")
            raise Exception(f"Ошибка при выполнении запроса: {response.status_code}")

    def process_file(self, source_file_path: str, target_file_path: str):
        # Чтение исходного текста
        with open(source_file_path, "r", encoding="utf-8") as file:
            text = file.read()

        print("Summarization started ...")
        final_summary = self._summarize_text(text)

        # Запись результата
        with open(target_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(final_summary)

        print("Summarization completed successfully!")
        print(f"Original text length: {len(text)} characters")
        print(f"Summary length: {len(final_summary)} characters")
        print(f"Result saved to file: {target_file_path}")
