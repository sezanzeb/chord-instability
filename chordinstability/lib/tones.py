import math
from collections import namedtuple

import numpy as np


Tone = namedtuple("Tone", "pitch amplitude")


def initialize_tones(
    chord,
    amplitude_function,
    num_partials,
):
    """One element for each partial (fundamental + harmonics),
    containing pitch in halfsteps and amplitude.
    """
    chord_size = len(chord)

    amplitudes = _initialize_amplitudes(chord, num_partials, amplitude_function)
    partials = _initialize_partials(chord, num_partials)

    tones = []

    for chord_tone_index in range(chord_size):
        for p in range(num_partials):
            tones.append(
                [
                    partials[chord_tone_index][p],
                    amplitudes[chord_tone_index][p],
                ]
            )

    # sort lower pitches to the front
    tones = sorted(tones, key=lambda tone: tone[0])

    return np.array(tones)


def _calculate_harmonic_series(n):
    return np.array([12 * math.log2(i / 1) for i in range(1, n + 1)])


def _initialize_amplitudes(
    chord,
    num_partials,
    amplitude_function,
):
    """Amplitudes for each partial, per chord tone,

    Parameters
    ----------
    amplitude_function
        other amplitudes proposed by n.d.cook. n starts at 0
        A(n) = 1 / (n + 1)
        A(n) = 0.8 ** n
        A(n) = 1.0 - n * 0.1
        A(n) = 1.0
    """
    amplitudes = np.zeros((len(chord), num_partials), dtype=float)

    amplitudes[0] = [amplitude_function(n) for n in range(num_partials)]

    # TODO This is redundant at the moment, but later if the input chord contains
    #  amplitudes as well, this will make sense
    for i in range(1, len(chord)):
        amplitudes[i] = amplitudes[0]

    return amplitudes


def _initialize_partials(
    chord,
    num_partials,
):
    """The fundamental and the overtone pitches,"""
    partials = np.zeros((len(chord), num_partials), dtype=float)

    harmonic_series = _calculate_harmonic_series(num_partials)

    for i in range(0, len(chord)):
        partials[i] = np.zeros((num_partials,))
        partials[i] += chord[i]
        partials[i] += harmonic_series

    return partials
