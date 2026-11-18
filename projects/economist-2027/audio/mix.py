"""Economist mix: VO + own vidIQ tension score (ducked) + whoosh per snap zoom, booms on hook and reveal -> mix.m4a at -14 LUFS."""
import subprocess
END = 20.4
MUS = '../../noah-ark/audio/music_tension.wav'
S = '../../atlantis-story/sfx/'
SFX = [('hit', 0.0, 0.9), ('rumble', 0.0, 0.7), ('hit', 3.3, 0.9)] + [('whoosh', t - 0.12, 0.45) for t in (4.38, 4.78, 5.62, 6.92, 8.22, 9.58, 10.84, 12.8, 14.7)] \
      + [('hit', 15.86, 1.0), ('rumble', 15.86, 0.8), ('tick', 18.4, 0.7)]
inp = ['-i', 'vo.wav', '-i', MUS] + sum([['-i', S + f'{n}.wav'] for n, _, _ in SFX], [])
f = [f'[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={END},asplit[vo][sc]',
     f'[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{END},volume=0.16,afade=t=out:st={END-0.25}:d=0.25[m]',
     '[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=250[md]']
for i, (n, t, g) in enumerate(SFX):
    f.append(f'[{i+2}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g},adelay={int(t*1000)}|{int(t*1000)},apad=whole_dur={END}[s{i}]')
f.append('[vo][md]' + ''.join(f'[s{i}]' for i in range(len(SFX))) + f'amix=inputs={2+len(SFX)}:normalize=0,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[out]')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(f), '-map', '[out]', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print('mix.m4a ok')
