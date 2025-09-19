import os
import subprocess


class AudioExtractor:
    """Handles audio extraction from video using ffmpeg."""

    @staticmethod
    def mp4_to_mp3(mp4_path: str, mp3_path: str):
        print(f"Converting {mp4_path} → {mp3_path} ...")

        os.makedirs(os.path.dirname(mp3_path), exist_ok=True)

        subprocess.run(
            ["ffmpeg", "-y", "-i", mp4_path, mp3_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        print("Conversion finished.")
