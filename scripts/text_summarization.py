import os
import re

import requests


class TextSummarizer:
    def __init__(self, subject=""):
        self.subject = subject
        # Читаем ключи из окружения
        self.api_key = os.environ.get("YANDEX_API_KEY")
        if not self.api_key:
            raise RuntimeError("YANDEX_API_KEY is not set")

        self.folder_id = os.environ.get("YANDEX_CATALOG")
        if not self.folder_id:
            raise RuntimeError("YANDEX_CATALOG is not set")

        self.model_uri = f"gpt://{self.folder_id}/yandexgpt"
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    def _request_model(self, text: str, mode: str = "chunk") -> str:
        """Выполняет запрос к модели.
        mode = 'chunk' → обычное сжатие чанка
        mode = 'merge' → объединение всех частей без сокращения"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}",
        }

        if mode == "chunk":
            user_prompt = (
                "Уберите лишнюю информацию, но подробно сохраните все факты, описания, "
                "информацию о том, как жили люди, об известных личностях, о датах, событиях, понятиях и терминах "
                "Верните ответ в формате markdown:\n\n"
                f"{text}"
            )
        elif mode == "merge":
            user_prompt = (
                "У тебя есть несколько подробных конспектов. "
                "Объедини их в единый связный текст лекции, сохранив все факты, даты, личности, детали, понятия и термины "
                "Не сокращай и не удаляй важное. "
                "Просто оформи как цельный, хорошо структурированный конспект в формате markdown:\n\n"
                f"{text}"
            )
        else:
            raise ValueError("Unknown mode")

        prompt = {
            "modelUri": self.model_uri,
            "completionOptions": {
                "stream": False,
                "temperature": 0.2,
                "maxTokens": 10_000,
            },
            "messages": [
                {
                    "role": "system",
                    "text": (
                        f"Вы профессиональный ассистент для лекций {self.subject} "
                        "в университете. "
                        "Вы должны сохранять подробную информацию о датах, фактах и понятиях. "
                        "Ответ должен быть четким, структурированным и подробным."
                    ),
                },
                {"role": "user", "text": user_prompt},
            ],
        }

        response = requests.post(self.url, headers=headers, json=prompt)

        if response.status_code == 200:
            result = response.json()
            return result["result"]["alternatives"][0]["message"]["text"]
        else:
            print(f"API Error: {response.status_code}")
            print(f"Error: {response.text}")
            raise Exception(f"Error: {response.status_code}")

    def _split_text(self, text: str, max_chunk_size: int = 6000) -> list[str]:
        """Разделяет текст на чанки примерно по max_chunk_size,
        но только по границам предложений (точка/!?)."""
        sentences = re.split(r"(?<=[.!?])\s+", text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
                current_chunk += sentence + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + " "

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def summazize_text(self, source_file_path: str, target_file_path: str):
        # Чтение исходного текста
        with open(source_file_path, "r", encoding="utf-8") as file:
            text = file.read()

        print("Summarization started ...")
        parts = self._split_text(text, 10_000)

        summaries = []
        for idx, part in enumerate(parts, start=1):
            print(f"Summarizing part {idx}/{len(parts)} (length={len(part)} chars) ...")
            summary = self._request_model(part, mode="chunk")
            summaries.append(f"### Part {idx}\n{summary}\n")

        # Объединяем промежуточные результаты
        merged_text = "\n\n".join(summaries)

        print("Merging all parts into a final detailed summary ...")
        final_summary = self._request_model(merged_text, mode="merge")

        # Запись результата
        with open(target_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(final_summary)

        print("Summarization completed successfully!")
        print(f"Original text length: {len(text)} characters")
        print(f"Final summary length: {len(final_summary)} characters")
        print(f"Result saved to file: {target_file_path}")
