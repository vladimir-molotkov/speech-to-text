import os
import subprocess


class AudioExtractor:
    """Handles audio extraction from video using ffmpeg."""

    @staticmethod
    def extract_audio(video_path: str, audio_path: str):
        print(f"Converting {video_path} → {audio_path} ...")

        os.makedirs(os.path.dirname(audio_path), exist_ok=True)

        subprocess.run(
            ["ffmpeg", "-y", "-i", video_path, audio_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        print("Conversion finished.")
