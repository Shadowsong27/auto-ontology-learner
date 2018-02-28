from common import BaseKeywordExtractor

import nltk


class PosKeywordExtractor(BaseKeywordExtractor):

    def tag(self):
        text = nltk.word_tokenize("And now for something completely different")
        tags = nltk.pos_tag(text)
        print(tags)


if __name__ == '__main__':
    PosKeywordExtractor().tag()
