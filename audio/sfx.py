# Sound effects and ambience for "The London Beer Flood of 1814"
import math
import numpy as np
from dsp import (SR, ns, tt, rng, dbg, lp, hp, bp, peq, shelf, pan, st, place, fades, widen, make_ir, convolve_st,
                 momentary_max, integrated, colored, smooth_noise, modal)
import sfx_gen as G
import timeline as T

N = ns(T.DUR)
SFX_DB = -6.0


class Cue:
    def __init__(self, t, name, desc, gen, naive, kind="event", p=0.0, extra=0.0, lpf=None, send=0.12, group=None, cut=None):
        self.t, self.name, self.desc, self.gen, self.naive = t, name, desc, gen, naive
        self.kind, self.p, self.extra, self.lpf, self.send, self.cut = kind, p, extra, lpf, send, cut
        self.group = group or name
        self.applied = naive + (SFX_DB if kind == "event" else 0.0) + extra
        self.measured = None


def _cut(g, dur, att=0.01, rel=0.08):
    def wrap():
        x, pk = g()
        return fades(x, att, rel), pk
    return wrap


def mix_signals(*sigs):
    maxlen = max(len(s) if np.asarray(s).ndim == 1 else np.asarray(s).shape[-1] for s in sigs)
    out = np.zeros(maxlen)
    for s in sigs:
        arr = np.asarray(s, dtype=float)
        if arr.ndim == 1:
            out[:len(arr)] += arr
        else:
            out[:arr.shape[-1]] += arr.mean(0)
    return out


def cues():
    C = []
    R = rng(1814)
    rr = lambda: rng(int(R.integers(1 << 30)))
    add = C.append

    # 1. Ambience: London city streets (sparrows, distant wind, cobblestone air)
    def amb_london(dur):
        def g():
            r = rng(101)
            n = ns(dur)
            x = G.breeze(dur, r, 0.7, 0.12, 750)
            x += pan(G.bird_chirps(dur, r, 0.35, "sparrow") * 0.06, 0.4)
            return fades(x, 0.3, 0.5), 0.0
        return g

    add(Cue(0.0, "amb_london", "1814 London city ambience", amb_london(T.DUR), -28, "bed", send=0.0))

    # 2. Hook reverse whoosh into white flash
    add(Cue(T.FLASH - 0.4, "flash_whoosh", "whoosh into flash",
            lambda: (G.whoosh(0.7, rng(130), 0.38, 250, 2200, 0.9, 0.1, 0.15), 0.38), -8, send=0.15))

    # 3. Brewery crowd murmur / clatter in shot 2
    add(Cue(4.5, "brewery_clatter", "brewery workshop activity",
            lambda: (fades(pan(G.rattle(2.5, rng(202), 15.0), -0.2) * 0.4, 0.2, 0.3), 0.0), -18, send=0.1))

    # 4. Ring drop: 700lb iron ring slipping off at 18.2s
    def ring_drop():
        r = rng(700)
        s1 = G.hammer_hit(r, big=1.2) * 0.8
        s2 = fades(G.rattle(0.6, r, 45.0, heavy=True), 0.01, 0.15) * 0.5
        return mix_signals(s1, s2), 0.0

    add(Cue(T.RING_DROP, "ring_drop", "700lb iron hoop clangs to the floor", ring_drop, -6, p=0.2, send=0.2))

    # 5. Fermentation bubbling & carbon dioxide pressure in vats (shots 6-8)
    def ferment_fizz(dur):
        def g():
            r = rng(3500)
            n = ns(dur)
            x = G.bubbles(dur, r, 45.0, f_lo=200, f_hi=1800) * 0.7
            x += colored(n, r, 0.5) * 0.08
            return fades(x, 0.4, 0.4), 0.0
        return g

    add(Cue(25.2, "ferment_fizz", "bubbling dark porter in 3500 barrels", ferment_fizz(9.5), -14, p=-0.1, send=0.15))

    # 6. Wood groaning & creaking under 20 tons outward pressure (shot 8)
    def wood_groan():
        r = rng(888)
        s1 = G.creak(1.8, r, rate0=70, rate1=140, rough=0.2) * 1.1
        s2 = G.timber_tear(r, dur=0.9) * 0.6
        return mix_signals(s1, s2), 0.0

    add(Cue(T.CREAK_T, "wood_groan", "oak staves creaking and bulging under pressure", wood_groan, -6, p=-0.2, send=0.2))

    # 7. THE SNAP: Bottom ring explodes like a cannon shot! (35.8s)
    def snap_cannon():
        r = rng(1814)
        s1 = G.bolt_snap(r) * 1.5
        s2 = G.wood_crack(r) * 1.2
        return mix_signals(s1, s2), 0.0

    add(Cue(T.SNAP, "snap_cannon", "SNAP: bottom iron hoop explodes like a cannon", snap_cannon, -2, p=0.0, send=0.25))

    # 8. Oak blowout & wall explosion (37.2s)
    def wall_blow():
        r = rng(999)
        s1 = G.timber_tear(r, dur=1.2) * 1.2
        s2 = G.wood_crack(r) * 1.0
        return mix_signals(s1, s2), 0.0

    add(Cue(T.WALL_BLOW, "wall_blow", "oak staves blow out and rupture neighboring vats", wall_blow, -4, p=0.1, send=0.2))

    # 9. TIDAL WAVE: 300,000 gallon surge crashes brick wall (41.0s)
    def wave_crash():
        r = rng(320000)
        s1 = G.splash_big(r) * 1.4
        s2 = G.whoosh(1.8, r, 0.3, 150, 1600, 0.9, 0.2, 0.25) * 1.2
        return mix_signals(s1, s2), 0.0

    add(Cue(T.WAVE_SURGE, "wave_crash", "15ft tidal wave of porter crashes into street", wave_crash, -2, p=0.0, send=0.3))

    # 10. Water/beer flooding streets ambience (shots 11-13)
    def beer_flood(dur):
        def g():
            r = rng(777)
            x = G.water_bed(dur, r, close=1.1, slosh_rate=1.2)
            return fades(x, 0.4, 0.5), 0.0
        return g

    add(Cue(44.5, "beer_flood", "beer sloshing and rushing down the street", beer_flood(11.0), -12, send=0.15))

    # 11. Locals cheer & clinking teacups/pots (shots 13)
    def teacup_clinks():
        r = rng(1313)
        n = ns(3.5)
        x = np.zeros((2, n))
        for _ in range(8):
            tm = float(r.uniform(0.1, 3.2))
            pos = float(r.uniform(-0.6, 0.6))
            c_audio = G.clink(r, f0=float(r.uniform(1800, 3200)), dur=0.18) * 0.6
            place(x, pan(c_audio, pos), tm)
        return fades(x, 0.1, 0.2), 0.0

    add(Cue(51.2, "teacup_clinks", "locals scooping beer with teacups and kettles", teacup_clinks, -10, send=0.2))

    # 12. Court gavel hits (shot 14)
    for k, tm in enumerate(T.GAVEL_HITS):
        add(Cue(tm, f"gavel_{k+1}", "judge's gavel bangs on desk",
                lambda k=k: (G.hammer_hit(rng(550 + k), big=0.9), 0.0), -6, p=-0.1, send=0.18))

    # 13. Tax refund coins jingle (59.8s)
    def coins_jingle():
        r = rng(9999)
        n = ns(1.5)
        x = np.zeros((2, n))
        for _ in range(6):
            tm = float(r.uniform(0.05, 1.2))
            c_audio = G.clink(r, f0=float(r.uniform(3400, 4800)), dur=0.15) * 0.7
            place(x, pan(c_audio, float(r.uniform(-0.3, 0.3))), tm)
        return fades(x, 0.05, 0.1), 0.0

    add(Cue(T.COINS, "coins_jingle", "parliament tax rebate coins jingling", coins_jingle, -8, send=0.2))

    # 14. Steel tank industrial clang (shot 15, 63.2s)
    add(Cue(T.STEEL_CLANK, "steel_clank", "switch to steel tanks: heavy metal ring",
            lambda: (G.hammer_hit(rng(8888), big=1.3), 0.0), -6, p=0.0, send=0.25))

    return C


