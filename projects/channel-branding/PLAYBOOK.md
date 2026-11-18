# "Or So The Story Goes" — Claude ile YouTube Shorts üretim rehberi

Bu dosya, bu kanalda Claude ile kullanılan bütün teknikleri tek yerde toplar. Başka bir Claude hesabında kullanmak için
dosyanın tamamını sohbete yapıştırın veya bir Proje'ye "talimat/bilgi dosyası" olarak ekleyin ve şöyle başlayın:
"Bu rehberdeki kurallarla çalış. Benimle Türkçe konuş, videolar İngilizce olsun."

> Bu dosyada şifre, token veya API anahtarı YOKTUR. Onları her hesapta ayrıca, güvenli yoldan (ortam ayarları / güvenli form) verin; sohbete yapıştırmayın.

---

## 1. Sabit kurallar (Claude'a ilk mesajda söyleyin)
1. Kredi harcamadan (vidIQ, ElevenLabs, fal vb.) ve yayınlamadan önce **mutlaka sor**.
2. Yayınlanmış bir videoyu **asla silip yeniden yükleme**; düzeltmeyi yerinde yap (başlık, açıklama, etiket).
3. Etiketlerde **sadece ekleme** yap, mevcut etiketi silme. 500 karakter sınırı (çok kelimeli etiket +2 tırnak, virgüller dahil) aşılacaksa güncelleme yapma, sor.
4. Başkasına ait müzik/görüntü kullanma (Content ID riski). Müzik: ya kendin üret ya da YouTube uygulamasındaki kütüphaneden ekle.
5. Günde 1 Short, her gün aynı saatte (20:00 İstanbul = 17:00 UTC), önceden zamanlanmış (private + publishAt).
6. Her Short: 60 saniyenin altı (ideal 20-58 sn), ilk 1-2 saniyede kanca, sonu başa bağlanan döngü.
7. Her iddia kaynaklı olsun; kaynak listesi açıklamaya.

## 2. Video formatı (kanal imzası)
- **Kanca:** Herkesin bildiğini söyleyip aynı cümlede şüphe: "Slaves built the pyramids... or did they?"
  Şüphe kelimesinde görüntü griye döner, sarsılır, beyaz flaş (grey shock). Kanca, videonun asıl iddiasını sorgulamalı
  (ör. Atlantis için "but was it ever there?", "but did it sink?" değil).
- **Efsane → dönüş:** Efsane canlı anlatılır, sonra "Or so the story goes." (kanal adı) + gri + MYTH damgası.
- **Kanıt:** Düz ve kaynaklı. Kapanış: açık bir soru, ilk cümleye bağlanır (loop). "Yorumlara yaz" demek yerine soru.
- **Görünüm:** 1080x1920. Üst 250 px boş (platform arayüzü). Karaoke altyazı (kelime kelime, aktif kelime altın/sarı),
  x 70-930 arası (sağdaki butonlardan uzak). Fontlar: Cinzel (başlık), Cormorant Garamond italik (alıntı), Manrope (altyazı).
  Renkler: mürekkep #0a1417, kemik #efe6d2, altın #d9b26a/#f1d49a, kırmızı damga #9c2f1f, efsane yeşili #7dffb0.
- **Ritim:** Resim her 1,5-3,5 sn'de değişir; her arka planda yavaş Ken Burns; hiçbir kare 3,5 sn'den uzun donuk kalmaz.
- **Ses:** Anlatıcı ~141 kelime/dk (George sesi). Müzik anlatıcının 5-10 dB altında, final -14 LUFS, tepe -1,5 dB.

## 3. Görsel kaynakları (telifsiz)
- **Wikimedia Commons** (kamu malı/CC): API ile ara ve indir; paylaşılan IP'de 429 hatası gelir, `Retry-After` kadar bekleyip tekrar dene.
  ```python
  API='https://commons.wikimedia.org/w/api.php?format=json&action=query&'
  # ara:  list=search&srnamespace=6&srsearch=<sorgu>
  # indir: prop=imageinfo&iiprop=url|size|extmetadata&iiurlwidth=1600&titles=File:<ad>
  # extmetadata -> LicenseShortName, Artist (açıklamaya kredi yaz)
  ```
- **The Met Open Access** (CC0), **NASA/ESA** (kamu malı), **Natural Earth** (harita verisi).
- CC BY-SA fotoğraflarda ekrana küçük kredi satırı + açıklamada kredi.

