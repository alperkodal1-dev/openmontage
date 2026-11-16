import subprocess
ev=[("rumble",0.0,0.45),("wash",0.05,0.22),("hit",1.0,0.6),("swell",1.3,0.18),
    ("tick",7.5,0.25),("tick",8.7,0.25),("tick",10.0,0.25),("hit",13.95,0.45),("hit",15.15,0.5),
    ("whoosh",19.3,0.25),("whoosh",20.4,0.25),("whoosh",21.4,0.3),("tick",25.45,0.3),("tick",28.2,0.3),("tick",32.2,0.3),("tick",36.65,0.3),
    ("whoosh",38.0,0.35),("tick",39.5,0.25),("tick",41.65,0.25),("hit",47.9,0.35),("hit",48.75,0.35),("rumble",49.55,0.55),("wash",50.4,0.4),
    ("hit",53.0,0.3)]+[("tick",54.6+i*0.1,0.12) for i in range(10)]+[("tick",57.55,0.3),("hit",62.1,0.55),("whoosh",67.3,0.35),("swell",69.6,0.22)]
inp=["-i","../source/audio.mp3"];fl=[];lab=[]
for i,(n,t,v) in enumerate(ev):
    inp+=["-i",f"{n}.wav"];ms=int(t*1000)
    fl.append(f"[{i+1}]adelay={ms}|{ms},volume={v}[e{i}]");lab.append(f"[e{i}]")
fl.append("[0]aformat=channel_layouts=stereo,aresample=48000[v]")
fl.append(f"[v]{''.join(lab)}amix=inputs={len(ev)+1}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
subprocess.run(["ffmpeg","-v","error","-y",*inp,"-filter_complex",";".join(fl),"-map","[out]","-ar","48000","-c:a","aac","-b:a","192k","mix.m4a"],check=True)
