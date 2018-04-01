import logging

from common import *

from handler import PosPatternHandler


class SimpleKeywordsExtractor:

    def __init__(self):
        self.handler = PosPatternHandler()

    def generate_base_candidates(self, target_text):
        candidate_patterns = self.handler.get_patterns_above_ratio(0.05)
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
    def upward_grouping(pre_list, tar_list):
        result = set()
        for pre in pre_list:
            for tar in tar_list:
                if pre in tar:
                    result.add(pre)

        return list(set(pre_list) - result)

    def generate_final_keywords(self, target_text):
        final = []
        result = self.generate_base_candidates(target_text)

        for item in zip(result, result[1:]):
            final += self.upward_grouping(*item)

        return final


class SimpleRelationsExtractor:
    pass


class SimpleConceptsExtractor:
    pass


class SimpleWebTextClassifier:

    pass
