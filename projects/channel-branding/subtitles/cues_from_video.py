"""Sentence cues (English) from a final video with faster-whisper word timestamps.
Usage: python3 cues_from_video.py <video.mp4> <out.json>"""
import json, re, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel
src, out = sys.argv[1], sys.argv[2]
pcm = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-f', 's16le', '-ac', '1', '-ar', '16000', '-'],
                                   capture_output=True).stdout, np.int16).astype(np.float32) / 32768
m = WhisperModel('small.en', device='cpu', compute_type='int8')
segs, _ = m.transcribe(pcm, word_timestamps=True, vad_filter=True)
words = [w for s in segs for w in s.words]
cues, cur = [], []
for w in words:
    cur.append(w)
    text = ''.join(x.word for x in cur).strip()
    end = re.search(r'[.?!]["”]?$', w.word.strip()) or w.word.strip().endswith('...')
    if end or len(text) > 80 or (cur[-1].end - cur[0].start) > 5.5:
        cues.append({'s': round(cur[0].start, 2), 'e': round(cur[-1].end, 2), 'en': text}); cur = []
if cur: cues.append({'s': round(cur[0].start, 2), 'e': round(cur[-1].end, 2), 'en': ''.join(x.word for x in cur).strip()})
json.dump(cues, open(out, 'w'), ensure_ascii=False, indent=1)
print(out, len(cues), 'cues, last', cues[-1]['e'])
