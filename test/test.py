import unittest

from chordinstability import instability
from chordinstability.lib.tones import _calculate_harmonic_series


class TestRelative(unittest.TestCase):
    """Test by relatively comparing values with those from other chords.

    No matter how the output is exactly shaped, a good model should pass all of
    those, given that the tests here make sense. More tests are appreciated.
    """

    def test_different_chord_sizes(self):
        # the model adjusts the magnitude of the output to make chords of various
        # sizes comparable
        c_9 = instability([0, 4, 7, 11, 14])
        c_maj7 = instability([0, 4, 7, 11])
        halfsteps = instability([0, 1, 2, 3, 4])
        minor_second = instability([0, 1])
        perfect_fifth = instability([0, 7])

        self.assertListEqual(
            sorted([halfsteps, c_maj7, perfect_fifth, minor_second, c_9]),
            [perfect_fifth, c_maj7, c_9, minor_second, halfsteps],
        )

    def test_three_halfsteps(self):
        d_major = instability([2, 6, 9])
        three_halfsteps = instability([2, 3, 4])
        self.assertGreater(three_halfsteps, d_major)

    def test_sus4(self):
        f_major_1 = instability([5, 9, 12])
        f_major_2 = instability([0, 5, 9])
        f_sus_4 = instability([5, 10, 12])

        self.assertGreater(f_sus_4, f_major_1)
        self.assertGreater(f_sus_4, f_major_2)

    def test_octave_stack(self):
        # they should be very stable
        a = instability([0, 12, 24])
        b = instability([3, 15, 27])

        self.assertAlmostEqual(a, 0, delta=0.01)
        self.assertAlmostEqual(b, 0, delta=0.01)

    def test_aug_halfsteps(self):
        aug = instability([0, 4, 8])
        halfsteps = instability([0, 1, 2])  # sounds much more dissonant to me

        self.assertGreater(halfsteps, aug)

    def test_fourths_stack(self):
        # - two stacked tritones sound less stable than two stacked fourths
        # - two stacked thirds sound less stable than two stacked fourths
        # I'm not sure how the tritones and the thirds compare though from listening
        # experiments
        tritones = instability([0, 6, 12])
        fourths = instability([0, 5, 10])
        thirds = instability([0, 4, 8])

        self.assertGreater(tritones, fourths)
        self.assertGreater(thirds, fourths)

    def test_intervals(self):
        # insert various intervals and test their instabilities. This should be
        # independent of the starting point
        def test(offset):
            m2 = instability([offset, 1 + offset])
            M3 = instability([offset, 4 + offset])
            p4 = instability([offset, 5 + offset])
            t = instability([offset, 6 + offset])
            p5 = instability([offset, 7 + offset])
            octave = instability([offset, 12 + offset])

            # sorted from stable to unstable
            self.assertListEqual(
                sorted([m2, M3, p4, t, p5, octave]),
                [octave, p5, p4, M3, t, m2],
            )

        test(0)  # c
        test(9)  # a
        test(11)  # b

    def test_idk(self):
        a = instability([0, 4, 14])  # c e d
        b = instability([0, 2, 10])  # c d a#  (sounds more dissonant to me)
        self.assertGreater(b, a)

    def test_idk2(self):
        a = instability([0, 8, 10])  # c g# a#  (sounds more dissonant to me)
        b = instability([0, 10, 14])  # c a# d
        self.assertGreater(a, b)


class TestRedundantPitches(unittest.TestCase):
    """Specifying notes twice in the input."""

    def test_perfect_fifth_redundancy(self):
        # C + C + G (intervals 0, 7)
        # should be the same (perfect fifth) as
        # C + G + G (intervals 7, 0)

        a = instability(chord=[0, 0, 7])
        b = instability(chord=[0, 7, 7])
        self.assertAlmostEqual(a, b, delta=0.01)

    def test_intervals_2(self):
        # same as test_intervals, but it is a 3-chord with 0 as the first interval.
        def calculate_(offset, size):
            return instability(chord=[offset, offset, size + offset])

        def test(offset):
            m2 = calculate_(offset, 1)
            M3 = calculate_(offset, 4)
            p4 = calculate_(offset, 5)
            t = calculate_(offset, 6)
            p5 = calculate_(offset, 7)
            octave = calculate_(offset, 12)

            # sorted from stable to unstable
            self.assertListEqual(
                sorted([octave, m2, M3, p4, t, p5]),
                [octave, p5, p4, M3, t, m2],
            )

        test(0)  # c
        test(9)  # a
        test(11)  # b

    def test_intervals_3(self):
        # same as test_intervals_2, but the upper interval is 0
        def calculate_(offset, size):
            return instability(chord=[offset, size + offset, size + offset])

        def test(offset):
            m2 = calculate_(offset, 1)
            M3 = calculate_(offset, 4)
            p4 = calculate_(offset, 5)
            t = calculate_(offset, 6)
            p5 = calculate_(offset, 7)
            octave = calculate_(offset, 12)

            # sorted from stable to unstable
            self.assertListEqual(
                sorted([octave, m2, M3, p4, t, p5]),
                [octave, p5, p4, M3, t, m2],
            )

        test(0)  # c
        test(9)  # a
        test(11)  # b


class TestUtils(unittest.TestCase):
    def test_calculate_harmonic_series(self):
        self.assertListEqual(
            list(_calculate_harmonic_series(6).round(3)),
            [0.0, 12.0, 19.02, 24.0, 27.863, 31.02],
        )


class TestAbsolute(unittest.TestCase):
    """Test by comparing with expected absolute values.

    If the model is improved, those values might change.
    """

    def test_f_major(self):
        f_major = instability([5, 9, 12])
        self.assertAlmostEqual(f_major, 0.1283077410107145, delta=0.001)
