"""Generate the site's original, offline ambient loop.

Edit CHORDS or BELL_NOTES below to change the harmony/motif.
Requires Python 3 and NumPy. The public website itself needs no Python.
"""
from pathlib import Path
import wave
import numpy as np

OUT = Path(__file__).resolve().parents[1] / "assets" / "audio" / "strategy-ambient.wav"
SAMPLE_RATE = 22050
BARS = 12
SECONDS_PER_BAR = 3.0
DURATION = BARS * SECONDS_PER_BAR

# MIDI note numbers. This is an original minor-key progression, not an anime OST.
CHORDS = [
    [50, 53, 57, 60, 64],  # Dm9
    [46, 50, 53, 57],      # Bbmaj7
    [41, 45, 48, 55],      # Fadd9
    [48, 50, 55, 60],      # Csus2
    [43, 46, 50, 53],      # Gm7
    [45, 50, 52, 55],      # Dm/A color
    [46, 50, 53, 57],      # Bbmaj7
    [45, 50, 52, 55],      # Asus4 color
    [50, 53, 57, 60, 64],  # Dm9
    [41, 45, 48, 52],      # Fmaj7
    [43, 46, 50, 57],      # Gm9 color
    [50, 53, 57, 60, 64],  # Dm9, returns to the opening harmony
]
BASS_ROOTS = [38, 34, 29, 36, 31, 33, 34, 33, 38, 29, 31, 38]
# A sparse, soft bell motif. Times are relative to each 3-second bar.
BELL_NOTES = [74, 69, 72, 77, 76, 72, 69, 74, 76, 72, 69, 81,
              74, 77, 72, 69, 74, 76, 77, 69, 72, 74, 69, 81]
BELL_OFFSETS = [0.45, 1.72]


def hz(midi_note):
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))


def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    total = int(SAMPLE_RATE * DURATION)
    time = np.arange(total, dtype=np.float64) / SAMPLE_RATE
    left = np.zeros(total, dtype=np.float64)
    right = np.zeros(total, dtype=np.float64)
    bar_size = int(SAMPLE_RATE * SECONDS_PER_BAR)

    # Soft, slowly breathing chord pads with tiny stereo detuning.
    for bar, chord in enumerate(CHORDS):
        start = bar * bar_size
        end = min(total, start + bar_size)
        local = time[start:end] - bar * SECONDS_PER_BAR
        attack = smoothstep(local / 0.48)
        release = smoothstep((SECONDS_PER_BAR - local) / 0.72)
        envelope = attack * release
        breath = 0.82 + 0.18 * np.sin(2 * np.pi * 0.105 * time[start:end])
        count = len(chord)
        for index, note in enumerate(chord):
            frequency = hz(note)
            pan = (index / max(1, count - 1)) * 2.0 - 1.0
            tone_l = (np.sin(2*np.pi*frequency*0.998*time[start:end])
                      + 0.21*np.sin(2*np.pi*frequency*2.003*time[start:end] + 0.3))
            tone_r = (np.sin(2*np.pi*frequency*1.002*time[start:end] + 0.12)
                      + 0.18*np.sin(2*np.pi*frequency*1.997*time[start:end] + 0.7))
            gain = envelope * breath * (0.033 / count)
            left[start:end] += tone_l * gain * (0.83 - pan * 0.12)
            right[start:end] += tone_r * gain * (0.83 + pan * 0.12)

        # Warm sub-bass under the chord, softly pulsing rather than percussive.
        root = hz(BASS_ROOTS[bar])
        pulse = 0.68 + 0.32 * (0.5 + 0.5 * np.sin(2*np.pi*0.75*local - np.pi/2))
        bass = np.sin(2*np.pi*root*time[start:end]) * envelope * pulse * 0.045
        left[start:end] += bass
        right[start:end] += bass * 0.96

    # Gentle bell notes, with a warm harmonic and short stereo delay/reverb.
    note_index = 0
    for bar in range(BARS):
        for offset in BELL_OFFSETS:
            note = BELL_NOTES[note_index % len(BELL_NOTES)]
            note_index += 1
            start_time = bar * SECONDS_PER_BAR + offset
            start = int(start_time * SAMPLE_RATE)
            if start >= total:
                continue
            end = min(total, start + int(2.3 * SAMPLE_RATE))
            local = time[start:end] - start_time
            fade_in = smoothstep(local / 0.025)
            decay = np.exp(-local / 1.42) * fade_in
            frequency = hz(note)
            bell = (np.sin(2*np.pi*frequency*local)
                    + 0.24*np.sin(2*np.pi*frequency*2.72*local + 0.2)
                    + 0.08*np.sin(2*np.pi*frequency*4.08*local + 0.6))
            bell *= decay * 0.045
            pan = -0.42 if (bar + note_index) % 2 else 0.42
            left[start:end] += bell * (0.78 - pan * 0.25)
            right[start:end] += bell * (0.78 + pan * 0.25)

    # Small room reflections; the tail is deliberately quiet for a soft loop point.
    dry_left, dry_right = left.copy(), right.copy()
    delay_a, delay_b = int(.19*SAMPLE_RATE), int(.31*SAMPLE_RATE)
    left[delay_a:] += dry_right[:-delay_a] * .10
    right[delay_b:] += dry_left[:-delay_b] * .08

    # Smooth loop endpoints, then set a safe, gentle output level.
    fade_samples = int(.35 * SAMPLE_RATE)
    fade_in = smoothstep(np.arange(fade_samples) / fade_samples)
    fade_out = smoothstep(np.arange(fade_samples, 0, -1) / fade_samples)
    left[:fade_samples] *= fade_in
    right[:fade_samples] *= fade_in
    left[-fade_samples:] *= fade_out
    right[-fade_samples:] *= fade_out
    stereo = np.column_stack([left, right])
    peak = np.max(np.abs(stereo))
    if peak:
        stereo = stereo * (0.72 / peak)
    pcm = np.int16(np.clip(stereo, -1.0, 1.0) * 32767)

    with wave.open(str(OUT), 'wb') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(pcm.astype('<i2').tobytes())
    print(f'Created {OUT} ({DURATION:.0f}s, {SAMPLE_RATE}Hz stereo)')


if __name__ == '__main__':
    main()
