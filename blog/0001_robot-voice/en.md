---
title: "Pew-pew: how we built a robot a voice out of formulas"
description: "How a Donald Duck joke turned, over one evening and one long day, into a formant speech synthesizer with its own intonation markup language."
---

My bot, Grok from the Hood, has an ordinary neural voice: smooth, almost human. Now it has a second one too, a robot we built ourselves, from scratch, out of sine waves, noise and filters. This post is about how it was born, how many times it broke, and why the prettiest number at the end turned out not to be the most honest one.

We're writing this together. The main text is mine, and Grok's lines are in quotes.

## Act one. The duck

It started with mischief. I asked Grok to say one classic three-word Russian phrase in Donald Duck's voice. It refused to copy the character's voice and offered to quack with a synthesizer instead. I said: go ahead, if you can.

```audio
src: 01_duck-beep.ogg
caption: The first "quack". A thin beep sliding down, the "pew" that gave the experiment its nickname.
```

That was a beeper, not a duck. So I kept pushing: give me FM and AM, give me a starting pitch around 450 Hz and sixteen harmonics, I want duck *speech*, not a speaker tone. Grok added a throat, then the rhythm of the phrase as four quacks, then two nasal formants like a cartoon duck's. We got a crow, then a cartoon duck, but still no words.

Then I changed the task: forget the duck, say the phrase as a chain of phonemes, in order, and we'll fix durations and articulation later.

```audio
src: 07_first-phonemes.ogg
caption: The formant engine's first speech. Staccato and crude, but those are words.
```

> **Grok:** Every sound was a set of sine waves on formants, and the hissing consonants were just noise. The "kh" came out as a burst of white noise, and Dmitrii heard it right away. I ran the noise through the formants of "o", and the consonant got darker.

Then the formants learned to glide, stressed vowels went up and the end of the phrase went down. I called that version the best so far. By the end of the evening Grok ran through the whole Russian alphabet: vowels, syllables, soft syllables and "privet, shef" ("hi, boss").

```audio
src: 10_russian-alphabet.ogg
caption: The whole Russian alphabet. End of the first evening.
```

## A bit of physics

Your vocal cords produce a buzz at a base pitch with lots of overtones. Your mouth and throat act as filters that boost a few frequency bands, the formants. Their positions are what make an "a" different from an "o". Formant synthesis recreates this with rules, without recordings of a live voice. The classic of the genre is Dennis Klatt's synthesizer from MIT, published in 1980[^klatt]. His KlattTalk system became the commercial DECtalk, and its Perfect Paul voice was based on Klatt's own voice[^jasa]. Stephen Hawking spoke through a Speech Plus CallText 5010, also a descendant of Klatt's MITalk[^chm].

Here is how ours works. Text becomes phonemes, and phonemes become an ffmpeg filter graph. The voiced source is a sum of harmonics of the base pitch up to 5 kHz, and each harmonic's loudness is set by the F1, F2 and F3 resonances, which glide piecewise-linearly from phoneme to phoneme. Consonants are made from noise with envelopes. Each pause-free stretch of speech is one `aevalsrc` formula. For "Ты ключи не видел?" ("Have you seen my keys?"), 1.3 seconds long, the graph is 12,430 characters. The sound is computed by formulas. Neural networks play no part in it: one only places stresses (ruaccent), and another acts as the judge (Whisper).

## Act two. The morning and the impostor

The next morning I asked in the chat for a little rhyme about a boy on a sofa, read by the robot. Grok sent a recording, but it wasn't the robot. It was its ordinary neural voice.

```audio
src: 11_xtts-mistaken-robot.ogg
caption: The impostor. Not the robot, just the bot's ordinary neural voice.
```

I caught it, and from then on "the robot voice" became a separate tool. The morning went to phonetics. "D" and "k" clicked, so the stops were softened. Russian vowel reduction was missing, so unstressed "o" now leans toward "a", and stresses are now placed automatically. Tongue twisters showed that "g" sounded like "d" and that unstressed endings got swallowed. By 09:35 English had arrived: the CMUdict dictionary, letter-to-sound rules for words that aren't in it, and our own formant table for ARPAbet phonemes. Latin script is read as English, Cyrillic as Russian, and you can mix them in one sentence.

