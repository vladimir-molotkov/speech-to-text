import whisper
import fire

def transcribe_mp3(mp3_filepath="/Users/vladimir/lec1.mp3", model_size="turbo", language="ru"):
    """
    Transcribes an MP3 file to text using Whisper.

    Args:
        mp3_filepath (str): The path to the MP3 file.
        model_size (str): The size of the Whisper model. Options: 'tiny', 'base', 'small', 'medium', 'large'. Larger models are more accurate but slower.
        language (str): The language code of the audio. 'ru' for Russian.
    """
    
    print(f"Loading the '{model_size}' model for {language}...")
    model = whisper.load_model(model_size)
    
    
    print("Transcribing audio. This may take a while...")
    result = model.transcribe(mp3_filepath, language=language, fp16=False, verbose=True) # fp16=False is best for Mac CPU

    print("\n--- Transcription Result ---")
    print(result["text"])
    

    text_filename = mp3_filepath.replace(".mp3", "_transcription.txt")
    with open(text_filename, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"\nTranscription saved to: {text_filename}")
    
    # (Optional) You can also access the segments with timestamps
    # for segment in result['segments']:
    #     print(f"[{segment['start']}s -> {segment['end']}s] {segment['text']}")


if __name__ == "__main__":
    fire.Fire(transcribe_mp3())
