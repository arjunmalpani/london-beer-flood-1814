# The Bridge That Fell for a Song - soundtrack cue sheet

All sound is original: synthesized in numpy/scipy by `sfx_gen.py` / `instruments.py`, placed by `sfx.py` / `music.py`, mixed by `mix.py`.
Voice = `voice/voice.wav`, gain only (no EQ, no compression, no pitch).

## Files
| file | content |
|---|---|
| `mix.wav` | final mix, 48 kHz, stereo, 24-bit, 3,240,000 samples = 67.500 s |
| `stem_voice.wav` / `stem_music.wav` / `stem_sfx.wav` | stems at mix gain (they sum to the mix before the master limiter) |

## Master loudness (own BS.1770-4 meter)
- Integrated **-15.0 LUFS**, true peak **-1.2 dBTP**, LRA 1.1 LU, max momentary -11.9 LUFS, max short-term -14.0 LUFS
- Stems: voice -15.2 LUFS, music -25.7 LUFS, sfx -35.2 LUFS (voice gain +2.62 dB, same gain on every stem)
- Master limiter (4x oversampled look-ahead, ceiling -1.2 dBTP): max gain reduction 2.99 dB, active (>0.1 dB) on 0.59 % of samples, >0.5 dB on 0.22 %

ffmpeg ebur128 cross-check:
```
Summary:
  Integrated loudness:
    I:         -15.0 LUFS
    Threshold: -25.1 LUFS
  Loudness range:
    LRA:         1.1 LU
    Threshold: -35.1 LUFS
    LRA low:   -15.6 LUFS
    LRA high:  -14.5 LUFS
  True peak:
    Peak:       -1.2 dBFS
```

## Voice on top: per-section loudness (LUFS, integrated per stem, at mix gain)
bed = music + sfx. margin = voice - bed (integrated over the section). speech median / p10 = median and 10th percentile of the 400 ms momentary margin (voice - bed) over windows centred on spoken words.

| section (shots) | time s | voice | music | sfx | bed | margin LU | speech median LU | speech p10 LU |
|---|---|---|---|---|---|---|---|---|
| hook (1) | 0.00-4.33 | -15.3 | -25.0 | -37.7 | -24.8 | 9.5 | 10.4 | 6.5 |
| brewery (2) | 4.33-11.67 | -15.5 | -25.8 | -41.5 | -25.6 | 10.2 | 10.9 | 6.6 |
| vat (3) | 11.67-15.83 | -15.3 | -25.7 | -43.1 | -25.6 | 10.3 | 10.2 | 6.2 |
| clerk (4) | 15.83-20.40 | -15.0 | -24.8 | -36.2 | -24.5 | 9.5 | 9.8 | 5.9 |
| boss (5) | 20.40-25.00 | -15.2 | -26.2 | -43.3 | -26.2 | 11.0 | 10.7 | 6.7 |
| ferment (6) | 25.00-30.50 | -15.3 | -24.8 | -36.4 | -24.5 | 9.2 | 9.4 | 4.9 |
| strain (7) | 30.50-33.00 | -14.9 | -25.0 | -37.1 | -24.8 | 9.9 | 10.2 | 6.0 |
| bulge (8) | 33.00-35.33 | -14.6 | -47.2 | -31.8 | -31.8 | 17.1 | 18.1 | 13.3 |
| snap (9) | 35.33-40.50 | -15.0 | - | -29.0 | -29.0 | 14.0 | 21.3 | 9.7 |
| wave (10) | 40.50-44.67 | -15.2 | -29.7 | -28.5 | -28.5 | 13.3 | 16.8 | 9.6 |
| luckily (11) | 44.67-47.00 | -14.7 | -26.9 | -34.1 | -26.1 | 11.4 | 11.7 | 9.2 |
| unluckily (12) | 47.00-50.83 | -15.1 | -26.4 | -34.0 | -25.7 | 10.7 | 10.7 | 8.4 |
| teacups (13) | 50.83-55.17 | -14.9 | -25.5 | -32.3 | -24.7 | 9.8 | 12.0 | 4.5 |
| court (14) | 55.17-61.67 | -15.3 | -26.8 | -33.9 | -25.9 | 10.6 | 10.9 | 7.3 |
| steel (15) | 61.67-65.27 | -15.1 | -26.5 | -35.5 | -26.0 | 10.8 | 11.3 | 7.4 |
| twist (16) | 65.27-69.73 | -15.4 | -26.5 | -43.4 | -26.6 | 11.2 | 12.5 | 10.0 |

## Music map (original march, Bb major, 120 bpm: quarter note = footfall)
Music target per section, LU under the voice (after a -3 dB speech duck keyed from words.json): hook -9.5, town -10.5, march -10.0, bounce -10.0, whistle -9.5, tension -10.0, sway -12.0, swing -11.5, march2 -10.5, rule -11.5, tourists -11.0. Applied section gains (dB): hook -9.1, town -6.5, march -7.9, bounce -6.3, whistle -8.3, tension -8.9, sway -8.8, swing -8.5, march2 -3.9, rule -6.3, tourists -7.9, dropout -8.9.

Rides (music only, dB): 3.65-4.30 s -3.0, 23.50-24.85 s -2.0, 33.50-35.00 s -4.0, 64.50-65.20 s -3.0 - so quiet sentence-final words stay on top and the band blooms in the gaps after them. The hook's last two footfalls (3.5, 4.0) are also 3 dB lower in the SFX for '...walking across it.'

