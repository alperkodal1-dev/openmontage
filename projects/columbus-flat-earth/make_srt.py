"""Turkish subtitles, one cue per sentence, timed from audio/words.json."""
import json, textwrap
W = json.load(open('audio/words.json'))
TR = [(0, 6, "Columbus, Dünya'nın yuvarlak olduğunu hiç kanıtlamadı."),
      (7, 13, "1492'de her eğitimli Avrupalı bunu zaten biliyordu."),
      (14, 20, "Peki ona hayır diyen uzmanlar?"),
      (21, 23, "Haklıydılar."),
      (24, 38, "MÖ 240 civarında Eratosthenes, gezegeni yalnızca iki Mısır şehrindeki gölgelerle ölçtü."),
      (39, 41, "Sonuca çok yaklaştı."),
      (42, 46, "Orta Çağ keşişleri de bunu öğretti."),
      (47, 54, "Denizcilerin asıl korktuğu şey okyanusun kendisiydi."),
      (55, 63, "Eski haritalar onu deniz yılanları ve canavarlarla doldururdu."),
      (64, 67, "Bir küre şöyle uyarır:"),
      (68, 70, "Burada ejderhalar var."),
      (71, 75, "Columbus'un asıl hatası boyuttu."),
      (76, 83, "Dünyayı yaklaşık dörtte bir küçülttü."),
      (84, 92, "Uzmanlar, Asya'nın ulaşılamayacak kadar uzak olduğunu söyledi."),
      (93, 104, "Yolda bilinmeyen bir kıta olmasaydı, tayfaları açlıktan ölecekti."),
      (105, 110, "Peki düz Dünya'yı kim icat etti?"),
      (111, 126, "1828'de Washington Irving, rahiplerin yuvarlak Dünya'yı reddettiği dramatik bir Columbus biyografisi yazdı."),
      (127, 129, "Okul kitapları bunu tekrarladı."),
      (130, 144, "Ya gökyüzünün kenarından öteye bakan adamın o ünlü \"Orta Çağ\" gravürü?"),
      (145, 150, "İlk kez 1888'de, Paris'te basıldı."),
      (151, 158, "Peki Dünya'nın düz olduğuna gerçekten kim inandı:"),
      (159, 161, "Onlar mı, biz mi?"),
      (162, 164, "Gerçek mi, efsane mi?"),
      (165, 167, "Aşağıya yaz.")]
assert TR[-1][1] == len(W) - 1
ts = lambda t: f"{int(t//3600):02}:{int(t%3600//60):02}:{int(t%60):02},{int(round(t%1*1000)):03}"
out = []
for i, (a, b, text) in enumerate(TR):
    s, e = W[a]['s'], W[b]['e'] + 0.25
    if i + 1 < len(TR): e = min(e, W[TR[i + 1][0]]['s'] - 0.05)
    else: e += 1.5
    out.append(f"{i+1}\n{ts(s)} --> {ts(e)}\n" + "\n".join(textwrap.wrap(text, 42)) + "\n")
open('out/columbus_tr.srt', 'w').write("\n".join(out))
print(len(out), 'cues')
