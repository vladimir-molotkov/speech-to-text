import os

import whisper


class AudioTranscriber:
    """
    A class for transcribing MP3 audio files using Whisper.
    """

    def __init__(self, model_size: str = "turbo", language: str = "ru"):
        """
        Initialize the transcriber with a Whisper model.

        Args:
            model_size (str): The size of the Whisper model. Options: 'tiny', 'base',
                              'small', 'medium', 'large', 'turbo'.
            language (str): The language code of the audio. Example: 'ru' for Russian.
        """
        self.model_size = model_size
        self.language = language

        print(f"Loading the '{self.model_size}' model for {self.language}...")
        self.model = whisper.load_model(self.model_size)

    def transcribe(self, mp3_file_path: str, transcription_file_path: str) -> str:
        """
        Transcribe an MP3 file to text.

        Args:
            mp3_file_path (str): Path to the MP3 file.

        Returns:
            str: The transcription text.
        """
        if not os.path.exists(mp3_file_path):
            raise FileNotFoundError(f"File not found: {mp3_file_path}")

        print("Transcribing audio. This may take a while...")
        result = self.model.transcribe(
            mp3_file_path, language=self.language, fp16=False, verbose=True
        )  # fp16=False for Mac CPU

        transcription_text = result["text"]

        # print("\n--- Transcription Result ---")
        # print(transcription_text[:100])

        with open(transcription_file_path, "w", encoding="utf-8") as f:
            f.write(transcription_text)

        print(f"\nTranscription saved to: {transcription_file_path}")
