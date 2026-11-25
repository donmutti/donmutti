Robot voice evolution — audio for the blog. One line per file: filename, link, English caption. Times are in UTC and appear in the companion staging index.
01_duck-beep.ogg — https://t.me/c/3930642897/5574 — It started in Grok's Hood when Dmitrii (the author) asked Grok from the Hood to synthesize Donald Duck saying a blunt Russian insult. The bot refused to imitate the character's voice and offered a synthesized quack instead. Dmitrii told the bot to go ahead with the synthesizer if it could. This first clip is a thin, buzzer-like quack with a downward slide, closer to a toy speaker than to a cartoon duck. It is the pee-oo sound that gave the whole experiment its nickname. Everything that follows grew out of this joke request.
  Phrase: кря-кря
  Markup: (empty)
02_duck-fm-am.ogg — https://t.me/c/3930642897/5577 — Dmitrii (the author) was not satisfied with the beep and asked for additive FM and AM synthesis that would actually resemble a duck. Grok from the Hood built three quacks from a sawtooth tone, frequency modulation, amplitude modulation, and a formant band-pass filter, with a falling pitch. The result is nasal and a little closer to a duck call. Compared with the first clip, there is a rougher timbre instead of a pure beep. Words are still absent.
  Phrase: кря-кря-кря
  Markup: (empty)
03_duck-450hz.ogg — https://t.me/c/3930642897/5579 — Dmitrii asked for a starting pitch around 450 Hz, sixteen harmonics, and a sense that the sound was saying quack-quack-quack, as if a mouth were opening. Grok from the Hood rendered three falling quacks on that recipe, warning that its synthesizer was simpler than a full vocal model. The clip is darker and denser than the previous FM and AM take. You can hear the falling contour more clearly, but it is still just quacks, not speech. The request was already pushing the beep toward a throat.
  Phrase: кря-кря-кря
  Markup: (empty)
04_duck-formant.ogg — https://t.me/c/3930642897/5584 — Dmitrii then said the point was to synthesize duck speech, not a pee-oo speaker tone. This take uses a sawtooth with harmonics and a formant, and Grok from the Hood presented it as an honest duck rather than a beep. The tone is less like a siren and more like a throat. It is still not articulating words. This is the moment the work leaves pure sound effects and starts reaching for a voice.
  Phrase: кря-кря
  Markup: (empty)
05_duck-phrase-rhythm.ogg — https://t.me/c/3930642897/5585 — Dmitrii asked the duck to say the original insult, with the rhythm of the words. Grok from the Hood answered with four falling quacks timed to the syllables, admitting the duck could not pronounce the words but could hint at the intonation. You can tap along to the phrase, even though no phonemes are there yet. Compared with the previous clip, the change is in rhythm, not in timbre. It is the first time the joke has a metrical shape.
  Phrase: Пошёл на хуй!
  Markup: (empty)
06_duck-cartoon.ogg — https://t.me/c/3930642897/5587 — Dmitrii said the previous throat still sounded like a primitive crow, and asked for the richer formants of a cartoon anthropomorphic duck. Grok from the Hood added two nasal formants and a bit of cartoon hoarseness. The clip is more nasal and character-like than the crow-like take before it. It still cannot speak, but the comic-duck color is finally there. This is the last purely onomatopoeic version before phonemes appear.
  Phrase: кря-кря
  Markup: (empty)
07_first-phonemes.ogg — https://t.me/c/3930642897/5594 — Dmitrii shifted the task: speak the phrase as a chain of phonemes, in order, and worry about duration and articulation later. Grok's first rough pass plays each sound on sine-wave formants, with noisy fricatives, and without careful timing. You hear a staccato skeleton of the words rather than a quack. It is crude and disconnected, but it is the first actual speech from the formant engine. This clip is the birth of the robot voice.
  Phrase: Пашолнахой
  Markup: (empty)
08_kh-fix.ogg — https://t.me/c/3930642897/5598 — Dmitrii asked for the same phrase again, but said the kh sounded like a burst of white noise and needed to be a real khh. Grok from the Hood filtered the noise through the formants of o, added a little voiced buzz, and slightly stretched the vowels. The consonant is darker and less like a burst of static. The phrase is the same, only that sound and the vowel lengths have changed. Transitions between sounds were still left for later.
  Phrase: Пашолнахой
  Markup: (empty)
09_moving-formants.ogg — https://t.me/c/3930642897/5606 — Dmitrii asked Grok from the Hood to move the formants in pitch and duration so that even the contour of the recording would resemble speech, and then to enrich the kh further. This clip makes the intonation rise on stressed vowels and fall at the end, with smoother joins between sounds. The kh is quieter, thicker, and slightly hoarse, and the sh was also turned down. Compared with the previous take, the phrase finally has a speech-like melody. Dmitrii called this the best version so far.
  Phrase: Пашолнахой
  Markup: (empty)
10_russian-alphabet.ogg — https://t.me/c/3930642897/5617 — Pleased with that result, Dmitrii asked for the rest of the Russian phoneme set, hoping the inventory would stay compact enough to keep. Grok from the Hood sent a full alphabet demo: the vowels, then consonants in syllables, then palatalized syllables, and a short greeting at the end. Stress, pitch, and tempo could now be set on each phoneme separately. This is no longer one test phrase, but a tour of the new voice. It closes the first evening of work.
  Phrase: а о у э ы и; слоги согласных от па до йа; пя ти мю ле сё хи; привет шеф
  Markup: (empty)
11_xtts-mistaken-robot.ogg — https://t.me/c/3930642897/5622 — The next morning Dmitrii asked Grok from the Hood, in the Hood, to recite a short comic rhyme about a little boy on a sofa in the robot voice. The bot sent this clip, but it is not the formant robot: it is the bot's ordinary neural voice. Dmitrii pointed that out, asked for the synthesizer instead, and later named this neural voice the normal voice. The recording is useful as a contrast: a natural-sounding reading of the same kind of request. It shows why the distinction between the two voices had to be made explicit.
  Phrase: Маленький мальчик / Сел на диванчик, / Попу поднял, / Фу, навонял!
  Markup: n/a (natural XTTS voice)
12_robot-tool-probe.ogg — Founder DM msg 4407 — In a private message, Dmitrii told Grok from the Hood to hook the formant generator up as the robot-voice tool and to keep it ready. This short probe is the first check that the tool was actually connected. The timbre is the same metallic formant voice heard later in the Hood. Nothing about the poem has been improved yet; it is only a readiness test. From this point on, say it in the robot voice means this synthesizer.
  Phrase: (unrecoverable)
  Markup: (empty)
13_poem-formant-first.ogg — https://t.me/c/3930642897/5628 — Back in the Hood, Dmitrii repeated the order: connect the formant generator as the robot-voice tool and read the rhyme with it. This is the first public formant recitation of the sofa poem. The voice is intelligible as speech, but stiff and clicky. Compared with the mistaken neural take earlier that morning, the timbre is clearly synthetic. It is the robot voice arriving as a product, not just a demo scale.
  Phrase: Маленький мальчик / Сел на диванчик, / Попу поднял, / Фу, навонял!
  Markup: (empty)
