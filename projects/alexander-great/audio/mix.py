"""Alexander mix: narration + own tension score (vidIQ, from the Noah project) ducked + signature SFX -> mix.m4a, -14 LUFS."""
import subprocess
END = 56.2
MUS = '../../noah-ark/audio/music_tension.wav'
S = '../../atlantis-story/sfx/'
SFX = [('hit', 3.6, 1.0), ('rumble', 3.6, 0.8), ('hit', 3.9, 0.7), ('whoosh', 4.78, 0.45), ('whoosh', 7.48, 0.4), ('whoosh', 11.18, 0.4),
       ('hit', 16.44, 1.0), ('swell', 19.48, 0.5), ('hit', 21.88, 0.8), ('hit', 23.44, 1.0), ('rumble', 23.44, 0.8), ('hit', 23.95, 0.9), ('whoosh', 24.75, 0.6), ('hit', 25.5, 0.9),
       ('whoosh', 27.28, 0.4), ('tick', 29.38, 0.8), ('tick', 30.08, 0.8), ('tick', 31.03, 0.8), ('whoosh', 33.18, 0.4), ('swell', 39.2, 0.7), ('wash', 43.1, 0.5), ('hit', 47.5, 0.6), ('swell', 50.4, 0.6)]
vol = "volume='if(lt(t,4.8),0.10,if(lt(t,23.4),0.14,if(lt(t,25.6),0.11,if(lt(t,39.3),0.08,0.13))))':eval=frame"
inp = ['-i', 'vo.wav', '-i', MUS] + sum([['-i', S + f'{n}.wav'] for n, _, _ in SFX], [])
f = [f'[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={END},asplit[vo][sc]',
     f'[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{END},{vol},afade=t=in:d=0.3,afade=t=out:st={END-1.6}:d=1.6[m]',
     '[m][sc]sidechaincompress=threshold=0.015:ratio=8:attack=20:release=350[md]']
for i, (n, t, g) in enumerate(SFX):
    f.append(f'[{i+2}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g},adelay={int(t*1000)}|{int(t*1000)},apad=whole_dur={END}[s{i}]')
f.append('[vo][md]' + ''.join(f'[s{i}]' for i in range(len(SFX))) + f'amix=inputs={2+len(SFX)}:normalize=0,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[out]')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(f), '-map', '[out]', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print('mix.m4a ok')
