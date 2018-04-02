import logging
from model import Keyword
from common import *
from handler import PosPatternHandler


class SimpleKeywordsExtractor:

    def __init__(self):
        self.handler = PosPatternHandler()

    def _generate_base_candidates(self, target_text):
        candidate_patterns = self.handler.get_patterns_above_ratio(0.03)
        candidate_patterns = list(map(lambda x: x[0], candidate_patterns))

        result_list = []
        tagged_text = tag(target_text)

        for i in range(1, 5):
            temp = []
            grams = find_ngrams(tagged_text, i)

            for gram in grams:
                phrase = " ".join(list(map(lambda x: x[0], gram)))
                pos = " ".join(list(map(lambda x: x[1], gram)))

                if pos in candidate_patterns:
                    temp.append(phrase)

            result_list.append(temp)

        return result_list

    @staticmethod
    def _upward_grouping(pre_list, tar_list):
        result = set()
        for pre in pre_list:
            for tar in tar_list:
                if pre in tar:
                    result.add(pre)

        return list(set(pre_list) - result)

    def generate_final_keywords(self, target_text):
        final = []
        result = self._generate_base_candidates(target_text)

        for item in zip(result, result[1:]):
            final += self._upward_grouping(*item)

        sentences = text_to_sentences(target_text)

        final = [Keyword(text=item) for item in final]

        # mark sentences index
        for i in range(len(sentences)):
            sentence = sentences[i]
            for keyword in final:
                if keyword.text in sentence:
                    keyword.sentence_start_pos = sentence.index(keyword.tokens[0])
                    keyword.sentence_end_pos = keyword.sentence_start_pos + len(keyword.text)
                    keyword.sentence_index = i

        return final


class SimpleRelationsExtractor:
    pass


class SimpleConceptsExtractor:
    pass


class SimpleWebTextClassifier:

    pass