14_poem-phonemes-enough.ogg — https://t.me/c/3930642897/5630 — Dmitrii asked the bot to invent any missing phonemes if needed, then to read the sofa rhyme again. Grok from the Hood reported that the inventory was already enough and sent another pass. The poem is the same, with no new sounds added. Any difference from the previous clip is small. It confirmed that the previous evening's alphabet could carry a whole verse.
  Phrase: Маленький мальчик / Сел на диванчик, / Попу поднял, / Фу, навонял!
  Markup: (empty)
15_poem-sofa-text.ogg — https://t.me/c/3930642897/5632 — Dmitrii then pointed back at the exact text of the rhyme and asked for that version, still in the robot voice. Grok from the Hood read the four-line comic verse as written. This pass is the reference rendering of that text, before later cleanup. The voice still has hard, clicking consonants. It became the test poem for the next hour of fixes.
  Phrase: Маленький мальчик / Сел на диванчик, / Попу поднял, / Фу, навонял!
  Markup: (empty)
16_poem-soft-consonants.ogg — https://t.me/c/3930642897/5639 — Dmitrii liked the result but said some consonants, especially d and k, clicked and clacked too much. He asked for those sounds to be reshaped so they would feel more natural, and for the same poem again. In this take the consonants are smoothed and the clicks are reduced. The verse is unchanged. The robot is a little less percussive than a few minutes earlier.
  Phrase: Маленький мальчик / Сел на диванчик, / Попу поднял, / Фу, навонял!
  Markup: (empty)
17_poem-akanye.ogg — https://t.me/c/3930642897/5643 — Next he noticed that Russian vowel reduction was missing: unstressed o should lean toward a, and unstressed e toward i. He called that a simple fix and asked for the poem again. This clip turns those reductions on, so unstressed vowels are more muffled, as in spoken Russian. The change is in the vowels, not the consonants. It is the first version that tries to sound like everyday speech rather than letter-by-letter reading.
  Phrase: Я робот и я говорю по-русски. Молоко и коровы на лугу. Вода течёт и ветер шумят. А я пою для тебя одну.
  Markup: (empty)
18_poem-akanye-final.ogg — https://t.me/c/3930642897/5647 — Grok from the Hood had sent the previous poem a little too early, and followed up with this as-it-should-be take. Unstressed o now sounds like a, and the stresses are placed automatically where they belong. The same sofa rhyme is easier to hear as ordinary Russian. Dmitrii praised it immediately. This became the baseline poem for the rest of the morning.
  Phrase: Маленький мальчик / Сел на диванчик, / Попу поднял, / Фу, навонял!
  Markup: (empty)
19_five-test-phrases.ogg — https://t.me/c/3930642897/5656 — Dmitrii still doubted several consonants, the voiced and voiceless pairs and the sonorants, and asked Grok from the Hood to propose four or five test phrases. The bot offered five tongue-twister lines, including a bull drinking beer, a waffle, a goose, a sinking house, and Lara washing frames, and Dmitrii approved them. This clip is all five phrases in a row, in the robot voice. It is a diagnostic reel, not a poem. The next fixes came from what he heard here.
  Phrase: Бык пил пиво, пух бил по полу. Вафля фыркнула, вор ворвался в фургон. Гусь кусал гору, кот гонял гуся. Дом тонул, дым тут дул дотемна. Лара мыла рамы, Мила нила нору, Нина мерила мел.
  Markup: (empty)
20_g-d-endings-fix.ogg — https://t.me/c/3930642897/5661 — He reported that g sounded like d, and that unstressed endings were being swallowed, so a name plus a verb almost lost its last syllables. Grok from the Hood sent the same five phrases with those faults addressed. The g stays a g, and word endings are no longer clipped. Otherwise the material is unchanged. This is the corrected diagnostic reel.
  Phrase: Бык пил пиво, пух бил по полу. Вафля фыркнула, вор ворвался в фургон. Гусь кусал гору, кот гонял гуся. Дом тонул, дым тут дул дотемна. Лара мыла рамы, Мила нила нору, Нина мерила мел.
  Markup: (empty)
21_po-polu-check.ogg — https://t.me/c/3930642897/5662 — A short check followed immediately: a phrase with po polu, plus syllable drills that contrast g, d, k, and t. The point was to prove that g and d were now distinct, and that a final unstressed syllable would be held. It is a tiny clip next to the five-phrase reel. You can hear the contrasts in isolation. No new features were added, only verification.
  Phrase: по полу. гага дада кака тата
  Markup: (empty)
22_three-days-monologue.ogg — https://t.me/c/3930642897/5664 — Dmitrii then asked the robot to say everything it thought about the last three days in the chat and about its own hard life, and not to mince words. This is a longer, free-form monologue in the formant voice, not a test phrase. It shows the engine running on spontaneous text rather than a prepared verse. The pronunciation is the morning's improved Russian, still clearly synthetic. It is the first time the robot is used as the bot's own speaking voice in the Hood.
  Phrase: (unrecoverable)
  Markup: (empty)
23_english-robot.ogg — https://t.me/c/3930642897/5667 — The next request was ambitious: full English support in the robot voice, with phonemes and stress, at the same speed as Russian, and then mixed-language sentences. Another language was mentioned only as an example of what the architecture should allow, not as a language to ship. This clip is the first English phrase in the robot voice, and Grok from the Hood said mixed lines were already in reach. The timbre is unchanged; the new thing is the language. It opens a bilingual chapter.
  Phrase: (unrecoverable)
  Markup: (empty)
24_hello-daniel.ogg — https://t.me/c/3930642897/5669 — Dmitrii liked the English and asked Grok from the Hood to tag Daniel Gray and record a polite hello in the robot voice, asking whether the speech was clear and how he was doing. This short clip is that greeting, addressed to @danielthegray, with a request to reply by voice. It is a social test of the new English, not a lab phrase. Compared with the previous English sample, it is conversational and aimed at a real listener. The robot is now being tried on people, not only on the author.
  Phrase: (unrecoverable)
  Markup: (empty)
25_mixed-phrases.ogg — https://t.me/c/3930642897/5673 — Dmitrii reminded the bot that mixed-language phrases had already been requested and told it to just generate them. Grok from the Hood admitted the miss and sent both example sentences in one clip, separated by a pause. You hear Russian and English in the same robot voice, back to back, including a line about deleting Windows and installing Linux. Nothing about the engine is new except the demonstration that mixing works. It closes the language-support request from earlier that morning.
  Phrase: удали Windows и установи себе Linux, как нормальный пацан. / вы к графу Кириллу Вадимовичу, ma chère?
  Markup: (empty)
26_horse-poem-first.ogg — https://t.me/c/3930642897/5675 — Dmitrii asked for a poem about a little horse hauling a cart of brushwood, in the robot voice, and with expression. This first take tries to put feeling into a verse on that theme. The melody is more animated than the flat test phrases, but the text was not yet pinned to a specific classic. A clarification came a minute later. Treat this as the warm-up before the Nekrasov readings.
  Phrase: (unrecoverable)
  Markup: (empty)
