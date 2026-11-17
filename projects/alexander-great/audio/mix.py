"""Alexander mix: narration + own tension score (vidIQ, from the Noah project) ducked + signature SFX -> mix.m4a, -14 LUFS."""
import subprocess
END = 54.6
MUS = '../../noah-ark/audio/music_tension.wav'
S = '../../atlantis-story/sfx/'
SFX = [('hit', 4.8, 1.0), ('rumble', 4.8, 0.8), ('hit', 5.1, 0.7), ('whoosh', 6.3, 0.45), ('whoosh', 9.0, 0.4), ('whoosh', 12.7, 0.4),
       ('hit', 17.96, 1.0), ('swell', 21.0, 0.5), ('hit', 23.4, 0.8), ('hit', 24.96, 1.0), ('rumble', 24.96, 0.8), ('hit', 25.9, 0.9),
       ('whoosh', 28.8, 0.4), ('tick', 30.9, 0.8), ('tick', 31.6, 0.8), ('tick', 32.55, 0.8), ('whoosh', 34.7, 0.4), ('hit', 47.7, 0.7), ('wash', 48.8, 0.5)]
vol = "volume='if(lt(t,6.3),0.10,if(lt(t,24.9),0.14,if(lt(t,27.1),0.11,if(lt(t,48.8),0.08,0.12))))':eval=frame"
inp = ['-i', 'vo.wav', '-i', MUS] + sum([['-i', S + f'{n}.wav'] for n, _, _ in SFX], [])
f = [f'[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={END},asplit[vo][sc]',
     f'[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{END},{vol},afade=t=in:d=0.3,afade=t=out:st={END-1.6}:d=1.6[m]',
     '[m][sc]sidechaincompress=threshold=0.015:ratio=8:attack=20:release=350[md]']
for i, (n, t, g) in enumerate(SFX):
    f.append(f'[{i+2}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g},adelay={int(t*1000)}|{int(t*1000)},apad=whole_dur={END}[s{i}]')
f.append('[vo][md]' + ''.join(f'[s{i}]' for i in range(len(SFX))) + f'amix=inputs={2+len(SFX)}:normalize=0,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[out]')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(f), '-map', '[out]', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print('mix.m4a ok')
