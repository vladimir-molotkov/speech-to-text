from scripts.audio_from_video import AudioExtractor
from scripts.speech_to_text import AudioTranscriber
from scripts.text_summarization import TextSummarizer


def main(file_name=None):
    source_dir = "/Users/vladimir/Desktop/Материалы курса по античности"
    temp_dir = "/Users/vladimir/Desktop/Материалы курса по античности/temp"
    target_dir = "/Users/vladimir/Obsidian/Ancient_History"

    video_file_path = f"{source_dir}/{file_name}.mp4"
    audio_file_path = f"{temp_dir}/{file_name}.mp3"
    transcription_file_path = f"{temp_dir}/{file_name}.txt"
    summary_file_path = f"{target_dir}/{file_name}.md"

    # Step 1: Extract audio from video file
    AudioExtractor.extract_audio(video_file_path, audio_file_path)

    # Step 2: Transcribe text from audio file to txt file
    transcriber = AudioTranscriber(model_size="turbo", language="ru")
    transcriber.transcribe_text(audio_file_path, transcription_file_path)

    # Step 3: Summarize text to markdown file
    summarizer = TextSummarizer(subject="по Истории Античности")
    summarizer.summazize_text(transcription_file_path, summary_file_path)

    print(f"All steps completed successfully for file {video_file_path}\n")


if __name__ == "__main__":
    main(file_name="Лекция 19")
