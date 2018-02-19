from common import BaseTokenizer
from tokenizer.sentence_tokenizer import SentenceTokenizer


class NgramTokenizer(BaseTokenizer):

    def __init__(self):
        self.sentence_tokenizer = SentenceTokenizer()

    def brutal_tokenize(self, text):
        sentences = self.sentence_tokenizer.tokenize(text)
        for sentence in sentences:
            print(sentence)
            sentence = self.remove_punctuation(sentence)
            # special character such as \n
            # lower cap
            break


if __name__ == '__main__':

    from nltk.corpus import gutenberg

    t = NgramTokenizer()
    t.brutal_tokenize(gutenberg.raw('austen-emma.txt'))
