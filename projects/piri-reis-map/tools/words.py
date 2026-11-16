"""Transcribe the narration with faster-whisper and spell the words as the script does.
Usage: python3 tools/words.py audio/vo_v1.mp3 audio/words.json"""
import difflib, json, re, sys
from faster_whisper import WhisperModel

audio, out = sys.argv[1], sys.argv[2]
script = open('script.md').read().split('## Spoken text (for the voiceover)')[1].strip().split('\n\n')[0]
sw = script.split()
m = WhisperModel('small.en', device='cpu', compute_type='int8')
import subprocess, numpy as np
pcm = np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',audio,'-f','s16le','-ac','1','-ar','16000','-'],capture_output=True).stdout, np.int16).astype(np.float32) / 32768
segs, _ = m.transcribe(pcm, word_timestamps=True)
hw = [w for s in segs for w in s.words]
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
sm = difflib.SequenceMatcher(None, [norm(x) for x in sw], [norm(w.word) for w in hw], autojunk=False)
times = [None] * len(sw)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal' or (tag == 'replace' and i2 - i1 == j2 - j1):
        for k in range(i2 - i1):
            times[i1 + k] = (hw[j1 + k].start, hw[j1 + k].end)
    elif tag == 'replace':  # spread the heard span over the script words
        s0, e0 = hw[j1].start, hw[j2 - 1].end
        n = i2 - i1
        for k in range(n):
            times[i1 + k] = (s0 + (e0 - s0) * k / n, s0 + (e0 - s0) * (k + 1) / n)
# fill gaps from neighbours
for i, t in enumerate(times):
    if t is None:
        p = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), 0.0)
        q = next((times[j][0] for j in range(i + 1, len(times)) if times[j]), p + 0.3)
        times[i] = (p, max(p + 0.05, q))
match = sum(b.size for b in sm.get_matching_blocks()) / len(sw)
json.dump([{'t': w, 's': round(a, 2), 'e': round(b, 2)} for w, (a, b) in zip(sw, times)], open(out, 'w'))
print(f'{len(sw)} words, match {match:.0%}, last end {times[-1][1]:.2f}s')
