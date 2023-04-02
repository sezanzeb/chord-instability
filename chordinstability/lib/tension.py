# [1] Norman D. Cook, Harmony Perception: Harmoniousness is More Than the Sum of
# Interval Consonance, 2009, Kansai University, Takatsuki, Osaka, Japan

import math
from typing import Optional, List

from chordinstability.lib.tones import initialize_tones, Tone


def tension(
    chord: List[float],
    tones: Optional[Tone] = None,
) -> float:
    """Calculate tension: Equidistant chords have high tension.

    This looks at the pitch-class, instead of the actual pitch. So the number of
    partials and amplitude function are not configurable.

    Parameters
    ----------
    chord:
        List of pitch classes. 0 is c, 1 is c#, etc.
        Microtonal pitches are supported, e.g. 0.5
    tones:
        If provided, you can use this list of (pitch, amplitude) to overwrite the
        automatic amplitude calculation.
    """
    if len(chord) <= 1:
        return 0

    # move upper notes down an octave, if they are very high. This fixes
    # unexpected peaks for a (0, 12, 24) chord, which should be very consonant.
    # In other words: Calculate this based on the pitch-class instead of the pitch.
    chord = [tone % 12 for tone in chord]
    # remove duplicates
    chord = list(set(chord))

    tones = tones or initialize_tones(
        chord,
        amplitude_function=lambda n: 1,
        num_partials=2,
    )

    # Examples:
    # - The tritone has a high tension, because it is equidistant between the lower
    # note and the first harmonic of the lower note.
    # - Augmented and diminished chords have high tension.

    tensions = []
    for f, first in enumerate(tones):
        for s, second in enumerate(tones):
            if s <= f:
                continue

            for t, third in enumerate(tones):
                if t <= s:
                    continue

                # first, second and third might be harmonics, or the fundamental,
                # it doesn't matter.
                v = first[1] * second[1] * third[1]
                x = abs(first[0] - second[0])
                y = abs(second[0] - third[0])

                # also possible: v * 1 / (abs(x - y) + 1)**2
                tension_ = T(x, y, v)
                tensions.append(tension_)

    return sum(tensions) / len(chord) ** 3


def T(x, y, v):
    # "a (≈0.6) is a parameter that determines the steepness of the fall from
    # maximal tension" [1]
    alpha = 0.6

    # [1] Eq. 2
    return v * math.e ** (-(((y - x) / alpha) ** 2))
