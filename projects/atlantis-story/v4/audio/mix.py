"""Atlantis v4 mix: narration + own score (Piri Reis vidIQ track) with side-chain ducking + signature SFX -> mix.m4a, -14 LUFS."""
import subprocess
END = 55.8
MUS = '../../../piri-reis-map/audio/music_v1.wav'
SFX = [('hit', 2.76, 1.0), ('rumble', 2.76, 0.8), ('hit', 3.0, 0.7), ('whoosh', 3.85, 0.45), ('swell', 15.6, 0.5),
       ('hit', 19.2, 0.6), ('hit', 21.44, 1.0), ('rumble', 21.44, 0.8), ('hit', 22.4, 0.9), ('whoosh', 23.5, 0.45),
       ('hit', 42.4, 0.7), ('whoosh', 43.7, 0.4), ('wash', 49.7, 0.5)]
# music level: lift in the legend, low under the evidence, back up for the question
vol = ("volume='if(lt(t,4),0.10,if(lt(t,21.4),0.135,if(lt(t,23.6),0.11,if(lt(t,49.7),0.075,0.12))))':eval=frame")
inp = ['-i', 'vo.wav', '-i', MUS] + sum([['-i', f'../../sfx/{n}.wav'] for n, _, _ in SFX], [])
f = [f'[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={END},asplit[vo][sc]',
     f'[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{END},{vol},afade=t=in:d=0.4,afade=t=out:st={END-1.6}:d=1.6[m]',
     '[m][sc]sidechaincompress=threshold=0.015:ratio=8:attack=20:release=350[md]']
for i, (n, t, g) in enumerate(SFX):
    f.append(f'[{i+2}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g},adelay={int(t*1000)}|{int(t*1000)},apad=whole_dur={END}[s{i}]')
f.append('[vo][md]' + ''.join(f'[s{i}]' for i in range(len(SFX))) + f'amix=inputs={2+len(SFX)}:normalize=0,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[out]')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(f), '-map', '[out]', '-c:a', 'aac', '-b:a', '192k', 'mix.m4a'], check=True)
print('mix.m4a ok')
