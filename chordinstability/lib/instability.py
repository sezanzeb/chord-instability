from typing import Optional, List

from chordinstability import dissonance
from chordinstability.lib.tension import tension
from chordinstability.lib.tones import Tone


def instability(
    chord: List[float],
    tones: Optional[Tone] = None,
) -> float:
    """Shorthand to calculate instability using the default arguments for tension and
    dissonance.

    Parameters
    ----------
    chord:
        List of pitch classes. 0 is c, 1 is c#, etc.
        Microtonal pitches are supported, e.g. 0.5
    tones:
        If provided, you can use this list of (pitch, amplitude) to overwrite the
        automatic amplitude calculation.
    """
    dissonance_ = dissonance(chord=chord, tones=tones)
    tension_ = tension(chord=chord, tones=tones)
    instability_ = tension_ + dissonance_
    return instability_
