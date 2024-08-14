from wrdcld import make_word_cloud

from hypothesis import given
import hypothesis.strategies as st
from string import ascii_letters, digits, punctuation

from unittest import TestCase

@st.composite
def words_with_repeats_strategy(draw):
    words = draw(st.lists(st.text(ascii_letters+digits+punctuation, min_size=1), min_size=1))

    frequencies = draw(st.lists(st.integers(min_value=1, max_value=100), min_size=len(words), max_size=len(words)))

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
        self.assertFalse(all(pixel == background_color for pixel in word_cloud.getdata()))