## 4. Ses teknikleri
- **Kredi kontrolü önce:** ElevenLabs'te `estimate_only` ile maliyeti gör; kredi yetmezse üretme. (~1 kredi/karakter.)
- **Aynı ses, kredisiz:** Daha önce okunmuş bir cümle gerekiyorsa eski kayıttan kes. Kelime zamanlarını (words.json) veya
  sessizlikleri bul:
  ```bash
  ffmpeg -ss 50 -t 12 -i vo.wav -af silencedetect=n=-40dB:d=0.25 -f null - 2>&1 | grep silence_
  ffmpeg -ss 54.20 -t 3.25 -i vo.wav -af "afade=t=in:d=0.03,afade=t=out:st=3.15:d=0.1,loudnorm=I=-15:TP=-2" line.wav
  ```
  Hızlandırılmış videoda zaman = SRT zamanı × hız oranı (ör. 1,06).
- **Ücretsiz alternatifler:** kendi sesin (telefonla kayıt) veya yerel açık kaynak TTS (kalitesi düşük, ses değişir).

## 5. Görüntü netleştirme (düşük çözünürlüklü kaynak)
Düz renkli çizimlerde (afiş, kapak) çok işe yarar: büyüt → medyan → kontrast → keskinleştir → renkleri paletine oturt.
```python
from PIL import Image, ImageFilter, ImageEnhance
big=src.filter(ImageFilter.MedianFilter(3))
big=ImageEnhance.Contrast(big).enhance(1.2).filter(ImageFilter.UnsharpMask(radius=4,percent=200,threshold=2))
cols=[(16,14,14),(205,30,32),(242,236,232),(150,24,26),(120,110,110)]   # kapağın kendi renkleri
pal=Image.new('P',(1,1)); pal.putpalette(sum(cols,())+(0,0,0)*(256-len(cols)))
flat=big.quantize(palette=pal,dither=Image.Dither.NONE).convert('RGB')
```
Yazıları 2x çözünürlükte çizip küçült (Playwright `deviceScaleFactor: 2`). Videoda filtre (`cas`, `unsharp`) az fark eder;
asıl çözüm videoyu net kaynakla yeniden oluşturmak.

## 6. Video oluşturma teknikleri
- **HTML kompozisyon (HyperFrames):** `cd hf && npx hyperframes render --quality high --output ../out/visual.mp4`
  Kamera planı (zaman, x, y, ölçek) + karaoke parçaları JSON olarak şablona gömülür.
- **Yazı katmanları:** Playwright ile şeffaf PNG (başlık, ay etiketleri, soru kartı):
  `page.locator('div').screenshot({path, omitBackground:true})`
- **Kare kare üretim (Python):** PIL ile her kareyi çiz, ham görüntüyü ffmpeg'e boru ile ver:
  ```python
  ff=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-',
                       '-c:v','libx264','-crf','14','-pix_fmt','yuv420p','-movflags','+faststart','out.mp4'],stdin=subprocess.PIPE)
  ff.stdin.write(frame.tobytes())
  ```
- **Kesintisiz döngü (loop):** Her hareketin periyodu video süresine tam bölünsün (10 sn video → 1,25 / 2,5 / 5 sn).
  `u=(t%P)/P`, hareket `sin(2πu)` → son kare ilk kareye bağlanır.
- **12 ay ızgarası:** Kapaktan 12 bölge kes, 3x4 kare yerleştir, her karenin içinde kendi döngüsü
  (uçak yönünde kayma, füze yönünde kayma, alev titremesi = kırmızı piksellerin parlaklığını sinüsle oynat, kalp atışı zoom, dalga sallanması).
  Gerçek nesne animasyonu (füzenin kendi uçması) için görüntüden-videoya AI aracı gerekir (kredili).
- **Sona kart + ses ekleme:**
  ```bash
  ffmpeg -i in.mp4 -loop 1 -i card.png -i line.wav -filter_complex \
  "[0:v]tpad=stop_mode=clone:stop_duration=3.8[v0];[v0][1:v]overlay=enable='gte(t,20.0)':shortest=1,format=yuv420p[v];\
   [0:a]apad=pad_dur=3.8,afade=t=out:st=20.3:d=3.6[m];[2:a]adelay=20250|20250[vo];\
   [m][vo]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.75[a]" -map "[v]" -map "[a]" -t 24.2 out.mp4
  ```
  Kart, altyazı alanının üstüne gelsin (eski altyazı kelimesi arkadan görünmesin; opak plaka).
- **Kalite kontrol:** süre, `loudnorm` ölçümü (-14 LUFS), siyah/donuk kare yok, birkaç anın kare görüntüsünü yan yana koyup gözle bak.

## 7. Kapak (küçük resim)
- Dikey 1080x1920, tek net konu, iki satır büyük başlık (beyaz + renk), alt kısımda kırmızı şerit soru.
- "X mi Y mi?" konularında ikiye bölünmüş kapak; büyük insan yüzü olan kapaklar yüksek puan alır.
- Yayındaki videonun kapağını yeni videoda tekrar kullanma (izleyici karıştırır).
- vidIQ `score_thumbnail` / `score_title` ile puanla (90+ hedef) — kredili.

