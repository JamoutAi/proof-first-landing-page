#!/usr/bin/env python3
"""Turn a video into a WebVTT caption file using faster-whisper word timestamps.

usage: python3 make_vtt.py clip.mp4 [--model small.en] > clip.vtt
Cues break at punctuation, about 8 words, or 3.2 seconds. Always read the
result: speech recognition mishears openings, names and brand words.
Needs: pip install faster-whisper
"""
import argparse
import re

from faster_whisper import WhisperModel


def stamp(t):
    m = int(t // 60)
    return f"{m:02d}:{t - 60 * m:06.3f}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("--model", default="small.en")
    p.add_argument("--max-words", type=int, default=8)
    p.add_argument("--max-seconds", type=float, default=3.2)
    args = p.parse_args()

    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(args.video, word_timestamps=True, beam_size=5, vad_filter=True)
    words = [(w.start, w.end, w.word.strip()) for s in segments for w in s.words]

    cues, cur = [], []
    for i, (start, end, word) in enumerate(words):
        cur.append((start, end, word))
        long_enough = len(cur) >= args.max_words or (cur[-1][1] - cur[0][0]) > args.max_seconds
        sentence_end = word.endswith((".", "?", "!", ",")) and len(cur) >= 4
        if long_enough or sentence_end or i == len(words) - 1:
            cues.append(cur)
            cur = []

    print("WEBVTT\n")
    for i, cue in enumerate(cues):
        end = cue[-1][1] + 0.25                      # linger a moment after the last word...
        if i + 1 < len(cues):
            end = min(end, cues[i + 1][0][0] - 0.02)  # ...but never overlap the next cue
        print(f"{stamp(cue[0][0])} --> {stamp(max(end, cue[-1][1]))}")
        # whisper sometimes splits hyphenated words ("co -opting"); rejoin them
        print(re.sub(r" -(?=\w)", "-", " ".join(w for _, _, w in cue)))
        print()


if __name__ == "__main__":
    main()
