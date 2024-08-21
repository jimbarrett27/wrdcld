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
    words = draw(
        st.lists(
            st.text(ascii_letters + digits + punctuation, min_size=1, max_size=10),
            min_size=1,
            max_size=10,
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

        word_cloud_1 = make_word_cloud(words, seed=seed)
        word_cloud_2 = make_word_cloud(words, seed=seed)

        self.assertTrue(_two_images_are_equal(word_cloud_1, word_cloud_2))
