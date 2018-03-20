import logging

from src.common import *

from database_handler import PosPatternHandler


class SimpleKeywordsExtractor:

    def __init__(self):
        self.handler = PosPatternHandler()

    def generate_keywords(self, target_text):
        candidate_patterns = self.handler.get_patterns_above_ratio(0.01)
        candidate_patterns = list(map(lambda x: x[0], candidate_patterns))

        result_list = []
        tagged_text = tag(target_text)

        for i in range(1, 5):
            logging.info("searching for {} gram".format(i))
            grams = find_ngrams(tagged_text, i)

            for gram in grams:
                phrase = " ".join(list(map(lambda x: x[0], gram)))
                pos = " ".join(list(map(lambda x: x[1], gram)))

                if pos in candidate_patterns:
                    result_list.append(phrase)

        return [item for item in result_list]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(SimpleKeywordsExtractor().generate_keywords("Established in 2009, 4FINGERS was founded after its creators tried Korean-style fried chicken in New York City's Koreatown. Steen Puggaard joined the brand as CEO in 2014, and the brand expanded from one outlet in Singapore to 21 outlets in Asia-Pacific within 4 years.[3][4] 4FINGERS is located in malls such as Plaza Singapura, Orchard Gateway and Changi Airport. In 2015, they opened their first overseas store in Kuala Lumpur, Malaysia located in Mid Valley Megamall and NU Sentral in December 2016. In June 2017, 4FINGERS announced its expansion to Australia, with their first store located on Bourke Street."))
