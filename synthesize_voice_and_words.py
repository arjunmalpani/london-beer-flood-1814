import os
import sys
import json
import re
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy import signal
from kokoro_onnx import Kokoro
from faster_whisper import WhisperModel

# Output paths
OUT_DIR = Path(r"C:\Users\st\.gemini\antigravity\scratch\london-beer-flood\voice")
OUT_DIR.mkdir(parents=True, exist_ok=True)
WAV_PATH = OUT_DIR / "voice.wav"
WORDS_PATH = OUT_DIR / "words.json"

SCRIPT_LINES = [
    "Over a million pints of beer once tore through London in a fifteen-foot tidal wave.",
    "It's 1814, and the Horse Shoe Brewery just finished its pride and joy: a fermentation tank the size of a three-story house.",
    "Twenty-two feet of solid oak, clamped together by twenty-nine massive iron hoops.",
    "At four o'clock, a warehouse clerk notices a seven-hundred-pound iron ring has fallen off.",
    "His boss tells him not to worry—rings slip all the time, just leave a note to fix it later.",
    "Inside, thirty-five hundred barrels of dark porter are fermenting, building up pressure like a giant shaken soda bottle.",
    "With one ring gone, the rest have to carry the load.",
    "They start creaking, stretching, and bulging.",
    "Then the bottom ring snaps like a cannon shot, the oak walls blow out, and the shockwave ruptures three more vats.",
    "A three-hundred-thousand-gallon tidal wave of beer blasts through the brick wall into the street.",
    "Luckily, the streets were flooded with free beer.",
    "Unluckily, the wave was fifteen feet tall and moving at thirty miles an hour.",
    "Locals rushed outside with pots, kettles, and teacups, scooping up pints straight from the road.",
    "In court, a judge officially ruled the flood an 'Act of God', and Parliament even gave the brewery a tax refund for the lost alcohol.",
    "It ended giant wooden vats forever, forcing breweries to switch to steel.",
    "So if you ever see a seven-hundred-pound metal ring pop off a barrel, maybe don't just leave a note."
]

print("1. Loading Kokoro TTS...")
KDIR = Path(os.path.expanduser('~/.faceless-shorts/kokoro'))
k = Kokoro(str(KDIR / 'kokoro-v1.0.onnx'), str(KDIR / 'voices-v1.0.bin'))

# Synthesize all lines
audio_pieces = []
SR_IN = 24000
pause_lead = np.zeros(int(SR_IN * 0.4), dtype=np.float32)
audio_pieces.append(pause_lead)

for i, line in enumerate(SCRIPT_LINES):
    print(f"  Synthesizing line {i+1}/{len(SCRIPT_LINES)}: {line[:40]}...")
    samples, _ = k.create(line, voice="bm_george", speed=1.04, lang="en-gb")
    # trim silence at start/end
    abs_samples = np.abs(samples)
    thresh = 0.01 * np.max(abs_samples)
    start_idx = 0
    while start_idx < len(samples) and abs_samples[start_idx] < thresh:
        start_idx += 1
    end_idx = len(samples)
    while end_idx > start_idx and abs_samples[end_idx - 1] < thresh:
        end_idx -= 1
    trimmed = samples[max(0, start_idx - 200):min(len(samples), end_idx + 200)]
    audio_pieces.append(trimmed)
    
    # Gap between sentences: 0.32s
    gap_duration = 0.32
    if i in [0, 2, 7, 9, 11]:  # major beat transitions get slightly longer breathing pause
        gap_duration = 0.45
    audio_pieces.append(np.zeros(int(SR_IN * gap_duration), dtype=np.float32))

full_audio_24k = np.concatenate(audio_pieces)

# Resample to 48000 Hz for Remotion audio pipeline
SR_OUT = 48000
num_out_samples = int(len(full_audio_24k) * SR_OUT / SR_IN)
full_audio_48k = signal.resample(full_audio_24k, num_out_samples)

# Normalize to -1 dB peak
peak = np.max(np.abs(full_audio_48k))
if peak > 0:
    full_audio_48k = full_audio_48k * (0.89 / peak)

# Save WAV
wavfile.write(str(WAV_PATH), SR_OUT, (full_audio_48k * 32767).astype(np.int16))
duration_sec = len(full_audio_48k) / SR_OUT
total_frames = int(round(duration_sec * 30))
print(f"Saved voice.wav: {duration_sec:.2f} seconds ({total_frames} frames at 30 fps)")

print("2. Extracting word timestamps with faster-whisper...")
model = WhisperModel("base.en", device="cpu", compute_type="int8")
segments, info = model.transcribe(str(WAV_PATH), word_timestamps=True)

words_list = []
for segment in segments:
    for word in segment.words:
        clean_w = word.word.strip()
        words_list.append({
            "w": clean_w,
            "start": round(word.start, 3),
            "end": round(word.end, 3),
            "start_frame": int(round(word.start * 30)),
            "end_frame": int(round(word.end * 30))
        })

with open(WORDS_PATH, "w", encoding="utf-8") as f:
    json.dump({
        "duration": duration_sec,
        "fps": 30,
        "total_frames": total_frames,
        "words": words_list
    }, f, indent=2)

print(f"Saved words.json with {len(words_list)} words.")