## 8. YouTube API (yükleme, altyazı, başlık çevirisi)
- **Kota:** günde 10.000 birim, İstanbul 11:00'de sıfırlanır. Altyazı yükleme 400, video yükleme 1.600,
  başlık/açıklama/etiket güncelleme 50, okuma 1 birim. Günde ~24 altyazı sığar.
- **Yetki — kalıcı yol (önerilen):** Kendi Google Cloud projen:
  1. console.cloud.google.com/projectcreate → proje aç
  2. YouTube Data API v3 → Enable
  3. Google Auth Platform → External, uygulama adı, e-posta; Audience → Test users → kanal Gmail'i
  4. Clients → Web application, redirect: `https://developers.google.com/oauthplayground`
  5. Playground ⚙️ → "Use your own OAuth credentials" (kendi ID + secret) → scope
     `https://www.googleapis.com/auth/youtube.force-ssl` → Authorize → Step 2'deki **kodu** Claude'a ver (Exchange'e basma)
  6. Claude kodu refresh token'a çevirir, makinede gizli dosyada tutar (asla repoya koymaz).
- **Geçici yol:** Playground'da kendi bilgilerin olmadan alınan `ya29...` token 1 saat geçerli ve Playground'un **ortak
  kotasını** kullanır (çoğu zaman dolu). Sabah 11:00 sonrası şansı en yüksek.
- **Altyazı:** `captions.insert` (multipart: JSON snippet {videoId, language, name} + .srt). Önce `captions.list` ile var olanı atla
  (otomatik ASR izleri sayılmaz).
- **Başlık çevirisi (localizations):** sadece ekle; canlı başlığı oku, çeviri dosyasındaki anahtarla eşleşmiyorsa atla.
  `defaultLanguage` yoksa snippet'i (başlık, açıklama, etiket, kategori) **aynen** geri gönder + `defaultLanguage:'en'`.
  Her çeviri dile canlı açıklamayı kopyala (önce açıklama düzeltmelerini yap). Başlık ≤ 100 karakter.
- **Güncelleme güvenliği:** `videos.update part=snippet` tüm snippet'i değiştirir — eksik alan silinir. Her zaman canlıyı oku,
  sadece değişecek alanı değiştir, sonra geri okuyup başlık/etiket/açıklamanın korunduğunu doğrula.
- **Yorum sabitleme API'de yok:** yorumu API ile gönder (`commentThreads.insert`, 50 birim), sabitlemeyi Studio'dan yap.

## 9. Altyazı çevirisi (çok dil)
- İngilizce SRT'nin zamanlarını koru, sadece metni cümle cümle çevir; her dil için aynı sayıda satır (assert ile kontrol).
- Kullanılan diller: en, tr, es, pt, de, fr, ja, hi, ur, ar, ps (Peştuca), fa (Farsça/Dari), ru.
- Bilmediğin dilleri satarken "AI destekli çeviri" diye belirt.

## 10. Başlık ve açıklama
- Ana arama ifadesi başlıkta ("who built the pyramids", "noah's ark") + 2-3 hashtag (#shorts #history ...).
- Açıklama: ilk satır kanca, kısa özet, kaynak listesi, görsel kredileri, "Narration/Music" kaynağı, hashtag'ler.
- Etiketler: vidIQ `keyword_research`'ten yüksek hacimli + yükselen ifadeler, kanal adı etiketi.

## 11. Planlı görevler (Claude Code bulut oturumu)
- Kota sıfırlanınca çalışacak görevler kur (ör. her gün 11:05 İstanbul): altyazı yükle, başlık çevirisi ekle, etiket ekle.
- Görev metni kendi başına anlaşılır olsun: hangi komut, hangi yetki dosyası, yetki yoksa sahibine ne denecek.
- Uzun bekleme işleri için arka planda yeniden deneme döngüsü (kota 403 → 6-20 sn bekle → tekrar), token süresi bitince dur.

## 12. Para ve büyüme (gerçekçi notlar)
- Shorts geliri düşük (500 bin izlenme ≈ 15-40 $); para uzun videolardan, sponsorluktan gelir. Tutan Short → 8-12 dk uzun video.
- İlk 30 gün: haftada 3-7 Short, "İzlendi/Kaydırıldı" oranı %60+ hedef, en iyi konuya yüklen; 30. günde veriyle karar ver.
- İkamet ülkesi gerçek ülke olmalı (AdSense/vergi); hizmet ihracatı için mali müşavir.

## 13. Başka hesapta işe başlarken örnek mesaj
"Bu PLAYBOOK'a göre çalış. Kanal: Or So The Story Goes. Yeni bir Short yapacağız: [konu]. Önce kaynaklı bir senaryo
(55 sn, kanca + efsane + 'Or so the story goes' + kanıt + döngü soru) ve Türkçe çevirisini yaz; kredi harcamadan önce sor."
