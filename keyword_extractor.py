import nltk
import string
import re

from nltk.corpus import gutenberg


class KeywordExtractor:

    def tag(self, text):
        text = nltk.word_tokenize(text)
        return nltk.pos_tag(text)

    def run(self):
        text = gutenberg.raw('austen-emma.txt')
        tagged_text = self.tag(text)

        pattern_dict = self.get_pos_pattern_distribution(tagged_text, 2)

        patterns = sorted(pattern_dict, key=pattern_dict.__getitem__, reverse=True)

        for pattern in patterns:
            if "NN" in pattern:
                print(pattern + " " + str(pattern_dict[pattern]))

    def get_pos_pattern_distribution(self, tagged_text, n):
        pattern_dict = {}
        grams = self.find_ngrams(tagged_text, n)

        for item in grams:

            next_item = 0

            pattern = ""
            for i in range(n):
                current_tag = item[i][1]

                if current_tag.isalpha():
                    pattern += current_tag + " "
                else:
                    next_item = 1
                    break

            if next_item:
                continue

            pattern = pattern.strip()
            if pattern in pattern_dict:
                pattern_dict[pattern] += 1
            else:
                pattern_dict[pattern] = 1

        return pattern_dict

    @staticmethod
    def find_ngrams(input_list, n):
        return zip(*[input_list[i:] for i in range(n)])

    @staticmethod
    def remove_punctuation(sentence):
        translator = str.maketrans('', '', string.punctuation)
        return sentence.translate(translator)

    @staticmethod
    def text_to_sentences(text):
        return re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)


if __name__ == '__main__':
    KeywordExtractor().run()

