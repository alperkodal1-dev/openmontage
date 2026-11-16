"""Turkish subtitles, one cue per sentence, timed from audio/words.json."""
import json, textwrap
W = json.load(open('audio/words.json'))
TR = [(0, 7, "Bu Osmanlı haritası Antarktika'yı gösterdiği için ünlü."),
      (8, 9, "Göstermiyor."),
      (10, 19, "Ama Columbus'un kayıp haritasının bir kopyasını saklıyor olabilir."),
      (20, 32, "1929'da Topkapı Sarayı'nda ortaya çıktı: bir parça ceylan derisi."),
      (33, 41, "Amiral Piri Reis onu 1513'te Gelibolu'da çizdi."),
      (42, 47, "Kenarları harikalarla dolu:"),
      (48, 56, "dev bir balığın sırtında kamp kuran keşişler, tek boynuzlu öküzler,"),
      (57, 61, "ve yedi karış boyunda canavarlar,"),
      (62, 66, "\"ama zararsız canlardır.\""),
      (67, 84, "1960'larda bazı yazarlar güney kıyısının, buzlardan önce kayıp bir uygarlığın çizdiği Antarktika olduğunu iddia etti."),
      (85, 100, "Ama Antarktika milyonlarca yıldır buz altında ve 1820'ye kadar kimse onu görmedi."),
      (101, 114, "Tarihçilerin çoğu o kıyıyı, deriye sığsın diye doğuya bükülmüş Güney Amerika olarak okuyor."),
      (115, 126, "Notları kaynakları sayıyor: yaklaşık yirmi harita, biri Columbus'un çizdiği."),
      (127, 138, "Amcasının elinde, Columbus'la üç kez sefere çıkmış bir esir vardı."),
      (139, 143, "Columbus'un kendi haritası kayıp."),
      (144, 152, "Ama o buzun altında fosil ormanlar, hatta dinozorlar yatıyor."),
      (153, 160, "Kim bilir... orada hiç yaşayan oldu mu?"),
      (161, 163, "Gerçek mi, efsane mi?"),
      (164, 166, "Aşağıya yaz.")]
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
