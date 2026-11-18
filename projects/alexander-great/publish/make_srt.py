"""Alexander v3 captions in 9 languages (one cue per spoken sentence group; times from ../audio/line_times.json)."""
import json
T = json.load(open('../audio/line_times.json'))
L = {
"en": [
"Alexander wept. No worlds left to conquer... or did he?",
"His mother said he was a son of Zeus.",
"At twelve, he tamed a horse no man could ride.",
"At Gordium, an oracle promised Asia to whoever untied a knot. He cut it with his sword.",
"By thirty-two, he ruled from Greece to India, and never lost a battle.",
"That's the legend. Now... let's check the sources.",
"The battles are real: Issus, Gaugamela, the Hydaspes, all won.",
"But the tears?",
"The philosopher Anaxarchus told him the universe held not one world... but infinite worlds.",
"Worlds without end.",
"And the man who had conquered everything he could reach... wept.",
"He was not lord of even one.",
"If the worlds are infinite... can anyone ever be great?"
],
"tr": [
"İskender ağladı. Fethedecek dünya kalmamıştı... öyle mi?",
"Annesi onun Zeus'un oğlu olduğunu söylerdi.",
"On iki yaşında, kimsenin binemediği bir atı evcilleştirdi.",
"Gordion'da bir kehanet, bir düğümü çözene Asya'yı vaat ediyordu. O düğümü kılıcıyla kesti.",
"Otuz iki yaşında Yunanistan'dan Hindistan'a kadar hüküm sürüyordu ve hiç savaş kaybetmemişti.",
"Bu efsane. Şimdi... kaynaklara bakalım.",
"Savaşlar gerçek: İssos, Gaugamela, Hydaspes, hepsi kazanıldı.",
"Peki ya gözyaşları?",
"Filozof Anaxarkhos ona evrende tek bir dünya değil... sonsuz sayıda dünya olduğunu söyledi.",
"Sonu olmayan dünyalar.",
"Ve ulaşabildiği her şeyi fethetmiş olan adam... ağladı.",
"Tek birinin bile efendisi değildi.",
"Dünyalar sonsuzsa... kimse gerçekten büyük olabilir mi?"
],
"es": [
"Alejandro lloró. No quedaban mundos por conquistar... ¿o no?",
"Su madre decía que era hijo de Zeus.",
"A los doce años, domó un caballo que nadie podía montar.",
"En Gordio, un oráculo prometía Asia a quien desatara un nudo. Él lo cortó con su espada.",
"A los treinta y dos, gobernaba de Grecia a la India y nunca perdió una batalla.",
"Esa es la leyenda. Ahora... revisemos las fuentes.",
"Las batallas son reales: Issos, Gaugamela, el Hidaspes, todas ganadas.",
"¿Y las lágrimas?",
"El filósofo Anaxarco le dijo que el universo no tenía un solo mundo... sino infinitos mundos.",
"Mundos sin fin.",
"Y el hombre que había conquistado todo lo que podía alcanzar... lloró.",
"No era señor ni de uno.",
"Si los mundos son infinitos... ¿puede alguien ser grande de verdad?"
],
"pt": [
"Alexandre chorou. Não havia mais mundos para conquistar... ou não?",
"Sua mãe dizia que ele era filho de Zeus.",
"Aos doze anos, domou um cavalo que ninguém conseguia montar.",
"Em Górdio, um oráculo prometia a Ásia a quem desatasse um nó. Ele o cortou com a espada.",
"Aos trinta e dois, governava da Grécia à Índia e nunca perdeu uma batalha.",
"Essa é a lenda. Agora... vamos checar as fontes.",
"As batalhas são reais: Isso, Gaugamela, o Hidaspes, todas vencidas.",
"E as lágrimas?",
"O filósofo Anaxarco lhe disse que o universo não tinha um só mundo... mas infinitos mundos.",
"Mundos sem fim.",
"E o homem que tinha conquistado tudo o que podia alcançar... chorou.",
"Não era senhor nem de um.",
"Se os mundos são infinitos... alguém pode ser realmente grande?"
],
"de": [
"Alexander weinte. Keine Welten mehr zu erobern... oder doch nicht?",
"Seine Mutter sagte, er sei ein Sohn des Zeus.",
"Mit zwölf zähmte er ein Pferd, das niemand reiten konnte.",
"In Gordion versprach ein Orakel Asien dem, der einen Knoten löst. Er durchschlug ihn mit dem Schwert.",
"Mit zweiunddreißig herrschte er von Griechenland bis Indien und verlor nie eine Schlacht.",
"Das ist die Legende. Und jetzt... prüfen wir die Quellen.",
"Die Schlachten sind echt: Issos, Gaugamela, der Hydaspes, alle gewonnen.",
"Und die Tränen?",
"Der Philosoph Anaxarchos sagte ihm, das Universum enthalte nicht eine Welt... sondern unendlich viele Welten.",
"Welten ohne Ende.",
"Und der Mann, der alles erobert hatte, was er erreichen konnte... weinte.",
"Er war nicht Herr über eine einzige.",
"Wenn die Welten unendlich sind... kann dann überhaupt jemand groß sein?"
],
"fr": [
"Alexandre a pleuré. Plus de mondes à conquérir... vraiment ?",
"Sa mère disait qu'il était fils de Zeus.",
"À douze ans, il dompta un cheval que personne ne pouvait monter.",
"À Gordion, un oracle promettait l'Asie à qui dénouerait un nœud. Il le trancha d'un coup d'épée.",
"À trente-deux ans, il régnait de la Grèce à l'Inde et n'avait jamais perdu une bataille.",
"Voilà la légende. Maintenant... vérifions les sources.",
"Les batailles sont réelles : Issos, Gaugamèles, l'Hydaspe, toutes gagnées.",
"Et les larmes ?",
"Le philosophe Anaxarque lui dit que l'univers ne contenait pas un seul monde... mais une infinité de mondes.",
"Des mondes sans fin.",
"Et l'homme qui avait conquis tout ce qu'il pouvait atteindre... pleura.",
"Il n'était le maître d'aucun.",
"Si les mondes sont infinis... quelqu'un peut-il vraiment être grand ?"
],
"ja": [
"アレクサンドロスは泣いた。征服すべき世界はもう無い…本当に？",
"母は彼をゼウスの子だと言った。",
"十二歳で、誰も乗りこなせない馬を手なずけた。",
"ゴルディオンでは、結び目を解いた者にアジアを与えるという神託があった。彼はそれを剣で断ち切った。",
"三十二歳でギリシャからインドまでを支配し、一度も戦いに負けなかった。",
"これが伝説だ。では…史料を確かめよう。",
"戦いは本物だ。イッソス、ガウガメラ、ヒュダスペス、すべて勝利。",
"では涙は？",
"哲学者アナクサルコスは彼に、宇宙には世界が一つではなく…無数にあると語った。",
"果てしない世界。",
"そして手の届くすべてを征服した男は…泣いた。",
"その一つの主にさえなっていなかったのだ。",
"世界が無数にあるなら…誰かが本当に偉大になれるのだろうか？"
],
"hi": [
"सिकंदर रोया। जीतने को कोई दुनिया नहीं बची थी... या नहीं?",
"उसकी माँ कहती थी कि वह ज़ीउस का बेटा है।",
"बारह साल की उम्र में उसने एक ऐसे घोड़े को काबू किया जिस पर कोई नहीं बैठ पाता था।",
"गोर्डियम में एक भविष्यवाणी थी कि जो गाँठ खोलेगा, उसे एशिया मिलेगा। उसने उसे तलवार से काट दिया।",
"बत्तीस साल की उम्र तक वह यूनान से भारत तक राज करता था, और कभी कोई लड़ाई नहीं हारा।",
"यह किंवदंती है। अब... स्रोतों की जाँच करते हैं।",
"लड़ाइयाँ सच्ची हैं: इसस, गौगामेला, झेलम (हाइडस्पीज़), सब जीतीं।",
"लेकिन आँसू?",
"दार्शनिक अनाक्सार्कस ने उससे कहा कि ब्रह्मांड में एक नहीं... अनगिनत दुनियाएँ हैं।",
"अंतहीन दुनियाएँ।",
"और जिस आदमी ने अपनी पहुँच की हर चीज़ जीत ली थी... वह रो पड़ा।",
"वह एक का भी स्वामी नहीं था।",
"अगर दुनियाएँ अनगिनत हैं... तो क्या कोई सच में महान हो सकता है?"
],
"ur": [
"سکندر رویا۔ فتح کرنے کو کوئی دنیا باقی نہیں تھی... یا نہیں؟",
"اس کی ماں کہتی تھی کہ وہ زیوس کا بیٹا ہے۔",
"بارہ سال کی عمر میں اس نے ایک ایسا گھوڑا سدھایا جس پر کوئی سوار نہیں ہو پاتا تھا۔",
"گورڈیم میں ایک پیشگوئی تھی کہ جو گرہ کھولے گا اسے ایشیا ملے گا۔ اس نے اسے تلوار سے کاٹ دیا۔",
"بتیس سال کی عمر تک وہ یونان سے ہندوستان تک حکومت کرتا تھا، اور کبھی کوئی جنگ نہیں ہارا۔",
"یہ داستان ہے۔ اب... ذرائع کو جانچتے ہیں۔",
"جنگیں سچی ہیں: اسوس، گاگامیلا، دریائے جہلم (ہائیڈاسپیز)، سب جیتیں۔",
"لیکن آنسو؟",
"فلسفی اناکسارکس نے اسے بتایا کہ کائنات میں ایک نہیں... بے شمار دنیائیں ہیں۔",
"لامتناہی دنیائیں۔",
"اور وہ شخص جس نے اپنی پہنچ کی ہر چیز فتح کر لی تھی... رو پڑا۔",
"وہ ایک کا بھی مالک نہیں تھا۔",
"اگر دنیائیں بے شمار ہیں... تو کیا کوئی واقعی عظیم ہو سکتا ہے؟"
]
}
ts = lambda t: f"{int(t//3600):02}:{int(t%3600//60):02}:{int(t%60):02},{int(round(t%1*1000)) % 1000:03}"
for lang, lines in L.items():
    assert len(lines) == len(T), lang
    out = []
    for i, ((a, b), x) in enumerate(zip(T, lines)):
        e = min(b + 0.3, T[i + 1][0] - 0.05) if i + 1 < len(T) else b + 1.5
        out.append(f"{i+1}\n{ts(a)} --> {ts(e)}\n{x}\n")
    open(f'alexander_{lang}.srt', 'w', encoding='utf-8').write('\n'.join(out))
print('ok', len(L))