| time s | frame | music |
|---|---|---|
| 0.00 | 0 | hook: theme A1-A2 tutti, 7 whistlers, tuba/after-beats/snare; snare fill 3.0-4.3 under 'across it.' |
| 4.33 | 130 | Bb button + light clash exactly on the white flash (frame 130), then the band is gone |
| 5.00 | 150 | story: theme A1-A2 light (glock + fife, tuba on 1/3, horns on 2/4, light snare) |
| 9.00 | 270 | full band: theme A3-A8 (cymbal), boots are the bass drum |
| 15.00 | 450 | tuba switches to bouncing octaves as the bridge starts bouncing |
| 21.00 | 630 | vamp bar, no melody: room for 'Somebody starts whistling' |
| 22.25 | 668 | solo whistler: 3-note pickup D-Eb-F into theme A on 23.0 (in Bb, on the beat) |
| 23.75 | 712 | the column joins the whistling (8 more whistlers by 24.75) |
| 29.22 | 877 | whistlers falter one by one (pitch droops, 29.2-29.7): faces turn nervous |
| 29.50 | 885 | tension: F7 pedal, tuba eighths, snare drive |
| 31.00 | 930 | chromatic climb F7 - F#dim7 - Gm - G#dim7, glock ticking 16ths, snare roll crescendo |
| 33.00 | 990 | DEAD STOP on 'Then,' - music silent through the bolt, the drop and the two-feet-deep joke |
| 43.43 | 1303 | warm return: pad Bb - Eb/Bb - Bb - F7, soft low brass, vibes pendulum on each sway extreme (84 bpm) |
| 47.24 | 1417 | music-box waltz (116 bpm, 3/4): one bar per swing cycle, pizzicato oom-pah-pah |
| 48.79 | 1464 | pushes 48.79 / 50.34 / 51.89 / 53.44 = downbeats (tiny triangle ting), melody climbs each bar |
| 53.62 | 1609 | music-box run up 'higher and higher' into the march |
| 54.00 | 1620 | march returns soft and golden, 6 whistlers, theme A1-A2 |
| 56.20 | 1686 | brass stab Bb + timpani on hammer blow 1 ('rule'), F on blow 2 ('Never'), Bb + cymbal on blow 3 ('step') |
| 58.85 | 1766 | snare roll pp-mf into the rule |
| 62.00 | 1860 | relaxed tourist version: swung, laid-back vibes melody, walking pizzicato bass, brushes |
| 67.00 | 2010 | final Bb chord on 'tourists' (66.72-67.24), rings out, faded to silence at 67.5 |

## SFX events
Level convention: every EVENT has a naive level (LU vs the voice stem, as the event's max momentary loudness); applied = naive - 6 dB (standard mix rule) + distance/intensity offsets. BEDS are integrated loudness, not reduced. 'mix LUFS' = the event's max momentary loudness in the final mix (voice stem = -15.2 LUFS integrated). Column sounds also get the camera-distance low-pass and more valley reverb.

| # | time s | frame | cue | what | naive LU | applied LU | mix LUFS | pan |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.000 | 0.0 | amb_london (bed, integrated) | 1814 London city ambience | -28 | -28.0 | -43.2 | +0.00 |
| 2 | 3.933 | 118.0 | flash_whoosh | whoosh into flash | -8 | -14.0 | -29.2 | +0.00 |
| 3 | 4.500 | 135.0 | brewery_clatter | brewery workshop activity | -18 | -24.0 | -39.2 | +0.00 |
| 4 | 18.200 | 546.0 | ring_drop | 700lb iron hoop clangs to the floor | -6 | -12.0 | -27.2 | +0.20 |
| 5 | 25.200 | 756.0 | ferment_fizz | bubbling dark porter in 3500 barrels | -14 | -20.0 | -35.2 | -0.10 |
| 6 | 33.500 | 1005.0 | wood_groan | oak staves creaking and bulging under pressure | -6 | -12.0 | -27.2 | -0.20 |
| 7 | 35.800 | 1074.0 | snap_cannon | SNAP: bottom iron hoop explodes like a cannon | -2 | -8.0 | -23.2 | +0.00 |
| 8 | 37.200 | 1116.0 | wall_blow | oak staves blow out and rupture neighboring vats | -4 | -10.0 | -25.2 | +0.10 |
| 9 | 41.000 | 1230.0 | wave_crash | 15ft tidal wave of porter crashes into street | -2 | -8.0 | -23.2 | +0.00 |
| 10 | 44.500 | 1335.0 | beer_flood | beer sloshing and rushing down the street | -12 | -18.0 | -33.2 | +0.00 |
| 11 | 51.200 | 1536.0 | teacup_clinks | locals scooping beer with teacups and kettles | -10 | -16.0 | -31.2 | +0.00 |
| 12 | 56.200 | 1686.0 | gavel_1 | judge's gavel bangs on desk | -6 | -12.0 | -27.2 | -0.10 |
| 13 | 57.500 | 1725.0 | gavel_2 | judge's gavel bangs on desk | -6 | -12.0 | -27.2 | -0.10 |
| 14 | 59.800 | 1794.0 | coins_jingle | parliament tax rebate coins jingling | -8 | -14.0 | -29.2 | +0.00 |
| 15 | 63.200 | 1896.0 | steel_clank | switch to steel tanks: heavy metal ring | -6 | -12.0 | -27.2 | +0.00 |