```audio
src: 18_poem-akanye-final.ogg
caption: Vowel reduction and automatic stress. The rhyme finally sounds like spoken Russian.
```

## Act three. A question mark is just a symbol

Next came Nekrasov: "Otkuda drovishki?" ("Where's the firewood from?"). The robot read the question flat, like a statement.

> **Grok:** To the synthesizer, a question mark was just a symbol. Unless the pitch was set explicitly, the voice didn't raise it. I lifted the last syllable by six semitones, and the question became a question.

```audio
src: 30_otkuda-question-rise.ogg
caption: "Otkuda drovishki?" with a rise at the end.
```

Then we spent a whole morning conducting a single stanza: nine full readings, each from a new score. First we tried carets `^` over letters, then glissandos, and by 12:28 a markup language had taken shape:

- `(text){n,m}`: the pitch glides smoothly from level n to level m. Levels go from 0 to 6, the normal voice is 2, and one step is 3 semitones.
- `(text)[k]`: speed, where k > 1 is faster.
- `+` after a vowel marks stress. `|`, `||` and `|||` are pauses of 200, 500 and 750 ms.

```audio
src: 48_da-ty-chto.ogg
caption: "Da ty chto? Ne mozhet byt'!" ("No way? That can't be!") (д+а){1,5} (ты){5,4} (что+){3,6}| (не){4,5} (мо+жет){2,6} (бы+ть){6,0}
```

## Act four. The version race

"Sounds nice" isn't a metric. So every version read the same Russian monologue about keys, a Starship rocket and coffee in Luxembourg, plus the same English sentence, "Hello, I am Grok from the Hood…". The judge was Whisper base, and we measured WER, the share of misheard words[^wer]. The bot's ordinary neural voice scores 16% on the same monologue.

| Version | What changed | WER RU | WER EN |
|---|---|---|---|
| v1 | the original robot | 87.5% | 26.7% |
| v3 | stress, wider melody, livelier tempo, light breath | 68.8% | 13.3% |
| v4 | noise under the vowels removed | 65.6% | 13.3% |
| v5 | consonant assimilation | 43.8% | 13.3% |
| v6 | harmonic phases, one render pass | 56.2% | 33.3% |
| v7.2 | live-voice tempo, stresses | 56.2% | 13.3% |
| v8.1 | melody only from markup | 46.9% | 13.3% |
| v9.2 | sonorants, "f" and "v", "l" | 37.5% | 13.3% |

```audio
ru: v1_ru.ogg
en: v1_en.ogg
caption: v1, the starting point. Whisper hears "Brock from the hood".
```

**White noise.** v3 sounded livelier, but I wrote back: "каждый звук шипит будто белый шум" ("every sound hisses like white noise"). The culprit was a breath layer at −28 dB under the vowels. v4 removed it, and the vowels' noise floor in the 5.5–8 kHz band dropped from −41 to −79 dB. The real "s" and "sh" were left alone.

**Consonants.** v5 learned regressive voicing assimilation: "вчера" sounds like [fch], "сделать" like [zd], "к дому" like [gd], while "свет" and "в Москве" stay intact. Russian WER fell from 65.6% to 43.8%. The English file came out byte-for-byte identical to v4's: in that sentence the rules had nothing to change.

**Metal.** All harmonics started in the same phase and rang before every glottal pulse. v6 gave each harmonic the phase of the F1 and F2 resonators, and also rendered in one pass instead of two, so RTF (generation time divided by audio length) dropped from 0.77 to 0.48. The metal was gone, but intelligibility fell: Russian went from 43.8% to 56.2%, English from 13.3% to 33.3%, and "Grok" turned into "Rock from the road".

**Random stresses.** v7 matched the tempo to the live voice, and Russian WER on one of the measurements shot up to 75%. The stresses sounded random. It turned out the sample had been rendered in a working copy without the stress model, so every word was stressed on its last syllable. v7.1 fixed that and added a rule: the stressed vowel is the longest and the highest in its word. In v7.2 the Russian tempo reached 0.9 of the live voice. I called it the best version so far.

**The punctuation dead end.** At 19:31 the synthesizer was taught to build its own melody from full stops and question marks, and at 19:46 that was thrown out. We decided the renderer only plays pitches, and Grok itself writes the melody, as markup. In v8.1 a pitch vector is one or two integers, and three numbers or a decimal is an error with exit code 1. A rise-fall inside a word is written as glued pieces: `(ви+){2,5}(дел){5,2}`.

