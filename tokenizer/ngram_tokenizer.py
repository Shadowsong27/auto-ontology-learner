from common import BaseTokenizer
from tokenizer.sentence_tokenizer import SentenceTokenizer
import nltk


class NgramTokenizer(BaseTokenizer):

    def __init__(self):
        self.sentence_tokenizer = SentenceTokenizer()

    def tokenize(self, text):
        cleaned_text = self.remove_punctuation(text).lower()
        result = self.find_ngrams(cleaned_text.split(), 4)

        for item in result:
            print(item)

    @staticmethod
    def find_ngrams(input_list, n):
        return zip(*[input_list[i:] for i in range(n)])


if __name__ == '__main__':

    from nltk.corpus import gutenberg

    t = NgramTokenizer()
    t.tokenize(gutenberg.raw('austen-emma.txt'))
