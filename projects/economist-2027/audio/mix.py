"""Economist mix: VO + own vidIQ tension score (ducked) + whoosh per snap zoom, booms on hook and reveal -> mix.m4a at -14 LUFS."""
import subprocess
END = 62.8
MUS = '../../noah-ark/audio/music_tension.wav'
S = '../../atlantis-story/sfx/'
SNAP = (7.3, 19.36, 23.1, 23.7, 24.3, 27.72, 28.48, 34.52, 36.0, 39.4, 40.88, 45.32)
SFX = [('hit', 0.0, 0.9), ('rumble', 0.0, 0.7), ('hit', 3.3, 0.9), ('rumble', 3.3, 0.6)] + [('whoosh', t - 0.12, 0.4) for t in SNAP] \
      + [('hit', 5.5, 0.8), ('swell', 9.6, 0.5), ('hit', 10.6, 0.8), ('whoosh', 16.35, 0.5), ('hit', 16.7, 0.8), ('whoosh', 30.3, 0.45), ('hit', 25.8, 0.8), ('hit', 31.8, 1.0), ('rumble', 31.8, 0.7),
         ('hit', 33.3, 0.8), ('tick', 38.5, 0.6), ('hit', 45.32, 1.0), ('rumble', 45.32, 0.8), ('tick', 48.2, 0.7),
         ('whoosh', 56.56, 0.45), ('whoosh', 57.94, 0.45), ('swell', 58.6, 0.6), ('hit', 59.62, 0.9), ('rumble', 59.62, 0.8)]
inp = ['-i', 'vo.wav', '-stream_loop', '-1', '-i', MUS] + sum([['-i', S + f'{n}.wav'] for n, _, _ in SFX], [])
f = [f'[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={END},asplit[vo][sc]',
     f'[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{END},volume=0.16,afade=t=out:st={END-0.4}:d=0.4[m]',
     '[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=250[md]']
for i, (n, t, g) in enumerate(SFX):
    f.append(f'[{i+2}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g},adelay={int(t*1000)}|{int(t*1000)},apad=whole_dur={END}[s{i}]')
f.append('[vo][md]' + ''.join(f'[s{i}]' for i in range(len(SFX))) + f'amix=inputs={2+len(SFX)}:normalize=0,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[out]')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(f), '-map', '[out]', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print('mix.m4a ok')
