# [1] Norman D. Cook, Harmony Perception: Harmoniousness is More Than the Sum of
# Interval Consonance, 2009, Kansai University, Takatsuki, Osaka, Japan

import math
from typing import List, Optional

from chordinstability.lib.tones import initialize_tones, Tone


def dissonance(
    chord: List[float],
    amplitude_function=lambda n: 1 / (n + 1),
    num_partials: int = 4,
    tones: Optional[Tone] = None,
) -> float:
    """Calculate dissonance: The smaller the interval the higher the dissonance.

    Parameters
    ----------
    chord:
        List of pitch classes. 0 is c, 1 is c#, etc.
        Microtonal pitches are supported, e.g. 0.5
    amplitude_function:
        A function that receives the index n of the partials [fundamental, *harmonics],
        and returns a float indicating the amplitude of it. Usually falling the higher
        n is.
    num_partials:
        How many partials to use in the calculation. 1 means "only the fundamental",
        2 would add the first overtone, which is an octave.
        Defaults to 4, because that shows dips for the perfect fourth and fifth.
        Increasing this gives more accurate results for chords spread farther
        apart.
    tones:
        If provided, you can use this list of (pitch, amplitude) to overwrite the
        automatic amplitude calculation.
    """
    if len(chord) <= 1:
        return 0

    # remove duplicates
    chord = list(set(chord))

    tones = tones or initialize_tones(
        chord,
        amplitude_function,
        num_partials,
    )

    dissonances = []
    for f, first in enumerate(tones):
        for s, second in enumerate(tones):
            if s <= f:
                continue

            # first and second might be harmonics, or the fundamental,
            # it doesn't matter.
            v = first[1] * second[1]

            dissonance_ = D(abs(first[0] - second[0]), v)
            dissonances.append(dissonance_)

    return sum(dissonances) / len(chord) ** 2


def D(x, v):
    # Using the formula from the paper [1].
    # "b1 specifies the interval of maximal dissonance" [1]
    beta_1 = -0.8
    # "b2 specifies the steepness of the fall from maximal dissonance" [1]
    beta_2 = -1.6
    beta_3 = 4.0

    # [1] Eq. 1
    return v * beta_3 * (math.e ** (beta_1 * x) - math.e ** (beta_2 * x))
