from common import BaseTokenizer
import re


class SentenceTokenizer(BaseTokenizer):

    GENERAL_REGEX = "(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s"

    def tokenize(self, text):
        return re.split(self.GENERAL_REGEX, text)


if __name__ == '__main__':

    t = SentenceTokenizer()
    for item in t.tokenize(""):
        print("=========")
        print(item)