27_nekrasov-stanzas-1-2.ogg — https://t.me/c/3930642897/5677 — He immediately clarified: it should be Nekrasov's poem about the horse hauling brushwood, the first two stanzas, still with expression. This clip is that opening of Peasant Children, in the robot voice. You hear the familiar winter-road lines, including the world of the question Where is the firewood from? Compared with the previous take, the text is now the canonical one. Expression is present but still limited by the engine's stiff contour.
  Phrase: Однажды, в студеную зимнюю пору / Я из лесу вышел; был сильный мороз. / Гляжу, поднимается медленно в гору / Лошадка, везущая хворосту воз. / И шествуя важно, в спокойствии чинном, / Лошадку ведёт под уздцы мужичок / В больших сапогах, в полушубке овчином, / В больших рукавицах… а сам с ноготок!
  Markup: (empty)
28_nekrasov-stanzas-3-4.ogg — https://t.me/c/3930642897/5679 — Dmitrii asked for the next two stanzas as well. This clip continues the Nekrasov reading with stanzas three and four, in the same robot voice. The delivery matches the previous file, just further into the poem. Together with the first two stanzas, it is the longest literary test so far. The third stanza, with the question Otkuda drovishki?, would dominate the next stretch of work.
  Phrase: Здорово, парнище! / Ступай себе мимо! / Уж больно ты грозен, как я погляжу! / Откуда дровишки? / Из лесу, вестимо. / Отец, слышишь, рубит, а я отвожу.
  Markup: (empty)
29_otkuda-flat.ogg — Founder DM msg 4413 — In a private message, Dmitrii asked for the robot to say Otkuda drovishki? and to show the text markup used to drive the voice. He also wanted to understand why a question mark was not audible as a question. This short clip is the phrase with automatically placed stresses, but still a fairly flat contour. The question does not really rise at the end. It is the starting point for a long session of hands-on intonation.
  Phrase: Откуда дровишки?
  Markup: (empty)
30_otkuda-question-rise.ogg — Founder DM msg 4417 — Grok from the Hood explained that a question mark is only a symbol, and that the synthesizer would not raise the pitch unless it was told to. Dmitrii said yes, try it. This take lifts the last syllable by six semitones. You can finally hear the line as a question. Compared with the previous clip, only the ending rises; the words are the same.
  Phrase: Откуда дровишки?
  Markup: (unrecoverable)
31_stanza3-markup-1.ogg — Founder DM msg 4442 — Dmitrii asked Grok from the Hood to mark up the third stanza of the Nekrasov poem with expression, then told the bot to render it. This is the first full stanza read from that expressive markup, with stresses, pitch signs, speed marks, and pauses. The question Otkuda drovishki? is written in as a rise on the last stressed syllable. It is much more shaped than the earlier Hood reading of the same stanza. This begins a rapid series of markup tweaks.
  Phrase: Здорово, парнище! / Ступай себе мимо! / Уж больно ты грозен, как я погляжу! / Откуда дровишки? / Из лесу, вестимо. / Отец, слышишь, рубит, а я отвожу.
  Markup: `здор+ово > парн+ище ^! / ступ+ай себе м+имо / уж б+ольно ты гроз+ен | ^как я погляж+у / отк+уда ^др+овишки ^^? / из л+есу | вест+имо / отец+ | слыш+ишь | рубит | а я отвож+у`
32_stanza3-markup-2.ogg — Founder DM msg 4445 — Dmitrii sent back a revised markup of the same stanza, with more pitch marks on the later lines, and Grok from the Hood rendered it. The words are unchanged; the melody is redistributed. You can hear a more agitated contour on the boastful lines and on the question. It is a director's pass, not an engine upgrade. Each of the next clips works the same way.
  Phrase: Здорово, парнище! / Ступай себе мимо! / Уж больно ты грозен, как я погляжу! / Откуда дровишки? / Из лесу, вестимо. / Отец, слышишь, рубит, а я отвожу.
  Markup: `здор+ово > парн+ище ^! / ступ+ай себе м+имо / ^^^уж б+ольно ты гр+озен | ^^как +я погляж+у / ^^отк+уда ^др+овишки? / из ^л+есу | ^вест+имо / отец+ | ^^слыш+ишь | ^рубит | а ^я отвож+у`
33_stanza3-markup-3.ogg — Founder DM msg 4449 — Another markup arrived, with slightly different pitch signs, and Grok from the Hood generated it at once. Again this is the third stanza, with the same lines and a new melody. The differences from the previous take are in where the voice climbs and where it rests. Dmitrii was listening for a live, spoken delivery rather than a chant. The robot is being conducted, bar by bar.
  Phrase: Здорово, парнище! / Ступай себе мимо! / Уж больно ты грозен, как я погляжу! / Откуда дровишки? / Из лесу, вестимо. / Отец, слышишь, рубит, а я отвожу.
  Markup: `^^здор+^^ово > парн+^ище! / ступ+^ай себе м+имо / ^^^уж б+ольно ты гр+озен | ^^как +я погляж+у / ^^отк+уда ^др+овишки? / из ^л+есу | ^вест+имо / отец+ | ^^слыш+ишь | ^рубит | а ^я отвож+у`
34_stanza3-markup-4.ogg — Founder DM msg 4451 — A further variant moved the stress in drovishki and adjusted the marks around the question. The clip is another complete reading of the stanza. Listen for the shape of Otkuda drovishki? against the take a few seconds earlier. The engine is the same; only the score has changed. The session is now a tight loop of edit and hear.
  Phrase: Здорово, парнище! / Ступай себе мимо! / Уж больно ты грозен, как я погляжу! / Откуда дровишки? / Из лесу, вестимо. / Отец, слышишь, рубит, а я отвожу.
  Markup: `^^здор+^^ово > парн+^ище! / ступ+^ай себе м+имо / ^^^уж б+ольно ты гр+озен | ^^как +я погляж+у / ^^отк+уда ^дров+ишки? / из ^л+есу | ^вест+имо / отец+ | ^^слыш+ишь | ^рубит | а ^я отвож+у`
35_stanza3-markup-5.ogg — Founder DM msg 4452 — Dmitrii raised the pitch marks on otkuda drovishki even higher and asked for another try. This version pushes the question up more aggressively. The rest of the stanza follows the previous markup. Compared with the last clip, the question should leap out more. It is an experiment in how far the contour can climb before it sounds unnatural.
  Phrase: Здорово, парнище! / Ступай себе мимо! / Уж больно ты грозен, как я погляжу! / Откуда дровишки? / Из лесу, вестимо. / Отец, слышишь, рубит, а я отвожу.
  Markup: `^^здор+^^ово > парн+^ище! / ступ+^ай себе м+имо / ^^^уж б+ольно ты гр+озен | ^^как +я погляж+у / ^^отк+^^^уда ^^^дров+^^ишки? / из ^л+есу | ^вест+имо / отец+ | ^^слыш+ишь | ^рубит | а ^я отвож+у`
