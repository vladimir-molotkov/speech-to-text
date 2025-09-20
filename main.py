from scripts.audio_from_video import AudioExtractor
from scripts.speech_to_text import AudioTranscriber
from scripts.text_summarization import TextSummarizer


def main(file_name=None):
    # file_name = "Занятие 2"
    source_dir = "/Users/vladimir/Desktop/Материалы курса по античности"
    temp_dir = "/Users/vladimir/Desktop/Материалы курса по античности/temp"
    target_dir = "/Users/vladimir/Obsidian/Roman_law"

    video_file_path = f"{source_dir}/{file_name}.mp4"
    audio_file_path = f"{temp_dir}/{file_name}.mp3"
    transcription_file_path = f"{temp_dir}/{file_name}.txt"
    summary_file_path = f"{target_dir}/{file_name}.md"

    # Step 1: Convert MP4 → MP3
    AudioExtractor.mp4_to_mp3(video_file_path, audio_file_path)

    # Step 2: Transcribe MP3 → TXT
    transcriber = AudioTranscriber(model_size="turbo", language="ru")
    transcriber.transcribe(audio_file_path, transcription_file_path)

    # Step 3: Summarize TXT → Markdown
    summarizer = TextSummarizer()
    summarizer.process_file(transcription_file_path, summary_file_path)

    print(f"\n All steps completed successfully for file {video_file_path}")


if __name__ == "__main__":
    lectures_to_convert = [f"Лекция {i}" for i in range(1, 19)] + ["Лекция 20"]
    for file in lectures_to_convert:
        main(file_name=file)
