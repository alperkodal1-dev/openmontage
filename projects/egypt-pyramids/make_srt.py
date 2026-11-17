"""Turkish subtitles, one cue per sentence, timed from audio/words.json (sentences end on . or ?, not on ...)."""
import json, os, textwrap
W = json.load(open('audio/words.json'))
TR = ["Piramitleri köleler yaptı... öyle mi?",
      "Mısır'daki bir tapınaktaki bu oyma, bir helikopteri gösteriyor gibi.",
      "1968'de İsviçreli bir yazar, Mısır'ı eski astronotların ziyaret ettiğini söyledi.",
      "Takipçileri daha fazla ipucu gördü.",
      "Dendera'da, dev bir ampule benzeyen şeyin içinde bir yılan.",
      "Sakkara'da, planör kanatlı tahta bir kuş.",
      "Ve Büyük Piramit: yaklaşık 2,3 milyon blok, gerçek kuzeye hizalı.",
      "Kimine göre bir enerji santraliydi.",
      "Kimine göre bir yıldız kapısı: içindeki bir kanal bir zamanlar Orion Kuşağı'na bakıyordu.",
      "Ya da öyle anlatılır.",
      "1990'da bir at gömülü bir duvara takıldı.",
      "Altında, kralın piramidinin gölgesinde, inşaatçılar yatıyordu.",
      "Ekipleri taşlara adlarını yazdı: Keops'un Dostları.",
      "Hemen yanında: Mikerinos'un Sarhoşları.",
      "Bir papirüs seyir defteri, kireçtaşı yüklü tekneleri Gize'ye kadar izliyor.",
      "Ama kralın lahdi boş bulundu.",
      "Daha sonraki piramit metinleri, krala göğe bir merdiven ve Orion'a dönüşmeyi vaat eder.",
      "Bir mezar mı... yoksa yıldızlara giden bir merdiven mi?",
      "Peki piramitler aslında neydi?"]
spans, a = [], 0
for i, w in enumerate(W):
    if w['t'].endswith('?') or (w['t'].endswith('.') and not w['t'].endswith('...')):
        spans.append((a, i)); a = i + 1
assert len(spans) == len(TR), (len(spans), len(TR))
ts = lambda t: f"{int(t//3600):02}:{int(t%3600//60):02}:{int(t%60):02},{int(round(t%1*1000)):03}"
out = []
for k, ((a, b), text) in enumerate(zip(spans, TR)):
    s, e = W[a]['s'], W[b]['e'] + 0.25
    if k + 1 < len(spans): e = min(e, W[spans[k + 1][0]]['s'] - 0.05)
    else: e += 0.6
    out.append(f"{k+1}\n{ts(s)} --> {ts(e)}\n" + "\n".join(textwrap.wrap(text, 42)) + "\n")
os.makedirs('out', exist_ok=True)
open('out/pyramid_tr.srt', 'w').write("\n".join(out))
print(len(out), 'cues')