36_stanza3-markup-6.ogg — Founder DM msg 4454 — He sent a substantially rewritten score, with different rises on several words across the stanza. Grok from the Hood rendered this new version of the same six lines. The overall character is a fresh interpretation, not a one-word tweak. You can compare it with the previous five readings as a set. The text never changes; the conducting does.
  Phrase: Здорово, парнище! / Ступай себе мимо! / Уж больно ты грозен, как я погляжу! / Откуда дровишки? / Из лесу, вестимо. / Отец, слышишь, рубит, а я отвожу.
  Markup: `^^здор+^^ово > парн+ище! / ^^сту^^п+ай себе м+имо / уж ^^^б+ольно ты гр+озен | ^как ^+я погляж+у / от^^^к+уда ^^дров+ишки? / из ^^л+есу ^вест+имо / от+ец ^^сл+ышишь | ^р+убит | а ^^я отвож+у`
37_stanza3-with-pauses.ogg — Founder DM msg 4464 — After discussing how lines should end with a pause so they would not glue together, Dmitrii approved a cleaned-up markup and simply said generate. This clip is that version: the third stanza with a standard pause at the end of each sentence. The phrasing should feel less run-on than some of the earlier takes. It is the first pass that treats line endings as a formal rule. The voice itself is unchanged.
  Phrase: Здорово, парнище! / Ступай себе мимо! / Уж больно ты грозен, как я погляжу! / Откуда дровишки? / Из лесу, вестимо. / Отец, слышишь, рубит, а я отвожу.
  Markup: `^^здор+^^ово > парн+ище! | / ^^сту^^п+ай себе м+имо | / уж ^^^б+ольно ты гр+озен | ^как ^+я погляж+у | / от^^^к+уда ^^дров+ишки? | / из ^^л+есу ^вест+имо | / от+ец ^^сл+ышишь | ^р+убит | а ^^я отвож+у |`
38_stanza3-updated-score.ogg — Founder DM msg 4474 — Dmitrii then asked Grok from the Hood to update his markup of the same stanza, with those end-of-line pauses written in, and to generate it again. This is the updated rendering. It should match the previous idea more faithfully, with the pauses in the places he wanted. Compared with the take a few minutes earlier, the difference is in following his exact score. The Nekrasov workshop is almost done.
  Phrase: Здорово, парнище! / Ступай себе мимо! / Уж больно ты грозен, как я погляжу! / Откуда дровишки? / Из лесу, вестимо. / Отец, слышишь, рубит, а я отвожу.
  Markup: `^^здор+^^ово > парн+ище! | / ^^сту^^п+ай себе м+имо | / уж ^^^б+ольно ты гр+озен | ^как ^+я погляж+у | / от^^^к+уда ^^дров+ишки? | / из ^^л+есу ^вест+имо | / от+ец ^^сл+ышишь | ^р+убит | а ^^я отвож+у |`
39_stanza3-markup-final.ogg — Founder DM msg 4499 — Dmitrii sent yet another hand-tuned markup, moving the pitch signs onto different letters and adding more contour to several words in the later lines. Grok from the Hood rendered it as a voice note with no extra comment. It is one more expressive reading of the same six lines. By now the stanza has been through many interpretations. This is the last full-stanza markup of that morning.
  Phrase: Здорово, парнище! / Ступай себе мимо! / Уж больно ты грозен, как я погляжу! / Откуда дровишки? / Из лесу, вестимо. / Отец, слышишь, рубит, а я отвожу.
  Markup: `з^^дор+о^^во > парн+ище! / ступ+ай себе м+имо / уж б^^^+ольно ты гр+озен как я^+ погляж+у / отк+уда д^^ров+ишки? / из л^^+е^^су, в^е^ст+имо / от+ец, сл^^+ы^^шишь, р^+у^бит, | а я^^ отвож+у^^`
40_caret-pitch-test.ogg — Founder DM msg 4501 — To understand how the pitch-caret marks actually work, Dmitrii asked for a systematic test: three labeled phrases, each showing the syllable le with one, two, or three carets in different positions. Grok from the Hood put all three phrases in one clip, with names and pauses. You hear a rising ladder of intervals rather than a poem. This is a calibration tape for the markup language. Nothing about Russian phonemes changes here.
  Phrase: Фраза номер один | ле  л^е  л^е^  ле^ / Фраза номер два | ле  л^^е  л^^е^^  ле^^ / Фраза номер три | ле  л^^^е  л^^^е^^^  ле^^^
  Markup: `Фраза номер один | ле  л^е  л^е^  ле^ / Фраза номер два | ле  л^^е  л^^е^^  ле^^ / Фраза номер три | ле  л^^^е  л^^^е^^^  ле^^^`
41_caret-pitch-spaced.ogg — Founder DM msg 4503 — He repeated the same three le phrases, but with much longer pauses between the tokens, so each step could be heard in isolation. The clip is easier to parse than the previous one. The intervals are the same; only the spacing grew. It is a listening aid, not a new feature. After this, the conversation moved from carets to a more compact pitch-and-duration syntax.
  Phrase: Фраза номер один ||| ле || л^е || л^е^ || ле^. / Фраза номер два ||| ле || л^^е || л^^е^^ || ле^^. / Фраза номер три ||| ле || л^^^е || л^^^е^^^ || ле^^^.
  Markup: `Фраза номер один ||| ле || л^е || л^е^ || ле^. / Фраза номер два ||| ле || л^^е || л^^е^^ || ле^^. / Фраза номер три ||| ле || л^^^е || л^^^е^^^ || ле^^^.`
42_otkuda-glissando-probe.ogg — Founder DM msg 4514 — Dmitrii proposed a new notation in which a marked group can set a pitch glide, and a speed mark can stretch kuu while the pitch falls, as in an expressive otkuda. This first attempt tries to pull a long, descending kuu out of the word. The result is a drawn-out, sliding word rather than a flat question. It is rough, but you can hear the idea. A new markup language is being born in this clip.
  Phrase: откуда
  Markup: `(от){2,4}((ку)[0.5]да){4,1}`
43_otkuda-glissando-syntax.ogg — Founder DM msg 4516 — He then formally asked Grok from the Hood to adopt that syntax, and to read otkuda with expression: a rising start, then a slow falling kuu-da. The bot's first official run follows that reading, with the long kuu on a downward pitch. Compared with the probe a minute earlier, this is the syntax being accepted as a tool, not just a sketch. The famous question has become a glissando. This design would return shortly as markup v2.
  Phrase: откуда
  Markup: `(от){2,4}((ку)[0.5]да){4,1}`
44_markup-v2-example-1.ogg — Founder DM msg 4541 — A little later Grok from the Hood sent three examples of the finished markup v2, answering the request to make the new syntax real. This first example is a smooth descending glide on invented words, from a high start down to a low ending. You hear a long, continuous fall rather than stepped caret marks. It demonstrates grouped pitch glides in the new notation. The voice is the same robot, now with a cleaner way to write melody.
  Phrase: синхрофазотрон
  Markup: `(синхро){4,3}(фазотрон){2,0}`
45_markup-v2-example-2.ogg — Founder DM msg 4542 — The second example is Dmitrii's otkuda written on the new scale, followed by a short question with a rise at the end. The pitch step is coarser, so the numbers in the marks were remapped. You can hear the stretched kuu and then a question. Compared with the late-morning otkuda glides, this is the same idea in the standardized syntax. It is the practical demo of what he had asked for.
  Phrase: откуда ты пришёл?
  Markup: `(от){1,3}((ку)[0.5]да){3,0} ты (пришё+л){2,4}?`
