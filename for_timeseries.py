from scripts.audio_from_video import AudioExtractor
from scripts.speech_to_text import AudioTranscriber
from scripts.text_summarization import TextSummarizer


def main(file_name=None):
    # 02_Стационарность_S02
    file_name = "01_Первое_занятие_S01"
    source_dir = "/Users/vladimir/Desktop"
    temp_dir = "/Users/vladimir/speech-to-text/temp/timeseries"
    target_dir = "/Users/vladimir/Obsidian/Timeseries"

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
    summarizer = TextSummarizer()
    summarizer.summazize_text(transcription_file_path, summary_file_path)

    print(f"All steps completed successfully for file {audio_file_path}\n")


if __name__ == "__main__":
    main()
