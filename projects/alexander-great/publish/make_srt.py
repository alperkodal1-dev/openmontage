"""Alexander captions in 9 languages, one cue per narration line (times from ../audio/line_times.json)."""
import json
T = json.load(open('../audio/line_times.json'))
L = {
"en": [
"Alexander wept. No worlds left to conquer... or did he?",
"His mother said he was a son of Zeus.",
"At twelve, he tamed a horse no man could ride.",
"At Gordium, an oracle promised Asia to whoever untied a knot. He cut it with his sword.",
"By thirty-two, he ruled from Greece to India, and never lost a battle.",
"Or so the story goes.",
"Let's start from the beginning.",
"The battles are real: Issus, Gaugamela, the Hydaspes, all won.",
"But the tears? A philosopher told him there were infinite worlds... and he wept because he hadn't conquered even one.",
"And no text from his lifetime calls him \"the Great.\" The first one we have is a Roman comedy.",
"So was he great... or did the story make him great?"
],
"tr": [
"İskender ağladı. Fethedecek dünya kalmamıştı... öyle mi?",
"Annesi onun Zeus'un oğlu olduğunu söylerdi.",
"On iki yaşında, kimsenin binemediği bir atı evcilleştirdi.",
"Gordion'da bir kehanet, bir düğümü çözene Asya'yı vaat ediyordu. O düğümü kılıcıyla kesti.",
"Otuz iki yaşında Yunanistan'dan Hindistan'a kadar hüküm sürüyordu ve hiç savaş kaybetmemişti.",
"Ya da öyle anlatılır.",
"Hadi en baştan başlayalım.",
"Savaşlar gerçek: İssos, Gaugamela, Hydaspes, hepsi kazanıldı.",
"Peki ya gözyaşları? Bir filozof ona sonsuz sayıda dünya olduğunu söyledi... ve o, tek birini bile fethedemediği için ağladı.",
"Ve onun yaşadığı döneme ait hiçbir metin ona \"Büyük\" demiyor. Elimizdeki ilk örnek bir Roma komedisi.",
"Peki o gerçekten büyük müydü... yoksa onu hikâye mi büyük yaptı?"
],
"es": [
"Alejandro lloró. No quedaban mundos por conquistar... ¿o no?",
"Su madre decía que era hijo de Zeus.",
"A los doce años, domó un caballo que nadie podía montar.",
"En Gordio, un oráculo prometía Asia a quien desatara un nudo. Él lo cortó con su espada.",
"A los treinta y dos, gobernaba de Grecia a la India y nunca perdió una batalla.",
"O eso cuenta la historia.",
"Empecemos desde el principio.",
"Las batallas son reales: Issos, Gaugamela, el Hidaspes, todas ganadas.",
"¿Y las lágrimas? Un filósofo le dijo que había infinitos mundos... y lloró porque no había conquistado ni uno.",
"Y ningún texto de su vida lo llama \"el Grande\". El primero que tenemos es una comedia romana.",
"Entonces, ¿fue grande... o lo hizo grande la historia?"
],
"pt": [
"Alexandre chorou. Não havia mais mundos para conquistar... ou não?",
"Sua mãe dizia que ele era filho de Zeus.",
"Aos doze anos, domou um cavalo que ninguém conseguia montar.",
"Em Górdio, um oráculo prometia a Ásia a quem desatasse um nó. Ele o cortou com a espada.",
"Aos trinta e dois, governava da Grécia à Índia e nunca perdeu uma batalha.",
"Ou assim diz a história.",
"Vamos começar do início.",
"As batalhas são reais: Isso, Gaugamela, o Hidaspes, todas vencidas.",
"E as lágrimas? Um filósofo lhe disse que havia infinitos mundos... e ele chorou porque não tinha conquistado nem um.",
"E nenhum texto da sua época o chama de \"o Grande\". O primeiro que temos é uma comédia romana.",
"Então, ele foi grande... ou a história o tornou grande?"
],
"de": [
"Alexander weinte. Keine Welten mehr zu erobern... oder doch nicht?",
"Seine Mutter sagte, er sei ein Sohn des Zeus.",
"Mit zwölf zähmte er ein Pferd, das niemand reiten konnte.",
"In Gordion versprach ein Orakel Asien dem, der einen Knoten löst. Er durchschlug ihn mit dem Schwert.",
"Mit zweiunddreißig herrschte er von Griechenland bis Indien und verlor nie eine Schlacht.",
"So erzählt man es jedenfalls.",
"Fangen wir von vorne an.",
"Die Schlachten sind echt: Issos, Gaugamela, der Hydaspes, alle gewonnen.",
"Und die Tränen? Ein Philosoph sagte ihm, es gebe unendlich viele Welten... und er weinte, weil er nicht einmal eine erobert hatte.",
"Und kein Text aus seiner Lebenszeit nennt ihn \"den Großen\". Der erste, den wir haben, ist eine römische Komödie.",
"War er also groß... oder hat die Geschichte ihn groß gemacht?"
],
"fr": [
"Alexandre a pleuré. Plus de mondes à conquérir... vraiment ?",
"Sa mère disait qu'il était fils de Zeus.",
"À douze ans, il dompta un cheval que personne ne pouvait monter.",
"À Gordion, un oracle promettait l'Asie à qui dénouerait un nœud. Il le trancha d'un coup d'épée.",
"À trente-deux ans, il régnait de la Grèce à l'Inde et n'avait jamais perdu une bataille.",
"C'est du moins ce qu'on raconte.",
"Reprenons depuis le début.",
"Les batailles sont réelles : Issos, Gaugamèles, l'Hydaspe, toutes gagnées.",
"Et les larmes ? Un philosophe lui dit qu'il existait une infinité de mondes... et il pleura de n'en avoir conquis aucun.",
"Et aucun texte de son vivant ne l'appelle « le Grand ». Le premier que nous ayons est une comédie romaine.",
"Alors, était-il grand... ou est-ce l'histoire qui l'a rendu grand ?"
],
"ja": [
"アレクサンドロスは泣いた。征服すべき世界はもう無い…本当に？",
"母は彼をゼウスの子だと言った。",
"十二歳で、誰も乗りこなせない馬を手なずけた。",
"ゴルディオンでは、結び目を解いた者にアジアを与えるという神託があった。彼はそれを剣で断ち切った。",
"三十二歳でギリシャからインドまでを支配し、一度も戦いに負けなかった。",
"少なくとも、そう語られている。",
"最初から見ていこう。",
"戦いは本物だ。イッソス、ガウガメラ、ヒュダスペス、すべて勝利。",
"では涙は？ある哲学者が世界は無数にあると語ると…彼は一つも征服していないと泣いたのだ。",
"そして存命中の文献で彼を「大王」と呼ぶものは無い。現存する最初の例はローマの喜劇だ。",
"彼は偉大だったのか…それとも物語が彼を偉大にしたのか？"
],
"hi": [
"सिकंदर रोया। जीतने को कोई दुनिया नहीं बची थी... या नहीं?",
"उसकी माँ कहती थी कि वह ज़ीउस का बेटा है।",
"बारह साल की उम्र में उसने एक ऐसे घोड़े को काबू किया जिस पर कोई नहीं बैठ पाता था।",
"गोर्डियम में एक भविष्यवाणी थी कि जो गाँठ खोलेगा, उसे एशिया मिलेगा। उसने उसे तलवार से काट दिया।",
"बत्तीस साल की उम्र तक वह यूनान से भारत तक राज करता था, और कभी कोई लड़ाई नहीं हारा।",
"या ऐसा कहा जाता है।",
"चलिए शुरुआत से शुरू करते हैं।",
"लड़ाइयाँ सच्ची हैं: इसस, गौगामेला, झेलम (हाइडस्पीज़), सब जीतीं।",
"लेकिन आँसू? एक दार्शनिक ने उससे कहा कि दुनियाएँ अनगिनत हैं... और वह रोया क्योंकि उसने एक भी नहीं जीती थी।",
"और उसके जीवनकाल का कोई भी लेख उसे \"महान\" नहीं कहता। हमारे पास पहला उदाहरण एक रोमन कॉमेडी है।",
"तो क्या वह महान था... या कहानी ने उसे महान बनाया?"
],
"ur": [
"سکندر رویا۔ فتح کرنے کو کوئی دنیا باقی نہیں تھی... یا نہیں؟",
"اس کی ماں کہتی تھی کہ وہ زیوس کا بیٹا ہے۔",
"بارہ سال کی عمر میں اس نے ایک ایسا گھوڑا سدھایا جس پر کوئی سوار نہیں ہو پاتا تھا۔",
"گورڈیم میں ایک پیشگوئی تھی کہ جو گرہ کھولے گا اسے ایشیا ملے گا۔ اس نے اسے تلوار سے کاٹ دیا۔",
"بتیس سال کی عمر تک وہ یونان سے ہندوستان تک حکومت کرتا تھا، اور کبھی کوئی جنگ نہیں ہارا۔",
"یا کم از کم یہی کہا جاتا ہے۔",
"آئیے شروع سے شروع کرتے ہیں۔",
"جنگیں سچی ہیں: اسوس، گاگامیلا، دریائے جہلم (ہائیڈاسپیز)، سب جیتیں۔",
"لیکن آنسو؟ ایک فلسفی نے اسے بتایا کہ دنیائیں بے شمار ہیں... اور وہ رویا کیونکہ اس نے ایک بھی فتح نہیں کی تھی۔",
"اور اس کی زندگی کی کوئی تحریر اسے \"اعظم\" نہیں کہتی۔ ہمارے پاس پہلی مثال ایک رومی مزاحیہ ڈرامہ ہے۔",
"تو کیا وہ واقعی عظیم تھا... یا کہانی نے اسے عظیم بنایا؟"
]
}
ts = lambda t: f"{int(t//3600):02}:{int(t%3600//60):02}:{int(t%60):02},{int(round(t%1*1000)):03}"
for lang, lines in L.items():
    assert len(lines) == len(T), lang
    out = []
    for i, ((a, b), x) in enumerate(zip(T, lines)):
        e = min(b + 0.3, T[i + 1][0] - 0.05) if i + 1 < len(T) else b + 1.5
        out.append(f"{i+1}\n{ts(a)} --> {ts(e)}\n{x}\n")
    open(f'alexander_{lang}.srt', 'w', encoding='utf-8').write('\n'.join(out))
print('ok', len(L))