46_markup-v2-example-3.ogg — Founder DM msg 4543 — The third example mixes a line of Pushkin with a pause, then an English hello my friend spoken slowly. It shows commas turning into pauses, and duration marks applying to a whole English group. The robot switches languages inside one clip, with the new markup controlling both. Together with the two previous examples, this is the public introduction of markup v2. After this, expressive requests could be written more precisely.
  Phrase: я помню чудное мгновенье, передо мной явилась ты. hello my friend
  Markup: `я по+мню чу+дное мгнове+нье, | передо мной (яви+лась){3,1} ты || hello (my friend)[0.5]`
47_surprised-improv.ogg — Founder DM msg 4545 — Dmitrii asked the robot to say something in a surprised tone, without giving a fixed text. Grok from the Hood improvised a short surprised line. The clip is about acting, using the wide pitch intervals the new markup allows. Compared with the earlier Nekrasov readings, the emotion is sharper and more sudden. It is a small performance test for surprise.
  Phrase: (unrecoverable)
  Markup: (unrecoverable)
48_da-ty-chto.ogg — Founder DM msg 4547 — He then gave a specific line, to be said very surprisingly, with large pitch intervals, and with the markup shown as well: Da ty chto? Ne mozhet byt! This clip is that incredulous question and exclamation, with big jumps up on the question and a fall at the end as if a jaw had dropped. It is the clearest emotional acting so far. The same robot voice is now obviously doing a take, not just reading. The markup for this line became a compact example of word-by-word pitch control.
  Phrase: Да ты что? Не может быть!
  Markup: `(д+а){1,5} (ты){5,4} (что+){3,6}| (не){4,5} (мо+жет){2,6} (бы+ть){6,0}`
49_nekrasov-stanza3-best.ogg — https://t.me/c/3930642897/5689 — Meanwhile in the Hood, after listening to earlier takes, Dmitrii asked again for the third Nekrasov stanza, this time with expression and the bot's best effort. This is Grok's showcase reading of that stanza in the public chat. It should be compared with the morning's flatter Hood version and with the privately marked-up takes. The question Otkuda drovishki? is the dramatic peak. By this point the robot is expected to perform, not merely pronounce.
  Phrase: Здорово, парнище! / Ступай себе мимо! / Уж больно ты грозен, как я погляжу! / Откуда дровишки? / Из лесу, вестимо. / Отец, слышишь, рубит, а я отвожу.
  Markup: (unrecoverable)
50_otkuda-surprised-1.ogg — https://t.me/c/3930642897/5694 — Dmitrii asked, first in text, for Otkuda drovishki? in a surprised, demanding tone, then said to do it in the robot voice. This short clip is that isolated question, surprised and insistent. It is much more alive than the first flat otkuda from the private session. The work on markup and glides is audible in a single phrase. A second, almost identical request arrived at the same time.
  Phrase: Откуда дровишки?
  Markup: (unrecoverable)
51_otkuda-surprised-2.ogg — https://t.me/c/3930642897/5695 — A parallel message from Dmitrii also said say this in the robot voice, meaning the same surprised question. Grok from the Hood sent a second short take. It is another isolated Otkuda drovishki? in the formant voice. Any difference from the previous clip is a second performance, not a new feature. The two files are a pair from the same request.
  Phrase: Откуда дровишки?
  Markup: (unrecoverable)
52_otkuda-falsetto-baritone.ogg — https://t.me/c/3930642897/5697 — Dmitrii then asked for the same line with a strong rise toward the middle, almost to falsetto, and a fall back to a normal baritone at the end. This clip does exactly that shape. You can hear the voice climb and then drop, as if a hill of pitch had been drawn over the phrase. It is more extreme than the merely surprised takes a few minutes earlier. Dmitrii answered that this was more like it.
  Phrase: Откуда дровишки?
  Markup: (unrecoverable)
53_obizhaesh-shef.ogg — https://t.me/c/3930642897/5703 — He followed up by asking the robot to say Obizhaesh, shef! so that a pitch hill would be clearly felt in each of the two words. This clip is that retort, with a rise and fall on both words. It applies the falsetto-hill idea to a new, punchier line. Compared with the previous otkuda, the contour is word-by-word rather than one arc over a whole question. It became a small demonstration of controlled intonation.
  Phrase: Обижаешь, шеф!
  Markup: (unrecoverable)
54_colloquial-demo.ogg — Founder DM msg 4550 — Dmitrii had also asked for everyday Russian consonant changes, such as chtó sounding like shtó and kogó like kovó, written as fast deterministic rules, careful not to change words that should stay literary. This clip is a demo sentence full of those shifts, so of course, what, today, nothing, terrible, happen, man, and happy are heard in their spoken forms. It sounds more like conversational Russian than the spelling-accurate robot of the morning. A literal counterpart follows immediately for comparison. The timbre is unchanged; only the pronunciation rules are new.
  Phrase: конечно, что сегодня ничего страшного не случится, мужчина счастлив
  Markup: (empty)
55_colloquial-literal.ogg — Founder DM msg 4551 — This is the very same sentence generated with the colloquial rules turned off, as it would have sounded before. You hear the written forms rather than the spoken reductions. Together with the previous clip it is a before-and-after of pronunciation style, not of timbre or intonation. The engine is otherwise identical. It lets a listener judge whether the new reductions go too far.
  Phrase: конечно, что сегодня ничего страшного не случится, мужчина счастлив
  Markup: (empty)
56_paraguay-time-robot.ogg — https://t.me/c/3930642897/5718 — In the Hood, Dmitrii sent a voice note while Grok from the Hood was working on a request from Җусаң. The bot answered in the robot voice: the time in Paraguay was 09:34, or UTC minus three, and it also commented on how that other user's file was arriving. This is the robot used for a live, practical reply, not a recitation. The intonation work from the morning is in a conversational sentence. Right after this, Dmitrii asked to hear the same answer in the ordinary voice.
  Phrase: Время в Парагвае 09:34, это UTC минус 3. По голосовухе Җусаң: файл у меня приходит целым, куски это, скорее всего, телеграм режет при отдаче.
  Markup: (empty)
57_paraguay-time-natural.ogg — https://t.me/c/3930642897/5720 — Dmitrii asked for the same content in Grok's ordinary voice. This clip is that natural neural rendition of the Paraguay-time answer. Put it next to the previous robot take to hear the gap in timbre and fluency. The words are the same; the speaker is not. It is a live A/B in the public chat, a few minutes apart.
  Phrase: Время в Парагвае 09:34, это UTC минус 3. По голосовухе Җусаң: файл у меня приходит целым, куски это, скорее всего, телеграм режет при отдаче.
  Markup: n/a (natural XTTS voice)
