from scripts.audio_from_video import AudioExtractor
from scripts.speech_to_text import AudioTranscriber
from scripts.text_summarization import TextSummarizer


def main():
    file_name = "Тестовая лекция"
    source_dir = "/Users/vladimir/Desktop/Материалы курса по античности"
    temp_dir = "/Users/vladimir/Desktop/Материалы курса по античности/temp"
    target_dir = "/Users/vladimir/Obsidian/Ancient_History"

    mp4_file_path = f"{source_dir}/{file_name}.mp4"
    mp3_file_path = f"{temp_dir}/{file_name}.mp3"
    transcription_file_path = f"{temp_dir}/{file_name}.txt"
    summary_file_path = f"{target_dir}/{file_name}.md"

    # Step 1: Convert MP4 → MP3
    AudioExtractor.mp4_to_mp3(mp4_file_path, mp3_file_path)

    # Step 2: Transcribe MP3 → TXT
    transcriber = AudioTranscriber(model_size="turbo", language="ru")
    transcriber.transcribe(mp3_file_path, transcription_file_path)

    # Step 3: Summarize TXT → Markdown
    summarizer = TextSummarizer()
    summarizer.process_file(transcription_file_path, summary_file_path)

    print(f"\n All steps completed successfully for file {mp4_file_path}")


if __name__ == "__main__":
    main()
