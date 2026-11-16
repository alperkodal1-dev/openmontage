"""Turkish subtitles, one cue per sentence, timed from audio/words.json."""
import json, textwrap
W = json.load(open('audio/words.json'))
TR = [(0, 7, "Bu Osmanlı haritası Antarktika'yı gösterdiği için ünlü."),
      (8, 9, "Göstermiyor."),
      (10, 19, "Ama Columbus'un kayıp haritasının bir kopyasını saklıyor olabilir."),
      (20, 31, "1929'da Topkapı Sarayı'nda ortaya çıktı: bir parça ceylan derisi."),
      (32, 39, "Piri Reis onu 1513'te, Gelibolu'da çizdi."),
      (40, 55, "Sonra bazı yazarlar güney kıyısında Antarktika'yı gördü: buzlardan önce, kayıp bir uygarlığın çizdiği."),
      (56, 71, "Ama Antarktika milyonlarca yıldır buz altında ve 1820'ye kadar kimse onu görmedi."),
      (72, 82, "Tarihçiler orada, deriye sığsın diye doğuya bükülmüş Güney Amerika'yı görüyor."),
      (83, 88, "Peki bu haritayı nereden buldu?"),
      (89, 98, "Notlarında yaklaşık yirmi harita sayıyor; biri Columbus'un çizdiği."),
      (99, 107, "Amcasının esiri, Columbus'la üç kez sefere çıkmıştı."),
      (108, 123, "Onların harikalarını da kopyaladı: dev bir balığın üstündeki keşişler, tek boynuzlu öküzler, yedi karış boyunda canavarlar."),
      (124, 131, "Ve yanlarına bir not bile düştü..."),
      (132, 136, "\"Ama zararsız canlardır.\""),
      (137, 142, "Columbus'un kendi haritası hiçbir zaman bulunamadı."),
      (143, 151, "Ama o buzun altında fosil ormanlar, hatta dinozorlar yatıyor."),
      (152, 158, "Antarktika hakkında hâlâ çok az şey biliyoruz..."),
      (159, 167, "o halde her şeyden nasıl bu kadar emin olabiliyoruz?"),
      (168, 172, "Orada hiç yaşayan oldu mu?"),
      (173, 175, "Aşağıya yaz.")]
assert TR[-1][1] == len(W) - 1
ts = lambda t: f"{int(t//3600):02}:{int(t%3600//60):02}:{int(t%60):02},{int(round(t%1*1000)):03}"
out = []
for i, (a, b, text) in enumerate(TR):
    s, e = W[a]['s'], W[b]['e'] + 0.25
    if i + 1 < len(TR): e = min(e, W[TR[i + 1][0]]['s'] - 0.05)
    else: e += 1.5
    out.append(f"{i+1}\n{ts(s)} --> {ts(e)}\n" + "\n".join(textwrap.wrap(text, 42)) + "\n")
import os; os.makedirs('out', exist_ok=True)
open('out/piri_reis_tr.srt', 'w').write("\n".join(out))
print(len(out), 'cues')
