"""Turkish subtitles, one cue per sentence, timed from audio/words.json."""
import json, os, textwrap
W = json.load(open('audio/words.json'))
TR = [(0, 10, "Mısır'daki bir tapınaktaki bu oyma, bir helikopteri gösteriyor gibi."),
      (11, 21, "1968'de İsviçreli bir yazar, Mısır'ı eski astronotların ziyaret ettiğini söyledi."),
      (22, 26, "Takipçileri daha fazla ipucu gördü."),
      (27, 37, "Dendera'da, dev bir ampule benzeyen şeyin içinde bir yılan."),
      (38, 45, "Sakkara'da, planör kanatlı tahta bir kuş."),
      (46, 59, "Ve Büyük Piramit: yaklaşık 2,3 milyon blok, gerçek kuzeye hizalı."),
      (60, 66, "Kimine göre bir enerji santraliydi."),
      (67, 76, "Kimine göre bir yıldız kapısı: içindeki bir kanal bir zamanlar Orion Kuşağı'na bakıyordu."),
      (77, 88, "1990'da, anlatılana göre, bir at gömülü bir duvara takıldı."),
      (89, 100, "Altında, kralın piramidinin gölgesinde, inşaatçılar yatıyordu."),
      (101, 108, "Ekipleri taşlara adlarını yazdı: Keops'un Dostları."),
      (109, 113, "Hemen yanında: Mikerinos'un Sarhoşları."),
      (114, 122, "Bir papirüs seyir defteri, kireçtaşı yüklü tekneleri Gize'ye kadar izliyor."),
      (123, 129, "Ama kralın lahdi boş bulundu."),
      (130, 143, "Daha sonraki piramit metinleri, krala göğe bir merdiven ve Orion'a dönüşmeyi vaat eder."),
      (144, 151, "Bir mezar mı... yoksa yıldızlara giden bir merdiven mi?"),
      (152, 157, "Peki piramitler aslında neydi?")]
assert TR[-1][1] == len(W) - 1
ts = lambda t: f"{int(t//3600):02}:{int(t%3600//60):02}:{int(t%60):02},{int(round(t%1*1000)):03}"
out = []
for i, (a, b, text) in enumerate(TR):
    s, e = W[a]['s'], W[b]['e'] + 0.25
    if i + 1 < len(TR): e = min(e, W[TR[i + 1][0]]['s'] - 0.05)
    else: e += 0.6
    out.append(f"{i+1}\n{ts(s)} --> {ts(e)}\n" + "\n".join(textwrap.wrap(text, 42)) + "\n")
os.makedirs('out', exist_ok=True)
open('out/pyramid_tr.srt', 'w').write("\n".join(out))
print(len(out), 'cues')
