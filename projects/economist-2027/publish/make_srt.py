"""Economist 2027 Short: caption tracks in 10 languages + localized titles/descriptions.
Cue times are from audio/words.json (pre speed-up) divided by 1.06 (the published cut is 6% faster)."""
import json
SP = 1.06
T = [(0.0, 3.9), (5.56, 6.9), (7.3, 9.5), (9.86, 15.2), (15.62, 17.4), (17.64, 22.0), (22.28, 25.4), (25.9, 27.4),
     (27.72, 32.9), (33.36, 35.7), (36.0, 39.3), (39.48, 42.0), (42.34, 45.1), (45.32, 48.1), (48.32, 49.6),
     (49.72, 53.7), (54.24, 57.6), (57.96, 63.5)]
L = {
'en': ["The Economist dropped its 2027 cover... and it's dark.", "Theory one: it's a script.", "People say it prints the future in advance.",
       "Their proof? In 1988, a cover showed a golden phoenix coin, dated 2018:", "\"Get ready for a world currency.\"",
       "Now look at 2027. At the very top, the world's leaders, lined up.", "Down below, tanks, missiles and refugee tents.", "Theory two: war.",
       "Fighter jets, and Beijing's own deadline for its army to be ready for Taiwan is... 2027.", "Theory three: AI takes over.",
       "A robot... stealing something? Mhm.", "Cameras everywhere, and a market crashing.", "And in the corner, the detail nobody can explain:",
       "a crescent, a star, and a rider on a camel.", "The magazine's only comment?", "\"All that's missing is the aliens. They probably won't appear in 2027.\"",
       "So is it a forecast... or a warning?", "Look at that corner one more time... What do you see?"],
'tr': ["The Economist 2027 kapağını yayınladı... ve kapak karanlık.", "Birinci teori: her şey senaryo.", "Derginin geleceği önceden bastığı söyleniyor.",
       "Kanıtları mı? 1988'de bir kapakta 2018 tarihli altın bir anka kuşu parası vardı:", "\"Bir dünya parasına hazır olun.\"",
       "Şimdi 2027'ye bakın. En tepede dünya liderleri, yan yana dizilmiş.", "Aşağıda tanklar, füzeler ve mülteci çadırları.", "İkinci teori: savaş.",
       "Savaş uçakları... ve Pekin'in ordusuna Tayvan için hazır olma tarihi... 2027.", "Üçüncü teori: yapay zekâ kontrolü ele alıyor.",
       "Bir robot... bir şey mi çalıyor? Hımm.", "Her yerde kameralar ve çöken bir piyasa.", "Ve köşede, kimsenin açıklayamadığı detay:",
       "bir hilal, bir yıldız ve deveye binmiş bir adam.", "Derginin tek yorumu ne mi?", "\"Bir tek uzaylılar eksik. Muhtemelen 2027'de de gelmeyecekler.\"",
       "Peki bu bir tahmin mi... yoksa bir uyarı mı?", "O köşeye bir kez daha bakın... Siz ne görüyorsunuz?"],
'es': ["The Economist publicó su portada de 2027... y es oscura.", "Teoría uno: es un guion.", "Dicen que imprime el futuro por adelantado.",
       "¿La prueba? En 1988, una portada mostró una moneda dorada con un fénix, fechada en 2018:", "\"Prepárense para una moneda mundial.\"",
       "Ahora mira 2027. En lo más alto, los líderes del mundo, en fila.", "Abajo, tanques, misiles y tiendas de refugiados.", "Teoría dos: guerra.",
       "Aviones de combate... y el plazo de Pekín para que su ejército esté listo para Taiwán es... 2027.", "Teoría tres: la IA toma el control.",
       "Un robot... ¿robando algo? Mmm.", "Cámaras por todas partes y un mercado que se desploma.", "Y en la esquina, el detalle que nadie puede explicar:",
       "una media luna, una estrella y un jinete sobre un camello.", "¿El único comentario de la revista?", "\"Solo faltan los extraterrestres. Probablemente no aparecerán en 2027.\"",
       "Entonces, ¿es un pronóstico... o una advertencia?", "Mira esa esquina una vez más... ¿Qué ves tú?"],
'pt': ["A The Economist lançou a capa de 2027... e ela é sombria.", "Teoria um: é um roteiro.", "Dizem que ela imprime o futuro com antecedência.",
       "A prova? Em 1988, uma capa mostrou uma moeda dourada com uma fênix, datada de 2018:", "\"Preparem-se para uma moeda mundial.\"",
       "Agora olhe para 2027. Lá no topo, os líderes do mundo, enfileirados.", "Lá embaixo, tanques, mísseis e tendas de refugiados.", "Teoria dois: guerra.",
       "Caças... e o prazo de Pequim para o seu exército estar pronto para Taiwan é... 2027.", "Teoria três: a IA assume o controle.",
       "Um robô... roubando alguma coisa? Hmm.", "Câmeras por toda parte e um mercado desabando.", "E no canto, o detalhe que ninguém consegue explicar:",
       "uma lua crescente, uma estrela e um cavaleiro num camelo.", "O único comentário da revista?", "\"Só faltam os alienígenas. Provavelmente não vão aparecer em 2027.\"",
       "Então, é uma previsão... ou um aviso?", "Olhe para aquele canto mais uma vez... O que você vê?"],
'de': ["The Economist hat sein Cover für 2027 veröffentlicht... und es ist düster.", "Theorie eins: Es ist ein Drehbuch.", "Man sagt, das Blatt druckt die Zukunft im Voraus.",
       "Der Beweis? 1988 zeigte ein Cover eine goldene Phönix-Münze mit der Jahreszahl 2018:", "\"Macht euch bereit für eine Weltwährung.\"",
       "Jetzt schau dir 2027 an. Ganz oben: die Mächtigen der Welt, in einer Reihe.", "Darunter: Panzer, Raketen und Flüchtlingszelte.", "Theorie zwei: Krieg.",
       "Kampfjets... und Pekings Frist, bis seine Armee bereit für Taiwan sein soll, ist... 2027.", "Theorie drei: Die KI übernimmt.",
       "Ein Roboter... der etwas stiehlt? Hm.", "Überall Kameras und ein Markt, der abstürzt.", "Und in der Ecke das Detail, das niemand erklären kann:",
       "ein Halbmond, ein Stern und ein Reiter auf einem Kamel.", "Der einzige Kommentar des Magazins?", "\"Es fehlen nur noch die Aliens. 2027 tauchen sie wohl nicht auf.\"",
       "Also: Prognose... oder Warnung?", "Schau dir diese Ecke noch einmal an... Was siehst du?"],
'fr': ["The Economist a dévoilé sa couverture 2027... et elle est sombre.", "Théorie numéro un : tout est écrit d'avance.", "On dit qu'il imprime l'avenir à l'avance.",
       "La preuve ? En 1988, une couverture montrait une pièce d'or au phénix, datée de 2018 :", "« Préparez-vous à une monnaie mondiale. »",
       "Maintenant, regardez 2027. Tout en haut, les dirigeants du monde, alignés.", "En bas, des chars, des missiles et des tentes de réfugiés.", "Théorie numéro deux : la guerre.",
       "Des avions de chasse... et l'échéance fixée par Pékin pour que son armée soit prête pour Taïwan, c'est... 2027.", "Théorie numéro trois : l'IA prend le contrôle.",
       "Un robot... qui vole quelque chose ? Hmm.", "Des caméras partout, et un marché qui s'effondre.", "Et dans le coin, le détail que personne ne sait expliquer :",
       "un croissant, une étoile et un cavalier sur un chameau.", "Le seul commentaire du magazine ?", "« Il ne manque que les extraterrestres. Ils n'apparaîtront sans doute pas en 2027. »",
       "Alors, une prévision... ou un avertissement ?", "Regardez ce coin encore une fois... Qu'y voyez-vous ?"],
'ja': ["エコノミスト誌が2027年の表紙を公開した…そして、それは暗い。", "説その1：すべては台本どおり。", "この雑誌は未来を前もって印刷していると言われている。",
       "証拠は？1988年、ある表紙に2018年と刻まれた金色のフェニックス硬貨が描かれていた：", "「世界通貨に備えよ」",
       "では2027年を見てみよう。いちばん上には、並んだ世界の指導者たち。", "その下には、戦車、ミサイル、難民のテント。", "説その2：戦争。",
       "戦闘機…そして中国が軍に台湾への備えを求めた期限は…2027年。", "説その3：AIが支配する。",
       "ロボットが…何かを盗んでいる？うーん。", "至る所にカメラ、そして崩れる市場。", "そして隅には、誰にも説明できない細部が：",
       "三日月、星、そしてラクダに乗った人物。", "雑誌の唯一のコメントは？", "「足りないのは宇宙人だけ。2027年にもおそらく現れないだろう」",
       "これは予測か…それとも警告か？", "もう一度あの隅を見てほしい…あなたには何が見える？"],
'hi': ["द इकोनॉमिस्ट ने 2027 का कवर जारी किया... और यह डरावना है।", "थ्योरी एक: सब कुछ पहले से लिखा है।", "लोग कहते हैं यह भविष्य पहले ही छाप देता है।",
       "सबूत? 1988 में एक कवर पर 2018 तारीख वाला सुनहरा फ़ीनिक्स सिक्का दिखाया गया था:", "\"एक विश्व मुद्रा के लिए तैयार हो जाइए।\"",
       "अब 2027 देखिए। सबसे ऊपर, दुनिया के नेता, कतार में।", "नीचे टैंक, मिसाइलें और शरणार्थियों के तंबू।", "थ्योरी दो: युद्ध।",
       "लड़ाकू विमान... और बीजिंग ने अपनी सेना को ताइवान के लिए तैयार रहने की जो समय-सीमा दी है, वह है... 2027।", "थ्योरी तीन: एआई कब्ज़ा कर लेगा।",
       "एक रोबोट... कुछ चुरा रहा है? हम्म।", "हर जगह कैमरे, और गिरता हुआ बाज़ार।", "और कोने में, वह बात जिसे कोई समझा नहीं पाता:",
       "एक अर्धचंद्र, एक तारा और ऊँट पर सवार एक आदमी।", "पत्रिका की इकलौती टिप्पणी?", "\"बस एलियंस की कमी है। वे शायद 2027 में भी नहीं आएँगे।\"",
       "तो यह भविष्यवाणी है... या चेतावनी?", "उस कोने को एक बार फिर देखिए... आपको क्या दिखता है?"],
'ur': ["دی اکانومسٹ نے 2027 کا سرورق جاری کیا... اور یہ تاریک ہے۔", "پہلا نظریہ: سب کچھ پہلے سے لکھا ہوا ہے۔", "لوگ کہتے ہیں یہ مستقبل پہلے ہی چھاپ دیتا ہے۔",
       "ثبوت؟ 1988 میں ایک سرورق پر 2018 کی تاریخ والا سنہری ققنس سکہ دکھایا گیا تھا:", "\"ایک عالمی کرنسی کے لیے تیار ہو جائیں۔\"",
       "اب 2027 دیکھیے۔ سب سے اوپر دنیا کے رہنما، قطار میں۔", "نیچے ٹینک، میزائل اور پناہ گزینوں کے خیمے۔", "دوسرا نظریہ: جنگ۔",
       "لڑاکا طیارے... اور بیجنگ نے اپنی فوج کو تائیوان کے لیے تیار رہنے کی جو آخری تاریخ دی ہے، وہ ہے... 2027۔", "تیسرا نظریہ: مصنوعی ذہانت قبضہ کر لے گی۔",
       "ایک روبوٹ... کچھ چرا رہا ہے؟ ہوں۔", "ہر طرف کیمرے، اور گرتی ہوئی منڈی۔", "اور کونے میں وہ تفصیل جسے کوئی بیان نہیں کر سکتا:",
       "ایک ہلال، ایک ستارہ اور اونٹ پر سوار ایک شخص۔", "رسالے کا واحد تبصرہ؟", "\"بس خلائی مخلوق کی کمی ہے۔ وہ شاید 2027 میں بھی نہیں آئیں گے۔\"",
       "تو یہ پیش گوئی ہے... یا انتباہ؟", "اس کونے کو ایک بار پھر دیکھیے... آپ کو کیا نظر آتا ہے؟"],
'ru': ["The Economist выпустил обложку на 2027 год... и она мрачная.", "Теория первая: всё написано заранее.", "Говорят, журнал печатает будущее заранее.",
       "Доказательство? В 1988 году на обложке была золотая монета с фениксом и датой 2018:", "«Готовьтесь к мировой валюте».",
       "Теперь посмотрите на 2027. На самом верху — мировые лидеры, в ряд.", "Внизу — танки, ракеты и палатки беженцев.", "Теория вторая: война.",
       "Истребители... а срок, к которому Пекин требует от армии готовности по Тайваню, — это... 2027.", "Теория третья: ИИ захватывает власть.",
       "Робот... что-то крадёт? Хм.", "Камеры повсюду и обвал рынка.", "А в углу — деталь, которую никто не может объяснить:",
       "полумесяц, звезда и всадник на верблюде.", "Единственный комментарий журнала?", "«Не хватает только инопланетян. В 2027 году они, скорее всего, не появятся».",
       "Так это прогноз... или предупреждение?", "Посмотрите на этот угол ещё раз... Что видите вы?"],
}
TITLES = {
 'tr': "The Economist 2027 Kapağını Yayınladı... ve Ürkütücü #shorts #economist",
 'es': "The Economist Publicó su Portada 2027... y Da Miedo #shorts #economist",
 'pt': "A The Economist Lançou a Capa de 2027... e É Assustadora #shorts #economist",
 'de': "The Economist hat sein Cover 2027 veröffentlicht... und es ist beängstigend #shorts",
 'fr': "The Economist dévoile sa couverture 2027... et elle fait peur #shorts #economist",
 'ja': "エコノミスト2027年の表紙が公開…そして不気味すぎる #shorts #economist",
 'hi': "द इकोनॉमिस्ट का 2027 कवर आ गया... और यह डरावना है #shorts #economist",
 'ur': "دی اکانومسٹ کا 2027 سرورق آ گیا... اور یہ خوفناک ہے #shorts #economist",
 'ru': "The Economist показал обложку 2027... и она пугает #shorts #economist",
}
ts = lambda t: f"{int(t//3600):02}:{int(t%3600//60):02}:{int(t%60):02},{int(round(t%1*1000)) % 1000:03}"
for lang, lines in L.items():
    assert len(lines) == len(T), lang
    out = [f"{i+1}\n{ts(a/SP)} --> {ts(b/SP)}\n{x}\n" for i, ((a, b), x) in enumerate(zip(T, lines))]
    open(f'economist_{lang}.srt', 'w', encoding='utf-8').write('\n'.join(out))
loc = {}
for lang, title in TITLES.items():
    assert len(title) <= 100, (lang, len(title))
    loc[lang] = {'title': title, 'description': ' '.join(L[lang][:5]) + '\n' + ' '.join(L[lang][5:]) + '\n\n#TheEconomist #Economist2027 #TheWorldAhead2027 #Shorts'}
json.dump(loc, open('localizations.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(L), 'srt,', len(loc), 'localizations')
