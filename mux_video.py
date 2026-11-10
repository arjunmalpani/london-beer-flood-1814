import subprocess
import os

video_in = r"C:\Users\st\.gemini\antigravity\scratch\london-beer-flood\out\beer_flood\video.mp4"
audio_in = r"C:\Users\st\.gemini\antigravity\scratch\london-beer-flood\audio\mix.wav"
final_out = r"C:\Users\st\.gemini\antigravity\scratch\london-beer-flood\out\beer_flood\final_beer_flood_1814.mp4"

if not os.path.exists(video_in):
    raise FileNotFoundError(f"Video input not found: {video_in}")

cmd = [
    "ffmpeg", "-y",
    "-i", video_in,
    "-i", audio_in,
    "-map", "0:v:0",
    "-map", "1:a:0",
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "320k",
    final_out
]

print("Muxing video with master audio mix...")
subprocess.run(cmd, check=True)
print(f"Successfully generated: {final_out}")
