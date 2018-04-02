import logging
from model import Keyword
from common import *
from handler import PosPatternHandler
from resources.stanford_openie.open_ie_api import call_api_single


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

    def generate_relations(self, target_text, keywords):
        sentences = text_to_sentences(target_text)

        # find relations / either relation or new grouping
        for i in range(len(sentences)):
            sentence = sentences[i]
            logging.info(sentence)
            keywords_group = list(filter(lambda x: x.sentence_index == i, keywords))

            for item in zip(keywords_group, keywords_group[1:]):
                keyword_1, keyword_2 = item
                logging.info(item)
                if keyword_1.sentence_end_pos >= keyword_2.sentence_start_pos:
                    # overlapping, could be combined into one word

                    word = sentence[keyword_1.sentence_start_pos: keyword_2.sentence_end_pos].strip()

                    # open IE

                else:

                    word_between = sentence[keyword_1.sentence_end_pos: keyword_2.sentence_start_pos]
                    print(tag(word_between))
                    # open IE
        return []


class SimpleConceptsExtractor:
    pass


class SimpleWebTextClassifier:

    pass
