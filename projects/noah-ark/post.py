"""v3: new hook line spliced in front of v2 narration. Remap v2 times -> v3 times."""
import re, json
D=5.16-8.986
def T(t):
    if t<=1.5: return t
    if t<8.98:
        A=[(1.5,1.5),(4.13,2.6),(6.46,3.9),(8.98,5.16)]
        for (a0,b0),(a1,b1) in zip(A,A[1:]):
            if a0<=t<=a1: return b0+(t-a0)*(b1-b0)/(a1-a0)
    return t+D
if __name__=="__main__":
    s=open("hf/index.html").read()
    # S1 rework
    s=s.replace('<div class="center" id="q1"><div class="big">MOUNT ARARAT?</div></div>','')
    s=re.sub(r'\n\s*tl\.from\("#q1"[^\n]*','',s)
    s=s.replace('<div class="stamp" id="st1s">NEVER NAMED</div>','<div class="stamp" id="st1s">NOT ONCE</div>')
    # numbers
    s=re.sub(r'data-start="([\d.]+)" data-duration="([\d.]+)"',lambda m:(lambda a,e:f'data-start="{a:.2f}" data-duration="{e-a:.2f}"')(T(float(m.group(1))),T(float(m.group(1))+float(m.group(2)))),s)
    s=re.sub(r'(id="root"[^>]*data-duration=")[\d.]+"',lambda m:m.group(1)+'72.2"',s)
    s=re.sub(r', ([\d.]+)\);',lambda m:f", {T(float(m.group(1))):.2f});",s)
    s=re.sub(r'\["(#(?:bg|ch)\d)",([\d.]+),([\d.]+)\]',lambda m:f'["{m.group(1)}",{T(float(m.group(2))):.2f},{T(float(m.group(3))):.2f}]',s)
    # hook overlay: keep through "not once", chapter after it
    s=re.sub(r'(id="hk" class="clip" data-start="0.00" data-duration=")[\d.]+"',r'\g<1>5.00"',s)
    s=re.sub(r'(tl\.to\(\["#hk1","#hk2"\][^)]*\}, )[\d.]+\);',r'\g<1>4.65);',s)
    s=re.sub(r'\["#ch1",[\d.]+,[\d.]+\],','',s)
    open("hf/index.html","w").write(s)
    # captions
    H=[("The",0.0,0.18),("Bible",0.18,0.46),("never",0.46,0.84),("says",0.84,1.18),("Noah's",1.18,1.66),("Ark",1.66,1.94),("landed",1.94,2.32),("on",2.32,2.52),("Mount",2.52,2.78),("Ararat...",2.78,3.36),("Not",3.9,4.12),("once.",4.12,4.48)]
    W=[{"t":t,"s":a,"e":b} for t,a,b in H]
    for w in json.load(open("audio/words.json")):
        if w["s"]>=8.9: W.append({"t":w["t"],"s":round(w["s"]+D,2),"e":round(w["e"]+D,2)})
    W=[w for w in W if w["s"]<60.9]
    E0=61.05
    for t,a,b in [("So...",0.0,0.34),("Ararat,",0.96,1.44),("or",1.44,2.04),("Cudi?",2.04,2.46),("Or...",3.2,3.4),("do",3.4,3.98),("you",3.98,4.12),("think",4.12,4.32),("Noah's",4.32,4.8),("Ark",4.8,5.12),("really",5.12,5.56),("existed?",5.56,6.1),("Tell",6.72,6.94),("me",6.94,7.12),("in",7.12,7.22),("the",7.22,7.3),("comments.",7.3,7.56)]:
        W.append({"t":t,"s":round(E0+a,2),"e":round(E0+b,2)})
    json.dump(W,open("audio/words_v3.json","w"))
    ch=[];cur=[]
    for w in W:
        cur.append(w)
        if re.search(r"[.,?!:]$",w["t"]) or len(cur)>=4 or cur[-1]["e"]-cur[0]["s"]>1.7: ch.append(cur);cur=[]
    if cur: ch.append(cur)
    C=[{"s":c[0]["s"],"e":c[-1]["e"],"w":c} for c in ch]
    for i in range(len(C)-1): C[i]["e"]=min(C[i+1]["s"],round(C[i]["e"]+0.5,2))
    C[-1]["e"]=round(C[-1]["e"]+1.2,2)
    open("hf/captions.js","w").write("window.CAPS="+json.dumps(C)+";")
    print("ok")
