"""Turkish subtitles, one cue per sentence, timed from audio/words.json."""
import json, os, textwrap
W = json.load(open('audio/words.json'))
TR = [(0, 10, "Büyük Piramit'i gerçekte kim yaptı... ve ne içindi?"),
      (11, 27, "2,3 milyon blok, bazıları bir kamyondan ağır, gerçek kuzeye neredeyse kusursuz hizalanmış."),
      (28, 34, "Dört bin beş yüz yıl önce."),
      (35, 46, "1968'de İsviçreli bir yazar cevabını verdi: yıldızlardan gelen astronotlar."),
      (47, 52, "Ve ipuçları her yere kazınmış gibiydi."),
      (53, 56, "Abydos'ta bir helikopter."),
      (57, 65, "Dendera'da dev bir ampulün içinde parlayan bir yılan."),
      (66, 76, "Sakkara'da planör kanatlı tahta bir kuş."),
      (77, 84, "Kimine göre piramit bir enerji santraliydi."),
      (85, 95, "Kimine göre bir yıldız kapısı: içindeki bir kanal doğrudan Orion Kuşağı'na bakıyor."),
      (96, 105, "Sonra, 1990'da, bir at gömülü bir duvara takıldı."),
      (106, 114, "Altında inşaatçıların kendileri yatıyordu, krallarının yanına gömülmüş."),
      (115, 125, "Ekipleri taşlara adlarını yazmıştı: Keops'un Dostları. Mikerinos'un Sarhoşları."),
      (126, 135, "Bir papirüs seyir defteri, taş yüklü tekneleri Gize'ye kadar izliyor."),
      (136, 142, "Ama kralın lahdi boştu."),
      (143, 147, "Keops hiç bulunamadı."),
      (148, 150, "Kim bilir..."),
      (151, 159, "Mısırlılar yoksa uzaylı bir ırktan yardım mı alıyordu?")]
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