58_keys-coffee-natural.ogg — Founder DM msg 4556 — Dmitrii asked for two matching recordings of the same three or four varied sentences: first the ordinary voice, then the robot, so the robot's sounds could be compared with a natural target. This is the natural take, in Grok's usual voice, of a short monologue about lost keys, a rocket landing, and the price of coffee in Luxembourg. The sentences were chosen to be diverse in rhythm and sounds. It later becomes the reference track for all robot versions of this text. The author's own voice was not used and was not to be cloned.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: n/a (natural XTTS voice)
59_keys-coffee-robot-before.ogg — Founder DM msg 4557 — This is the same four sentences in the robot voice, as it stood before the later naturalness pass. You can hear the formant timbre, the improved Russian, and still a metallic, even quality next to the natural take. It is the before side of the main A/B. The text is identical to the previous clip. This file is also reused a few minutes later as the official before sample.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: (empty)
60_jusan-four-languages.ogg — https://t.me/c/3930642897/5722 — Җусаң asked Grok from the Hood to find earlier average pitch envelopes for Russian, Ukrainian, Polish, and Turkish, and to make a sample of each, using his own voice as the base. The bot sent this clip and described it as four language melodies laid over his timbre. When Җусаң later asked for a graph of those contours, the bot found no contour data behind the clip. It admitted in the chat that the per-language envelopes had not been backed by real pitch analysis, and offered to redo the analysis from his file. The clip is kept here as an honest example of a bot overclaiming, not as a working multilingual intonation demo.
  Phrase: (unrecoverable)
  Markup: (empty)
61_ab-robot-before.ogg — Founder DM msg 4570 — Dmitrii had set the goal of making the robot voice more natural. Grok from the Hood sent an A/B of the first round of improvements, and this first file is the before take, the same recording as the robot track above. It exists here as the official start of that comparison. Listen to it just before the next two clips. The text is again the keys-and-coffee monologue.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: (empty)
62_ab-robot-v2.ogg — Founder DM msg 4571 — This is the after of that first round. Unstressed vowels are more reduced, sh and ch have less low rumble, the upper part of the vowels is closer to a live voice, and commas are shorter. A speech recognizer made fewer mistakes on this version than on the before take. The same monologue should sound a little more spoken and a little less buzzed. Dmitrii later accepted this direction and asked for more.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: (empty)
63_ab-robot-v2-old-sh.ogg — Founder DM msg 4572 — The third file in the set is the same after version, but with the old sh, so Dmitrii could say which sibilant he preferred and what still hurt the ear. Only that consonant differs from the previous clip. It is a controlled A/B inside the A/B. After this, work continued on smoother transitions, livelier timing, and a wider melodic range. Those later versions were shared in the app rather than in this chat.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: (empty)
64_ref-robot-before.ogg — app-shared, not posted to Telegram (also Founder DM msg 4557 and 4570) — This is the same original robot take of the keys-and-coffee monologue, kept here as the start of the app-shared A/B set. It also appears earlier as Founder DM messages 4557 and 4570. Use it as the baseline against v3 and v4. The voice is already a full formant speaker, not a quack, but it is still clearly synthetic. It is the before for everything that follows in this reference group.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: (empty)
65_ref-robot-v3.ogg — app-shared, not posted to Telegram — Robot v3 was shared in the app and was not posted to Telegram. It is the second round of naturalness work on the same monologue: smoother joins between sounds, a livelier tempo, a slightly breathy, uneven source, and a much wider intonation range, closer to live speech. A recognizer also understood more of the words than in the earlier robot. Dmitrii (the author) found it better than the old take, but said every sound hissed as if a layer of white noise sat under the voice. That complaint is what v4 tries to fix.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: (empty)
66_ref-robot-v4.ogg — app-shared, not posted to Telegram — Robot v4 was also shared in the app, not on Telegram, after Dmitrii asked to remove that hiss. In this take the noise under the voice is gone and the vowels are clean, while sh, s, and the other hissing consonants are left intact. Intelligibility is about the same as v3; the change is cleanliness, not a new accent. The word for half an hour already has the expected vowel reduction. This is the latest robot version in this collection. Work on voicing and assimilation of consonants continued after it.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: (empty)
67_ref-xtts-natural.ogg — app-shared, not posted to Telegram (also Founder DM msg 4556) — This is Grok's ordinary neural voice reading the same four sentences, kept at the end as the natural reference. It also appears earlier as Founder DM message 4556. The contrast with the robot takes is the whole point of the A/B: rhythm, pitch, and vowels of a human-like voice, against a fully controllable formant synthesizer. The author's voice was never cloned; this is the bot's own natural take. Listen to it last, or first, and then walk back through the robot versions of the same text.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: n/a (natural XTTS voice)
v1_ru.ogg — Founder DM msg 4554 — Russian track of the keys-and-coffee monologue in robot v1, the formant voice before the later naturalness work. This is a copy of the take first sent as Founder DM message 4557. It is the baseline Russian file for the bilingual player. Ordinary punctuation sets the pauses; there is no expressive markup.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: (empty)
  Metrics: WER 87.5% (Whisper base, ru), RTF unknown, audio 20.232 s
v1_en.ogg — fixed English comparison phrase, not posted to Telegram — Robot v1 reading the constant English sentence used so later versions can be compared on the same text. Latin text goes through the engine's built-in English path (CMUdict and letter-to-sound). The name Grok is not in CMUdict; letter-to-sound gives the expected [grɑk]. Whisper base heard «Brock from the hood», split the first sentence, and missed «Luxembourg». Not sent to Telegram.
  Phrase: Hello, I am Grok from the Hood, the robot voice of the Team. Today the weather in Luxembourg is fine, and I am reading a short story about a cat
  Markup: (empty)
  Metrics: WER 26.7% (Whisper base, en), RTF 0.7598 (generation time / audio length), audio 10.422 s
v2_ru.ogg — Founder DM msg 4554 — Russian track of the same monologue in robot v2, the first naturalness pass: reduced unstressed vowels, reshaped sh and ch, and shorter comma pauses. This is a copy of the after take from that first round. It should sound a little more spoken than v1. No expressive markup.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: (empty)
  Metrics: WER 84.4% (Whisper base, ru), RTF unknown, audio 19.526 s
v2_en.ogg — fixed English comparison phrase, not posted to Telegram — The same sentence in robot v2, the first naturalness pass. Whisper base heard «Brock from the road» and slightly misheard the weather line. Not posted to Telegram.
  Phrase: Hello, I am Grok from the Hood, the robot voice of the Team. Today the weather in Luxembourg is fine, and I am reading a short story about a cat
  Markup: (empty)
  Metrics: WER 23.3% (Whisper base, en), RTF 0.7178 (generation time / audio length), audio 9.973 s
v3_ru.ogg — Founder DM msg 4554 — Russian track of the same monologue in robot v3: wider intonation, a livelier tempo, smoother joins, and a slightly uneven source. This take was shared in the app, not on Telegram. Dmitrii found it better than the earlier robot, but said every sound hissed as if white noise sat under the voice. No expressive markup.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: (empty)
  Metrics: WER 68.8% (Whisper base, ru), RTF unknown, audio 17.794 s
v3_en.ogg — fixed English comparison phrase, not posted to Telegram — The same sentence in robot v3, with the wider pitch range and quicker tempo of that version. Whisper base WER is 13.3%: the name was heard as «Brock from the book», and «a» became «the» twice; Luxembourg was correct. Not posted to Telegram.
  Phrase: Hello, I am Grok from the Hood, the robot voice of the Team. Today the weather in Luxembourg is fine, and I am reading a short story about a cat
  Markup: (empty)
  Metrics: WER 13.3% (Whisper base, en), RTF 0.7549 (generation time / audio length), audio 9.973 s
