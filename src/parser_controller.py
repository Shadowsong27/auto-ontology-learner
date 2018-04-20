from config import basic_short_parsers, basic_long_parsers
from src.common.handler import ParserHandler
from src.parsers.short_parsers import *
from src.parsers.long_parser import *


class ParserController:

    def __init__(self):
        self.handler = ParserHandler()
        self.context = {}

    def execute(self, domain_id):
        self.context['domain'] = self.handler.get_domain(domain_id)
        logging.info("Start parsing of domain {}".format(self.context['domain']))
        bodies = self.handler.get_domain_bodies_by_id(domain_id)

        for body in bodies:
            page_source, hashed_url = body

            # parsing
            candidates = self._parse_candidate_text(page_source)
            candidates = self._parse_candidate_type(candidates)

            for candidate in candidates:
                if candidate.type == 'short':
                    for parser_name in basic_short_parsers:
                        result = self._string_to_class(parser_name)(candidate, self.context).execute()
                        if result is not None:
                            self.handler.insert_knowledge(result)
                else:
                    for parser_name in basic_long_parsers:
                        result = self._string_to_class(parser_name)(candidate, self.context).execute()
                        for item in result:
                            self.handler.insert_knowledge(item)

            self.handler.commit()

        logging.info("Parsing of domain {} complete".format(domain_id))

    def _parse_candidate_text(self, page_source):
        """
        parse page source into candidates that contain only text and source html

        """
        soup = build_clean_soup(page_source)

        candidates = []

        for child in soup.find('body').findChildren():
            if self._is_atomic(child):
                text = child.text.strip()

                if "\n" in text:
                    text = " ".join(list(map(lambda x: x.strip(), text.split("\n"))))

                if text != '':
                    candidates.append(CandidateText(text=text, analysed_html=child))

        return candidates

    def _parse_candidate_type(self, candidates):
        """
        parse (classify) the type of candidates based on existing available data
        such as source HTML and text
        """
        for candidate in candidates:

            if self._is_short(candidate):
                candidate.type = 'short'
            else:
                candidate.type = 'long'

        return candidates

    @staticmethod
    def _is_short(candidate):
        tags = tag(candidate.text)
        list_of_tags = set(map(lambda x: x[1], tags))

        diversity_of_tags = len(list_of_tags)

        if diversity_of_tags >= 7:  # more likely to be a sentence if the diversity of tags are high
            return False
        else:
            return True

    @staticmethod
    def _is_atomic(soup_object):
        for child in soup_object.findChildren():
            if child.text != '':
                return False

        return True

    @staticmethod
    def _string_to_class(parser):
        return eval(parser)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    ParserController().execute(1)
