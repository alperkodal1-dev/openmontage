"""Economist mix: VO + own vidIQ tension score (ducked) + whoosh per snap zoom, booms on hook and reveal -> mix.m4a at -14 LUFS."""
import subprocess
END = 56.0
MUS = '../../noah-ark/audio/music_tension.wav'
S = '../../atlantis-story/sfx/'
SNAP = (7.3, 19.36, 22.28, 24.36, 27.72, 28.48, 34.92, 35.98, 38.64, 42.74, 54.22)
SFX = [('hit', 0.0, 0.9), ('rumble', 0.0, 0.7)] + [('whoosh', t - 0.12, 0.4) for t in SNAP] \
      + [('hit', 5.5, 0.8), ('swell', 9.6, 0.5), ('hit', 10.6, 0.8), ('hit', 25.8, 0.8), ('hit', 31.8, 1.0), ('rumble', 31.8, 0.7),
         ('hit', 33.45, 0.8), ('hit', 42.74, 1.0), ('rumble', 42.74, 0.8), ('tick', 45.6, 0.7), ('hit', 54.22, 0.9)]
inp = ['-i', 'vo.wav', '-i', MUS] + sum([['-i', S + f'{n}.wav'] for n, _, _ in SFX], [])
f = [f'[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={END},asplit[vo][sc]',
     f'[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{END},volume=0.16,afade=t=out:st={END-0.25}:d=0.25[m]',
     '[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=250[md]']
for i, (n, t, g) in enumerate(SFX):
    f.append(f'[{i+2}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g},adelay={int(t*1000)}|{int(t*1000)},apad=whole_dur={END}[s{i}]')
f.append('[vo][md]' + ''.join(f'[s{i}]' for i in range(len(SFX))) + f'amix=inputs={2+len(SFX)}:normalize=0,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[out]')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(f), '-map', '[out]', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print('mix.m4a ok')