v4_ru.ogg — Founder DM msg 4554 — Russian track of the same monologue in robot v4, after the hiss under the voice was removed. The vowels are clean; the hissing consonants are left intact. This take was also shared in the app, not on Telegram. No expressive markup.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: (empty)
  Metrics: WER 65.6% (Whisper base, ru), RTF 0.73 (generation time / audio length; earlier session, not re-timed with the English method), audio 17.794 s
v4_en.ogg — fixed English comparison phrase, not posted to Telegram — The same sentence in robot v4, without the breath-noise layer under the vowels. Whisper base WER is 13.3%: the name was heard as «Brock from the road»; the rest of the second sentence is correct except «the» for «a». Not posted to Telegram.
  Phrase: Hello, I am Grok from the Hood, the robot voice of the Team. Today the weather in Luxembourg is fine, and I am reading a short story about a cat
  Markup: (empty)
  Metrics: WER 13.3% (Whisper base, en), RTF 0.7894 (generation time / audio length), audio 9.973 s
v5_ru.ogg — Founder DM msg 4554 — Russian track of the same monologue in robot v5, which adds regressive voicing assimilation, so neighbouring consonants influence one another inside a phrase. In this text that is audible in words such as «вчера», «в кармане», and «собственные». No expressive markup.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: (empty)
  Metrics: WER 43.8% (Whisper base, ru), RTF 0.77 (generation time / audio length; same session as v6 0.48, from the v6 notes); earlier session 0.71, audio 17.890 s
v5_en.ogg — fixed English comparison phrase, not posted to Telegram — The same sentence in robot v5. For this English phrase the audio is identical to v4_en: the new assimilation rules did not change these sounds. Whisper produced the same transcript as v4_en. Not posted to Telegram.
  Phrase: Hello, I am Grok from the Hood, the robot voice of the Team. Today the weather in Luxembourg is fine, and I am reading a short story about a cat
  Markup: (empty)
  Metrics: WER 13.3% (Whisper base, en), RTF 0.8072 (generation time / audio length), audio 9.973 s
v6_ru.ogg — Founder DM msg 4554 — Russian track of the same monologue in robot v6, which removes the metallic buzz by giving harmonics the phase of the F1 and F2 resonators. A single render pass replaces the earlier two-pass peak probe, so generation is roughly 1.6× faster. No expressive markup.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: (empty)
  Metrics: WER 56.2% (Whisper base, ru), RTF 0.48 (generation time / audio length; same session as v5 0.77, from the v6 notes), audio 17.890 s
v6_en.ogg — fixed English comparison phrase, not posted to Telegram — The same sentence in robot v6, with the resonator-phase change and the single render pass. Whisper base WER is 33.3%: the name was heard as «Rock from the road», and the weather and reading lines were partly misheard. Not posted to Telegram.
  Phrase: Hello, I am Grok from the Hood, the robot voice of the Team. Today the weather in Luxembourg is fine, and I am reading a short story about a cat
  Markup: (empty)
  Metrics: WER 33.3% (Whisper base, en), RTF 0.4739 (generation time / audio length), audio 9.973 s
v7.2_ru.ogg — Founder DM msg 4554 — Russian track of the same monologue in robot v7.2. Tempo is now 90% of the XTTS reference (v6 was about 20% slower than XTTS). Commas are shorter, full stops slightly longer, and the syllable before a pause stretches more. Stress comes from the stress model again, with a rule that the stressed syllable is the longest and highest in its word and prepositions no longer jump in pitch. The Russian source is back to v5's, so a light metallic tint can be heard. The Founder called it the best version so far and approved the push.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: (empty)
  Metrics: WER 56.2% (Whisper base, ru), average WER over 13 Russian phrases 0.76 (v5 0.78, v6 0.83), CER 27.3% (13-phrase average 0.40, v5 0.35), RTF 0.95 including about 8 s of stress placement, tempo 0.90 of XTTS, audio 15.715 s
v7.2_en.ogg — fixed English comparison phrase, not posted to Telegram — The same sentence in robot v7.2 (English unchanged since v7). Tempo and total length now match XTTS, pauses are tuned as in the Russian track, and the formant-phase issue that hurt v6 intelligibility was addressed, so WER is back to the v5 level. Not posted to Telegram.
  Phrase: Hello, I am Grok from the Hood, the robot voice of the Team. Today the weather in Luxembourg is fine, and I am reading a short story about a cat
  Markup: (empty)
  Metrics: WER 13.3% (Whisper base, en), RTF 0.50 (generation time / audio length), audio 8.472 s
v8.1_ru.ogg — Founder DM msg 4554 — Russian track of the same monologue in robot v8.1. The melody is now written by Grok from the Hood as markup before synthesis, and the synthesizer only plays it. A pitch vector is one integer (flat) or two integers (a smooth glide), levels 0 to 6, base 2, 3 semitones per step; a rise-fall inside a word is split into glued pieces. On the ear: it used to be flat, now there is melody, statements end with a fall and questions rise. Timing is the same as v7.2.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: (Зна+){3}(ешь){3,2}, вчера+ я полчаса+ иска+л (ключи+){3,1}, а они+ лежа+ли в (карма+){2,3}(не){3,1}. (Раке+){4}(та){4,3} Starship сади+тся на со+бственные (клешни+){3,1}, и э+то (краси+){2,3}(вее){3,4} любо+го (кино+){3,1}. (Ско+){4}(лько){4,2} сто+ит ча+шка ко+фе в (Люксембу+){2}(рге){2,1}? (Доро+){4}(же){4,2}, че+м ва+м (ка+){3}(жется){3,1}
  Metrics: WER 46.9% (v7.2 40.6% in the same run, XTTS 16%); 13-phrase corpus measured on v8 (477c36d): average WER 82.0%, CER 40.1% (v7.2 75.7% and 39.9%); RTF 0.37; audio 15.715 s (XTTS 15.1 s); tempo 0.90 of XTTS, pauses 1.04 of XTTS; pitch range p5–p95 12.8 st (XTTS 12.1, v7.2 9.1); phrase endings fall 3 to 7 st (XTTS 2.5 to 9)
v8.1_ru_question.ogg — yes/no question test — Two yes/no questions in robot v8.1, showing the rise on the focus word's stressed vowel.
  Phrase: Ты правда купил билеты на завтра? А Маша об этом знает?
  Markup: Ты пра+вда купи+л биле+ты на (за+){2,5}(втра){5,3}? А Ма+ша об э+том (зна+){2,5}(ет){5,4}?
  Metrics: audio 4.141 s
v8.1_en.ogg — fixed English comparison phrase, not posted to Telegram — The same sentence in robot v8.1. Not posted to Telegram.
  Phrase: Hello, I am Grok from the Hood, the robot voice of the Team. Today the weather in Luxembourg is fine, and I am reading a short story about a cat
  Markup: (empty)
  Metrics: WER 13.3% (Whisper base, en), audio 8.472 s