def render(v_ref, on_event=None):
    """v_ref = integrated loudness of the voice stem (stereo). Returns (stereo stem, cue list with measured levels)."""
    C = cues()
    out = np.zeros((2, N))
    send = np.zeros(N)
    for c in C:
        try:
            x, anchor = c.gen()
            x = np.asarray(x, float)
            x = pan(x, c.p) if x.ndim == 1 else x
            if c.cut is not None:
                k = ns(c.cut - (c.t - anchor))
                if 0 < k < x.shape[1]:
                    x = fades(x[:, :k], 0.0, 0.02)
            tgt = v_ref + c.applied
            cur = momentary_max(x) if c.kind == "event" else integrated(x)
            if np.isfinite(cur):
                x = x * dbg(tgt - cur)
            if c.lpf:
                x = lp(x, c.lpf, 1)
            c.measured = momentary_max(x) - v_ref if c.kind == "event" else integrated(x) - v_ref
            t0 = c.t - anchor
            place(out, x, t0)
            if on_event:
                on_event(c, x, t0)
            if c.send > 0:
                G._place_mono(send, c.send * x.mean(0), t0)
        except Exception as e:
            print(f"Error on cue {c.name}: {e}")

    street_rev = make_ir(0.8, 1814, pre=0.015, hf=1.2)
    out += 0.35 * convolve_st(send, street_rev)
    out = hp(out, 25, 2)
    end = ns(T.DUR - 0.12)
    out[:, end:] *= np.linspace(1, 0, N - end)[None, :] ** 2
    return out, C

