import os
import wave
import struct
import math

def write_wav(filename, samples, sample_rate=44100):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)        # Mono
        wf.setsampwidth(2)       # 16-bit
        wf.setframerate(sample_rate)
        buffer = bytearray()
        for sample in samples:
            clamped = max(-1.0, min(1.0, sample))
            ival = int(clamped * 32767)
            buffer += struct.pack("<h", ival)
        wf.writeframes(buffer)

def generate_all_sounds(target_dir):
    os.makedirs(target_dir, exist_ok=True)
    sr = 44100

    # 1. Jump Sound: punchy upward chirp (220Hz -> 520Hz over 0.14s)
    dur_jump = 0.14
    n_jump = int(sr * dur_jump)
    jump_samples = []
    for i in range(n_jump):
        t = i / sr
        p = t / dur_jump
        freq = 220 + (520 - 220) * (p ** 1.2)
        env = (1.0 - p) ** 0.7
        val = 0.75 * math.sin(2 * math.pi * freq * t) + 0.25 * math.sin(4 * math.pi * freq * t)
        jump_samples.append(val * env)
    write_wav(os.path.join(target_dir, "jump.wav"), jump_samples, sr)

    # 2. Score Sound: bright two-tone chime (523Hz (C5) for 0.07s then 784Hz (G5) for 0.12s)
    dur_score = 0.19
    n_score = int(sr * dur_score)
    score_samples = []
    t_split = 0.07
    for i in range(n_score):
        t = i / sr
        if t < t_split:
            freq = 523.25
            env = 1.0 - (t / t_split) * 0.3
        else:
            freq = 783.99
            rem = (t - t_split) / (dur_score - t_split)
            env = 1.0 - rem
        val = 0.8 * math.sin(2 * math.pi * freq * t) + 0.2 * math.sin(4 * math.pi * freq * t)
        score_samples.append(val * env)
    write_wav(os.path.join(target_dir, "score.wav"), score_samples, sr)

    # 3. Hit / Crash Sound: heavy low thud with distortion (200Hz down to 40Hz over 0.3s)
    dur_hit = 0.3
    n_hit = int(sr * dur_hit)
    hit_samples = []
    for i in range(n_hit):
        t = i / sr
        p = t / dur_hit
        freq = max(35.0, 200.0 * ((1.0 - p) ** 2.0))
        env = (1.0 - p) ** 0.5
        raw = math.sin(2 * math.pi * freq * t)
        distorted = math.copysign(min(1.0, abs(raw) * 1.6), raw)
        hit_samples.append(distorted * env * 0.85)
    write_wav(os.path.join(target_dir, "hit.wav"), hit_samples, sr)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    generate_all_sounds(current_dir)
    print("Sound effects successfully generated in:", current_dir)