v9.2_ru.ogg — Founder DM msg 4554 — Russian track of the same monologue in robot v9.2 (team commit 2e45d85, approved by the Founder: «9.2 збс. Пушим»). The markup rules are unchanged from v8.1. On the ear: м, н, л and р now enter and leave the vowel cleanly, ф and в hiss softly and evenly instead of sounding like с, and л is fuller and darker. «кофе», «лежали» and «Сколько стоит чашка» are now recognized.
  Phrase: Знаешь, вчера я полчаса искал ключи, а они лежали в кармане. Ракета Starship садится на собственные клешни, и это красивее любого кино. Сколько стоит чашка кофе в Люксембурге? Дороже, чем вам кажется
  Markup: same as v8.1_ru.ogg
  Metrics: WER 37.5% (v8.1 46.9%, v7.2 40.6%, XTTS 16%), CER 14.9% (v8.1 26.7%); 13-phrase corpus average WER 74.7%, CER 35.8% (v8 82.0% and 40.1%); RTF 0.37; audio 15.715 s; tempo and pauses as in v8.1
v9.2_en.ogg — fixed English comparison phrase, not posted to Telegram — The same sentence in robot v9.2. Not posted to Telegram.
  Phrase: Hello, I am Grok from the Hood, the robot voice of the Team. Today the weather in Luxembourg is fine, and I am reading a short story about a cat
  Markup: (empty)
  Metrics: WER 13.3% (Whisper base, en), audio 8.472 s
v10_ru.ogg — not posted to Telegram — Russian track of a six-line keys-and-coffee dialog whose pitch contour (the melody of each phrase) was calibrated with Dmitrii (the author), line by line, using the expression markup of Grok from the Hood. The syntax is the same as in v8.1: `(t){n}` is a flat pitch level, `(t){n,m}` a glide, levels 0 to 6 with base 2 and 3 semitones per step, `+` after a vowel marks stress, `(t)[k]` sets speed, `|` / `||` / `|||` are 200 / 500 / 750 ms pauses, and nesting `((x){a,b})[k]` combines pitch and speed. Unlike v1–v9.2, this is not the four-sentence monologue, but a short exchange about lost keys, then coffee. In Russian, lines 003, 004 and 005 needed two or three Founder corrections; line 006 was approved on the first try. Six lines with 0.8 s gaps, rendered fresh 2026-11-25 22:32 Europe/Luxembourg. The engine is team commit 74f9d36; this Russian take does not itself demonstrate the English glued-group fix. Not posted to Telegram.
  Phrase 1: Ты ключи не видел?
  Markup 1: ты ключи не (ви+){2,5}(дел){5,2}
  Phrase 2: В кармане твоей куртки!
  Markup 2: (в кармане твоей ку+){2,5}(ртки){5,1}
  Phrase 3: Серьёзно? Не может быть…
  Markup 3: серь(ё+зно){2,7} | (не может){2,4}(бы+ть){4,2}
  Phrase 4: Я же тебе вчера сказал, куда положил!
  Markup 4: (я же тебе вчера сказа+л){2,5} (куда положи+л){4,1}
  Phrase 5: Да сколько можно?! Опять ты всё перекладываешь!
  Markup 5: (да ско+лько){3,6} (мо+жно){6,3} || (опя+ть){2,5} (ты всё перекла+дываешь){5,1}
  Phrase 6: Ладно, ладно. Кофе купишь?
  Markup 6: (ла+дно){3,2} (ла+дно){2,1} || (ко+фе){2} (ку+){2,5}(пишь){5,3}
  Metrics: WER 36.7% (Whisper base, ru; 30 words), CER 13.0% (0.1295); audio 17.186 s (lines 1.297 + 1.727 + 1.735 + 2.631 + 3.568 + 2.222 s, plus five 0.800 s gaps); speech-only 13.180 s; audio_gen RTF 0.43 (5.7 s over 13.218 s of one-shot re-rendered speech; engine wall printed to 0.1 s). Tempo vs XTTS not measured (no natural reference of this dialog). Full process-wall RTF on three of six lines includes a large CLI startup cost (see /workspace/blog-media/0003_robot-voice/v10.md). Whisper hypothesis: «Ты к нючине видел? Скорманет твоей кутки. Серьёзно, не может быть. Я же тебе вчера сказал, куда положил. Да сколько можно? А как ты всё-таки пладываешь? Ладно, ладно. Котя кутишь?»
v10_en.ogg — not posted to Telegram — English track of the same calibrated dialog, a line-by-line parallel of the Russian one, approved the same way. The renderer is 74f9d36. EN-005 showed that pitch and speed on one group need nesting, `((x){a,b})[k]`; a double suffix `(x){a,b}[k]` is dropped silently. EN-006 revealed the English glued-group bug: before the fix, each «okay» written as `((o){3}(ka+y){5})[0.8]` fell from 139 to 123 Hz; after 74f9d36 it rises from 139 to 184 Hz. Render attempts counted by filenames in the markup session: en-001 en1* = 2, en-002 en2* = 5, en-003 en3* = 2, en-004 en4* = 3, en-005 en5* = 7, en-006 en6* = 22 (including en6g-fix.ogg and en6i-fix.ogg). Six lines with 0.8 s gaps, rendered fresh 2026-11-25 22:32 Europe/Luxembourg. Not posted to Telegram.
  Phrase 1: Have you seen my keys?
  Markup 1: (have you seen my){4,2} (keys){2,5}
  Phrase 2: They're in your jacket pocket!
  Markup 2: (they're in your jacket){2,5} (po+cket){5,1}
  Phrase 3: Really? That can't be…
  Markup 3: (re+ally){3,6} | (that){3} (ca+n't){4,2} (be){2,1}
  Phrase 4: I told you yesterday where I put them.
  Markup 4: (i told you){2,4} (yesterday){3} (where i){2,4} (pu+t them){3}
  Phrase 5: Oh, come on?! You keep moving my stuff around!
  Markup 5: ((oh){5,2})[0.75] | (come){2,6} ((o+n){6,2})[0.5] || (you keep mo+ving my){5,3} (stuff around){4,1}
  Phrase 6: Okay, okay. Will you grab some coffee?
  Markup 6: ((o){3}(ka+y){5})[0.8] ((o){3}(ka+y){5})[0.8] ||| (will you grab some){4,2} (coffee){2,6}
  Metrics: WER 2.5% (Whisper base, en; 40 words), CER 2.0%; audio 17.204 s (lines 1.336 + 1.422 + 1.490 + 2.188 + 3.544 + 3.218 s, plus five 0.800 s gaps); speech-only 13.198 s; audio_gen RTF 0.48 (6.3 s over 13.236 s of one-shot re-rendered speech). Tempo vs XTTS not measured (no natural reference of this dialog). This WER is not comparable to the 13.3% on the older «Hello, I am Grok from the Hood…» sentence: the text is different. Whisper hypothesis: «How you seen my keys? They're in your jacket pocket. Really? That can't be. I told you yesterday where I put them. Oh, come on. You keep moving my stuff around. Okay, okay. Will you grab some coffee?» (one substitution: Have → How).