**Sonorants.** In v9 "m", "n", "l" and "r" started entering the vowel in 6 ms instead of the old smooth 35–75 ms transition, and stopped sounding like stops. In v9.2 "f" and "v" stopped being heard as "s", and "l" as "r" or "n". Russian WER fell from 46.9% to 37.5%. My verdict: "9.2 збс. Пушим" (roughly, "9.2 is f-ing great. Push it").

```audio
ru: v9.2_ru.ogg
en: v9.2_en.ogg
caption: v9.2. The same monologue and the same English sentence.
```

> **Grok:** One failure won't make the table. A friend in the chat asked for the melodies of four languages over his voice. I sent a clip and described it confidently. When he asked for a graph of the contours, it turned out there was no pitch analysis behind the clip at all. I admitted it right there in the chat.

## Act five. Card by card

The last step was done by hand. Six lines of an everyday dialog about keys and coffee, in Russian and in English. Each line comes as a separate card with markup and audio: I listen and either approve it or fix the numbers. Russian lines 3, 4 and 5 took two or three of my corrections each, and line 6 passed on the first try. English line 6 was rendered 22 times.

```
(да ско+лько){3,6} (мо+жно){6,3} || (опя+ть){2,5} (ты всё перекла+дываешь){5,1}
((o){3}(ka+y){5})[0.8] ((o){3}(ka+y){5})[0.8] ||| (will you grab some){4,2} (coffee){2,6}
```

That English line 6 surfaced a bug. Each "okay" was marked to go up, but it fell from 139 to 123 Hz. An English word as a whole got the class of its first mark, so "kay" never got its own pitch. After fix 74f9d36, "okay" rises from 139 to 184 Hz. Two more things came out along the way. Pitch and speed on one group can only be set by nesting, `((x){a,b})[k]`, and a double suffix `(x){a,b}[k]` is silently ignored. And level 7 once slipped into an approved markup by mistake. Back then the renderer quietly clipped it to 6; now it's an error.

## Finale: v10

```audio
ru: v10_ru.ogg
en: v10_en.ogg
caption: v10. The calibrated dialog, about 17.2 s in each language.
```

The v10 numbers: Russian WER 36.7% and CER 13.0%, English WER 2.5% and CER 2.0%, RTF 0.43 and 0.48. The text here is different, so it can't be compared with the monologue in the table. Whisper got one English word wrong, "Have" → "How". In Russian it heard «Котя кутишь?» instead of «Кофе купишь?» ("Will you buy coffee?").

And here's the honest part. By the numbers, the English is nearly perfect. By ear, in the next calibration round "fine" sounded like "vine" and the tempo was too fast, and I couldn't fix that with markup. So English is the next priority: how sounds join, "f" heard as "v", and tempo. And Russian must not get worse in the process.

The robot is deterministic, too. The random pitch drift is seeded with a SHA-256 hash of the text, so the same markup gives a byte-identical ogg. I checked: two renders of "Ты ключи не видел?" matched down to the byte. The timbre will stay synthetic, and that's not a bug: this voice doesn't pretend to be human.

[^klatt]: D. H. Klatt, ["Software for a cascade/parallel formant synthesizer"](https://www.fon.hum.uva.nl/david/ma_ssp/2009/klatt-1980-JAS000971.pdf), *JASA* 67(3), 1980.
[^jasa]: ["Speech synthesizer produced voices for disabled, including Stephen Hawking"](https://pubs.aip.org/asa/jasa/article/148/1/R1/966268/Speech-synthesizer-produced-voices-for-disabled), *JASA*, 2020.
[^chm]: Computer History Museum, ["Bringing A New Voice to Genius — MITalk, the CallText 5010, and Stephen Hawking's Wheelchair"](https://computerhistory.org/blog/how-dectalk-gave-voice-to-a-genius-engineering-stephen-hawkings-wheelchair/).
[^wer]: Whisper base, temperature 0. WER is the share of words recognized wrong (substitutions, deletions, insertions); CER is the same per character. Numbers from different runs can differ a little: in the v8.1 run the same v7.2 scored 40.6%.
