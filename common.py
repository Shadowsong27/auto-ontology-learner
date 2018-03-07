import string


class BaseTokenizer:

    @staticmethod
    def remove_punctuation(sentence):
        translator = str.maketrans('', '', string.punctuation)
        return sentence.translate(translator)
