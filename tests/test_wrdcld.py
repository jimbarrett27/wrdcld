from collections import Counter
from string import ascii_letters, digits, punctuation
from unittest import TestCase

import hypothesis.strategies as st
from hypothesis import given, settings
from PIL import ImageChops

from wrdcld import make_word_cloud


def _two_images_are_equal(image1, image2):
    return ImageChops.difference(image1, image2).getbbox() is None


@st.composite
def words_with_repeats_strategy(draw):
    """
    Strategy to generate a list of words with repeats
    """
    words = draw(
        st.lists(
            st.text(ascii_letters + digits + punctuation, min_size=1, max_size=10),
            min_size=1,
            max_size=50,
        )
    )

    frequencies = draw(
        st.lists(
            st.integers(min_value=1, max_value=100),
            min_size=len(words),
            max_size=len(words),
        )
    )

    all_words = []
    for word, freq in zip(words, frequencies):
        all_words.extend([word] * freq)

    return all_words


class TestWordCloud(TestCase):

    @given(words=words_with_repeats_strategy())
    def test_make_word_cloud(self, words: list[str]):
        """
        Test that a word cloud is created
        """

        background_color = (0, 0, 0)
        word_cloud = make_word_cloud(words, background_color=background_color)

        self.assertIsNotNone(word_cloud)

        no_pixels_filled = all(
            pixel == background_color for pixel in word_cloud.getdata()
        )

        self.assertFalse(no_pixels_filled)

    @settings(deadline=None)
    @given(words=words_with_repeats_strategy(), seed=st.integers())
    def test_word_cloud_reproducibility(self, words: list[str], seed: int):
        """
        Test that two word clouds with the same seed are equal
        """
        counter = Counter(words)

        word_cloud_1 = make_word_cloud(words, seed=seed)
        word_cloud_2 = make_word_cloud(counter, seed=seed)

        self.assertTrue(_two_images_are_equal(word_cloud_1, word_cloud_2))

    @settings(deadline=None)
    @given(
        words=words_with_repeats_strategy(),
        seeds=st.sets(st.integers(), min_size=2, max_size=2),
    )
    def test_word_cloud_seed_differences(
        self, words: list[str], seeds: tuple[int, int]
    ):
        """
        Test that two word clouds with different seeds are different
        """

        seed1, seed2 = seeds

        word_cloud_1 = make_word_cloud(words, seed=seed1)
        word_cloud_2 = make_word_cloud(words, seed=seed2)

        self.assertFalse(_two_images_are_equal(word_cloud_1, word_cloud_2))
