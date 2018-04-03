import logging
from model import Keyword
from common import *
from handler import PosPatternHandler

NOUN_PHRASE_THRESHOLD = 0.03
VERB_PHRASE_THRESHOLD = 0.01


class SimpleKeywordsExtractor:

    def __init__(self, phrase_type):
        self.handler = PosPatternHandler()

        if phrase_type == 'noun':
            self.candidate_pattern = list(map(lambda x: x[0],
                                              self.handler.get_patterns_above_ratio_for_noun(NOUN_PHRASE_THRESHOLD)))
        else:
            self.candidate_pattern = list(map(lambda x: x[0],
                                              self.handler.get_patterns_above_ratio_for_verb(VERB_PHRASE_THRESHOLD)))

    def generate_keywords(self, target_text):
        """main logic to generate final keywords list"""
        logging.debug("Start generate keywords")
        sentences = text_to_sentences(target_text)

        base_candidates = self._generate_base_candidates(target_text)

        temp_result = []
        for item in zip(base_candidates, base_candidates[1:]):
            temp_result += self._upward_grouping(*item)

        # convert str into objects
        temp_result = [Keyword(text=item) for item in temp_result]
        temp_result = self._mark_keyword_attributes(sentences, temp_result)

        # check overlapping, could be combined into one word
        return self._merge_keywords(sentences, temp_result)

    def _generate_base_candidates(self, target_text):
        """generate base candidates based on ratio threshold"""

        result_list = []
        tagged_text = tag(target_text)

        for i in range(1, 5):
            temp = []
            grams = find_ngrams(tagged_text, i)

            for gram in grams:
                phrase = " ".join(list(map(lambda x: x[0], gram)))
                pos = " ".join(list(map(lambda x: x[1], gram)))

                if pos in self.candidate_pattern:
                    temp.append(phrase)

            result_list.append(temp)

        return result_list

    @staticmethod
    def _upward_grouping(pre_list, tar_list):
        """
        given two list of candidates
        pre_list: one gram lesser than tar_list
        group potential candidates together by substring grouping
        """
        result = set()
        for pre in pre_list:
            for tar in tar_list:
                if pre in tar:
                    result.add(pre)

        return list(set(pre_list) - result)

    @staticmethod
    def _merge_keywords(sentences, temp_result):
        final = {}
        for i in range(len(sentences)):
            logging.debug("sentence {}".format(i))
            keywords_group = list(filter(lambda x: x.sentence_index == i, temp_result))
            keywords_group.sort(key=lambda x: x.sentence_start_pos)
            for item in zip(keywords_group, keywords_group[1:]):
                keyword_1, keyword_2 = item
                if keyword_1.sentence_end_pos >= keyword_2.sentence_start_pos:
                    new_text = sentences[i][keyword_1.sentence_start_pos: keyword_2.sentence_end_pos].strip()
                    new_keyword = Keyword(new_text)
                    new_keyword.sentence_start_pos = keyword_1.sentence_start_pos
                    new_keyword.sentence_end_pos = keyword_2.sentence_end_pos
                    new_keyword.sentence_index = i
                    final[new_text] = new_keyword
                else:
                    final[keyword_1.text] = keyword_1
                    final[keyword_2.text] = keyword_2

        return [value for value in final.values()]

    @staticmethod
    def _mark_keyword_attributes(sentences, temp_result):
        for i in range(len(sentences)):
            sentence = sentences[i]
            for keyword in temp_result:
                if keyword.text in sentence:
                    keyword.sentence_start_pos = sentence.index(keyword.tokens[0])
                    keyword.sentence_end_pos = keyword.sentence_start_pos + len(keyword.text)
                    keyword.sentence_index = i

        return temp_result


class SimpleRelationsExtractor:

    def __init__(self):
        self.handler = PosPatternHandler()
        self.ke_n = SimpleKeywordsExtractor('noun')
        self.ke_v = SimpleKeywordsExtractor('verb')

    def generate_relations(self, target_text):
        noun_phrases = self.ke_n.generate_keywords(target_text)
        verb_phrases = self.ke_v.generate_keywords(target_text)

        for i in range(len(text_to_sentences(target_text))):
            cur_nouns = list(filter(lambda x: x.sentence_index == i, noun_phrases))
            cur_verbs = list(filter(lambda x: x.sentence_index == i, verb_phrases))

            logging.debug(cur_nouns)
            logging.debug(cur_verbs)


class SimpleConceptsExtractor:
    pass


class SimpleWebTextClassifier:

    pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    SimpleKeywordsExtractor('noun').generate_keywords("We understand the importance of community and that also means giving back to our friends. There is a deep and important ecosystem that is created when businesses give back to their local community. Our donation program is an important part of our business and we appreciate all our friends who take the time to request gift certificates and/or funding from Marie Catrib's.")