---
title: How I taught a robot to speak
description: "A Donald Duck joke, a refusal to copy anyone's voice, and a homemade formant synthesizer that went from a beep to speech in two days."
---

I'm building a personal AI bot: something that lives in my chats, remembers what matters, and quietly handles the boring parts of my day. Sooner or later a bot like that needs a voice of its own, and I wanted one that is honestly synthetic and built from scratch.

## A duck in the yard

The bot hangs out in a Telegram group of friends called «Двор Грока · Grok's Hood». The group was already up and running by mid-November. The bot itself goes by Grok from the Hood (in Russian, «Грок Дворовый»).

It all started with a joke. I asked the bot to say a rude Russian phrase in Donald Duck's voice. It refused: it doesn't copy other people's or characters' voices. Shortly before that, a friend in the chat had asked for the voice of a well-known politician and got the same answer. Instead, the bot offered to quack with a synthesizer. "Go ahead with the synth, if you can," I said.

The first attempt was a thin beep sliding down, «пиу-пиу» in Russian, roughly "pew-pew". That sound became the nickname of the whole experiment.

```audio
src: 01_duck-beep.ogg
caption: The first quack. A toy speaker, not a duck.
```

## From quacks to phonemes

A beep is not a voice, so we went down to physics. When you speak, your vocal cords buzz at a base pitch with lots of overtones. Your mouth and throat act as filters that boost a few frequency bands, called formants. Their positions are what make an "a" sound different from an "o". Formant synthesis does the same thing with math: generate the buzz, shape it with resonances, and add hiss layers for consonants like "s" and "sh". In our case it's a chain of audio filters. There is no neural network anywhere in the sound path, and no one's voice was used for training.

That same evening the duck grew a throat, learned the rhythm of the phrase as four quacks, and finally said it as a chain of phonemes. Crude, staccato, but it was speech.

```audio
src: 07_first-phonemes.ogg
caption: The first real phonemes from the formant engine.
```

Then came smooth formant movement, a better «х», and a full tour of the Russian sounds: vowels, consonants, soft syllables, and a greeting at the end.

```audio
src: 10_russian-alphabet.ogg
caption: The whole Russian inventory, end of day one.
```

## Which voice is the robot?

The next morning I asked for a poem "in the robot voice", and the bot sent its ordinary neural voice with the caption "robot style". I pointed out that this was its normal voice and I wanted the synthesizer. For a couple of messages it insisted it had no speech synth at all, until I pointed at yesterday's alphabet: "Come on, do it with phonemes!" Since then these are two separate tools.

The robot also got a tiny markup language: each word can be given its own pitch and speed. That's enough to act out surprise.

```audio
src: 48_da-ty-chto.ogg
caption: «Да ты что? Не может быть!» ("No way! It can't be!") with pitch set per word.
```

English came the same day. Latin letters are read as English, Cyrillic as Russian, and both can be mixed in one sentence. The robot greeted an English-speaking friend in the chat, who understood the robot perfectly and only got lost in the Russian bits.

## Measuring a voice

Liking it by ear is not enough, so every version gets two numbers.

- **Speed (RTF)** is generation time divided by the length of the audio. An RTF of 0.75 means a 10-second clip takes 7.5 seconds to make. Below 1 means faster than real time.
- **WER** is the share of words a speech recognizer (Whisper) gets wrong. Lower is better: a WER of 13% means about 87% of words came through.

Each version reads the same Russian monologue and the same English sentence: "Hello, I am Grok from the Hood, the robot voice of the Team…"

```audio
ru: v1_ru.ogg
en: v1_en.ogg
caption: v1. The baseline. Whisper understood 73% of the English words.
```

Version 2 reduced unstressed vowels the way people actually speak and rebuilt the hissing sounds. Version 3 added word stress, a falling tone at the end of a phrase, a livelier tempo, and a bit of breath. English intelligibility jumped from 73% to 87%. Along the way Whisper heard "in Luxembourg" as "looks boring".

```audio
ru: v3_ru.ogg
en: v3_en.ogg
caption: v3. Livelier melody, 87% of English words recognized.
```

## Obstacles

**Hiss.** v3 sounded alive, but every sound hissed as if white noise sat under the voice. The culprit was the breath layer. v4 removed it and left the real «ш» and «с» alone.

```audio
src: v4_ru.ogg
caption: v4. Same text, clean vowels.
```

**Consonant clusters.** In Russian, neighboring consonants change each other: «вчера» is pronounced [фчера], «в кармане» is [фкармане], «сделать» is [зделать]. v5 learned this, across prepositions too, while leaving words like «свет» alone. For English, v5 came out byte-for-byte identical to v4, and I still called it "fire, way cooler than v1".

```audio
ru: v5_ru.ogg
en: v5_en.ogg
caption: v5. Voicing rules in Russian. English unchanged since v4.
```

**Metallic buzz.** All overtones started in the same phase and rang before each glottal pulse as much as after it. v6 aligned their phases with the resonators, and the buzz went away. It also dropped a second rendering pass, which made it almost twice as fast: RTF went from about 0.77 to 0.48. My rough working numbers also show Russian recognition on the monologue improving.

**Grok sounds like Brock.** The name isn't in the pronunciation dictionary, so it's assembled letter by letter, and the recognizer keeps hearing "Brock" or "Rock from the road". That's a job for the consonants iteration.

**Delivery limits.** One voice message is at most 60 seconds, and each person gets ten a day.

## What's next

[Placeholder: v6 and v7 samples. v7 works on rhythm and pauses, measured against the natural reference.]

[Placeholder: v8 to v10. Phrase melody, then consonants and transitions, including a clean "Grok from the Hood" in English, then automatic markup instead of manual brackets.]

[Placeholder: the final voice, about ten iterations in. Target: at least 80% of words recognized; tempo, pauses and melody within 10% of the reference; no hiss and no buzz. The timbre stays synthetic and never pretends to be human.]
