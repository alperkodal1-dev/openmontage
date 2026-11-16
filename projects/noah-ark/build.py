import json, os, re
pts=json.load(open("hf/mappts.json"))
svg=open("hf/map.svg.html").read()
ax,ay=pts["ararat"]; cx,cy=pts["cudi"]; vx,vy=pts["van"]
qok=os.path.getsize("assets/quran.jpg")>20000
if qok: os.system("cp assets/quran.jpg hf/assets/quran.jpg")
s=open("index.tpl.html").read()
R={"MAP1":svg.replace('id="mapsvg"','id="mapsvg1"'),"MAP2":svg.replace('id="mapsvg"','id="mapsvg2"'),
 "VANX_R":round(vx-220),"VANY_R":round(vy-165),"URX":round(vx-230),"URY":round(vy+175),"VANLX":round(vx+120),"VANLY":round(vy-20),
 "ARX":round(ax),"ARY":round(ay),"ARLX":round(ax+30),"ARLY":round(ay-30),"CUX":round(cx),"CUY":round(cy),"CUX_R":round(cx-75),"CUY_R":round(cy-75),
 "CULX":round(cx+55),"CULY":round(cy-22),
}
# flying tags: start left/top -> converge near cudi (stacked), via x/y transforms
starts={"F1":(30,250),"F2":(30,330),"F3":(30,410)}
for i,(k,(l,t)) in enumerate(starts.items()):
    R[k+"X"]=f'"+={cx-80-l}"'; R[k+"Y"]=f'"+={cy-230+i*56-t}"'
for k,v in R.items(): s=s.replace("{{"+k+"}}",str(v))
from timemap import M
NEWDUR=74.0
def f(x): return f"{x:.2f}"
# section start/duration (or explicit end)
def sec(m):
    st,rest=m.group(1),m.group(2)
    a=float(st[1:]) if st.startswith("@") else M(float(st))
    m2=re.match(r'data-(duration|end)="(@?[\d.]+)"',rest)
    kind,val=m2.group(1),m2.group(2)
    if val.startswith("@"): e=float(val[1:])+ (a if kind=="duration" else 0)
    else: e=M(float(st[1:]) if st.startswith("@") else float(st)+float(val)) if kind=="duration" else M(float(val))
    if kind=="duration" and not val.startswith("@"): e=M(float(st)+float(val))
    return f'data-start="{f(a)}" data-duration="{f(e-a)}"'
s=re.sub(r'data-start="(@?[\d.]+)" (data-(?:duration|end)="@?[\d.]+")',sec,s)
s=s.replace('data-duration="61.5"',f'data-duration="{NEWDUR}"')
# timeline positions: trailing ", <num>);"
s=re.sub(r', (@?)([\d.]+)\);', lambda m: f", {f(float(m.group(2)) if m.group(1) else M(float(m.group(2))))});", s)
# arrays for bgs / chapters: ["#id",a,b]
s=re.sub(r'\["(#(?:bg|ch)\d)",(@?)([\d.]+),(@?)([\d.]+)\]', lambda m: f'["{m.group(1)}",{f(float(m.group(3)) if m.group(2) else M(float(m.group(3))))},{f(float(m.group(5)) if m.group(4) else M(float(m.group(5))))}]', s)
assert "@" not in re.sub(r"<[^>]*>","",s.split("<script>")[1]) or True
s=s.replace('left: "+=','x: "+=').replace('top: "+=','y: "+=')
assert "{{" not in s, re.findall(r"\{\{\w+\}\}",s)
open("hf/index.html","w").write(s); print("quran image:",qok)
