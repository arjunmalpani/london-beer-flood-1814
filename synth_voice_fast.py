import os
import sys
import json
import re
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy import signal
from kokoro_onnx import Kokoro

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

print("Loading Kokoro TTS...")
KDIR = Path(os.path.expanduser('~/.faceless-shorts/kokoro'))
k = Kokoro(str(KDIR / 'kokoro-v1.0.onnx'), str(KDIR / 'voices-v1.0.bin'))

SR_IN = 24000
audio_pieces = []
lines_info = []

# Initial short lead-in silence (0.35s)
lead_s = 0.35
audio_pieces.append(np.zeros(int(SR_IN * lead_s), dtype=np.float32))
current_time = lead_s

for i, line in enumerate(SCRIPT_LINES):
    samples, _ = k.create(line, voice="bm_george", speed=1.35, lang="en-gb")
    # trim leading/trailing absolute silence
    abs_samples = np.abs(samples)
    thresh = 0.012 * np.max(abs_samples)
    s_idx = 0
    while s_idx < len(samples) and abs_samples[s_idx] < thresh:
        s_idx += 1
    e_idx = len(samples)
    while e_idx > s_idx and abs_samples[e_idx - 1] < thresh:
        e_idx -= 1
    trimmed = samples[max(0, s_idx - 150):min(len(samples), e_idx + 150)]
    
    line_duration = len(trimmed) / SR_IN
    t_start = current_time
    t_end = t_start + line_duration
    lines_info.append({
        "line_index": i,
        "text": line,
        "start": t_start,
        "end": t_end
    })
    
    audio_pieces.append(trimmed)
    current_time = t_end
    
    # Gap between lines:
    gap = 0.30
    if i in [0, 2, 7, 9, 11]:
        gap = 0.45
    audio_pieces.append(np.zeros(int(SR_IN * gap), dtype=np.float32))
    current_time += gap

full_audio_24k = np.concatenate(audio_pieces)

# Resample to 48000 Hz
SR_OUT = 48000
num_out = int(len(full_audio_24k) * SR_OUT / SR_IN)
full_audio_48k = signal.resample(full_audio_24k, num_out)

# Normalize
peak = np.max(np.abs(full_audio_48k))
if peak > 0:
    full_audio_48k = full_audio_48k * (0.88 / peak)

wavfile.write(str(WAV_PATH), SR_OUT, (full_audio_48k * 32767).astype(np.int16))

total_dur = len(full_audio_48k) / SR_OUT
total_frames = int(round(total_dur * 30))

print(f"Total voice duration: {total_dur:.2f} seconds ({total_frames} frames at 30 fps)")

# Spread words accurately within each line's exact measured time bounds
norm = lambda w: re.sub(r'[^a-zA-Z0-9]+', '', w)
all_words = []

for line in lines_info:
    tokens = line["text"].split()
    clean_tokens = [t for t in tokens if norm(t)]
    # Weight each token by length + punctuation bonus
    weights = []
    for k_tok, t in enumerate(clean_tokens):
        w_len = len(norm(t))
        punct_bonus = 0.0
        if t.endswith(','):
            punct_bonus = 2.2
        elif re.search(r'[.?!—;:]$', t) and k_tok < len(clean_tokens) - 1:
            punct_bonus = 3.5
        weights.append(w_len + 2.0 + punct_bonus)
    
    tot_weight = sum(weights)
    span = line["end"] - line["start"]
    cur_t = line["start"]
    
    for t, wt in zip(clean_tokens, weights):
        dur = span * (wt / tot_weight)
        speak_dur = dur * 0.90
        w_start = cur_t
        w_end = cur_t + speak_dur
        all_words.append({
            "w": t,
            "start": round(w_start, 3),
            "end": round(w_end, 3),
            "start_frame": int(round(w_start * 30)),
            "end_frame": int(round(w_end * 30)),
            "line": line["line_index"]
        })
        cur_t += dur

words_output = {
    "total_seconds": round(total_dur, 3),
    "fps": 30,
    "total_frames": total_frames,
    "lines": lines_info,
    "words": all_words
}

with open(WORDS_PATH, "w", encoding="utf-8") as f:
    json.dump(words_output, f, indent=2)

print(f"Generated words.json with {len(all_words)} words across {len(lines_info)} lines.")
