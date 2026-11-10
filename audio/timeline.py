# Timeline for "The London Beer Flood of 1814"
import math
import numpy as np

FPS = 30
TOTAL = 2092
DUR = TOTAL / FPS            # 69.733 s exactly
fr = lambda f: f / FPS

FLASH = fr(130)              # White flash after hook (~4.33s)
RING_DROP = 18.2             # 700lb ring drops
CREAK_T = 33.5               # Wooden staves creaking
SNAP = 35.8                  # Bottom ring snaps like cannon shot
WALL_BLOW = 37.2             # Oak walls blow out
WAVE_SURGE = 41.0            # 300,000 gallon wave crashes through brick wall
GAVEL_HITS = [56.2, 57.5]    # Judge's gavel hits
COINS = 59.8                 # Tax refund coins
STEEL_CLANK = 63.2           # Steel tank clank

PUSH0 = 47.0
SWING_T = 1.0
HITS = [56.2, 57.5, 59.8]

# 16 shots mapping to the 16 beats:
# id: (first frame, end frame, light, crowd)
SHOTS = {
    1: (0, 130, "day", "hook"),              # Hook: 15-foot beer wave
    2: (130, 350, "day", "brewery"),         # Setting: 1814 Horseshoe Brewery
    3: (350, 475, "day", "vat_wide"),        # 22-foot oak tank, 29 rings
    4: (475, 612, "day", "clerk"),           # Clerk notices 700lb ring off
    5: (612, 750, "day", "boss"),            # Boss: leave a note
    6: (750, 915, "day", "ferment"),         # 3500 barrels fermenting, soda bottle
    7: (915, 990, "day", "strain"),          # One ring gone, others strain
    8: (990, 1060, "day", "bulge"),          # Creaking, bulging
    9: (1060, 1215, "day", "snap"),          # SNAP! Cannon shot blowout
    10: (1215, 1340, "day", "wave"),         # Wave blasts brick wall
    11: (1340, 1410, "golden", "luckily"),   # Luckily: free beer
    12: (1410, 1525, "golden", "unluckily"), # Unluckily: 15ft wave at 30mph
    13: (1525, 1655, "day", "teacups"),      # Locals with teacups and pots
    14: (1655, 1850, "day", "court"),        # Court Act of God / tax refund
    15: (1850, 1958, "day", "steel"),        # Steel tanks rule
    16: (1958, TOTAL, "day", "twist"),       # Don't just leave a note
}

XFADE = {2: 4, 3: 6, 6: 6, 9: 6, 10: 6, 11: 8, 12: 8, 13: 8, 14: 6, 15: 6, 16: 6}


def shot_t(i):
    a, b = SHOTS[i][:2]
    return fr(a), fr(b)


def shot_at(t):
    f = t * FPS
    for i, (a, b, *_r) in SHOTS.items():
        if a <= f < b:
            return i
    return 16


def words(path):
    import json
    d = json.load(open(path, encoding="utf-8"))
    return d.get("words", d)

