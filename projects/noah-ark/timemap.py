import json, re, difflib
norm=lambda x: re.sub(r"[^a-z0-9]","",x.lower())
O=json.load(open("audio/words_v1.json")); N=json.load(open("audio/words.json"))
OLD_END,NEW_END=57.94,70.43
STOP={"the","and","that","this","with","they","into","were","from","what","where","which","only","said","says"}
key=lambda w: norm(w["t"]) if len(norm(w["t"]))>=4 and norm(w["t"]) not in STOP else "_"+str(id(w))
sm=difflib.SequenceMatcher(a=[key(w) for w in O],b=[key(w) for w in N],autojunk=False)
A=[(0.0,0.0)]
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=="equal":
        for k in range(i2-i1):
            o,n=O[i1+k]["s"],N[j1+k]["s"]
            if o>A[-1][0]+0.05 and n>A[-1][1]+0.05: A.append((o,n))
A.append((OLD_END,NEW_END))
def M(t):
    if t<=1.5: return t                      # cold open choreography stays fixed
    if t>=OLD_END: return t-OLD_END+NEW_END
    for (o0,n0),(o1,n1) in zip(A,A[1:]):
        if o0<=t<=o1: return n0+(t-o0)*(n1-n0)/(o1-o0)
    return t
