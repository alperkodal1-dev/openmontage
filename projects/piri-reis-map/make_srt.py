"""Turkish subtitles, one cue per sentence, timed from audio/words.json."""
import json, textwrap
W = json.load(open('audio/words.json'))
TR = [(0, 9, "Kaçımız Antarktika'da ne olduğundan gerçekten emin?"),
      (10, 21, "1513 tarihli bu harita, 1820'ye kadar kimsenin görmediği bir kıtayı gösteriyor..."),
      (22, 24, "öyle mi?"),
      (25, 33, "Osmanlı amirali Piri Reis onu ceylan derisine çizdi."),
      (34, 40, "1929'da Topkapı Sarayı'nda ortaya çıktı."),
      (41, 55, "Yazarlar güney kıyısında, buzlardan önce kayıp bir uygarlığın çizdiği Antarktika'yı gördü."),
      (56, 63, "Ama o buz milyonlarca yıllık."),
      (64, 74, "Tarihçiler orada, deriye sığsın diye doğuya bükülmüş Güney Amerika'yı görüyor."),
      (75, 76, "Kaynakları mı?"),
      (77, 86, "Notları yaklaşık yirmi harita sayıyor; biri Columbus'un çizdiği."),
      (87, 101, "Amcası, korsan Kemal Reis'in elinde Columbus'la üç kez sefere çıkmış bir esir vardı."),
      (102, 119, "Eski haritaların harikalarını da kopyaladı: dev bir balığın üstündeki keşişler, tek boynuzlu öküzler, yedi karış boyunda canavarlar."),
      (120, 122, "Bir not bile düştü..."),
      (123, 127, "\"Ama zararsız canlardır.\""),
      (128, 133, "Columbus'un kendi haritası hiçbir zaman bulunamadı."),
      (134, 142, "Ve o buzun altında fosil ormanlar, hatta dinozorlar yatıyor."),
      (143, 149, "Antarktika hakkında hâlâ çok az şey biliyoruz..."),
      (150, 156, "o halde nasıl bu kadar emin olabiliriz?")]
assert TR[-1][1] == len(W) - 1
ts = lambda t: f"{int(t//3600):02}:{int(t%3600//60):02}:{int(t%60):02},{int(round(t%1*1000)):03}"
out = []
for i, (a, b, text) in enumerate(TR):
    s, e = W[a]['s'], W[b]['e'] + 0.25
    if i + 1 < len(TR): e = min(e, W[TR[i + 1][0]]['s'] - 0.05)
    else: e += 0.6
    out.append(f"{i+1}\n{ts(s)} --> {ts(e)}\n" + "\n".join(textwrap.wrap(text, 42)) + "\n")
import os; os.makedirs('out', exist_ok=True)
open('out/piri_reis_tr.srt', 'w').write("\n".join(out))
print(len(out), 'cues')
