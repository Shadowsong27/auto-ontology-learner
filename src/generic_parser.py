from handler import ParserHandler
from model import CandidateText, AnchorText
from common import build_clean_soup, tag

import nltk
import logging


class SimpleGenericParser:

    def __init__(self):
        self.handler = ParserHandler()
        self.candidate_parse = CandidateParser()
        self.domain = None

    def execute(self, domain_id):
        self.domain = self.handler.get_domain(domain_id)
        logging.info("Start parsing of domain {}".format(self.domain))
        bodies = self.handler.get_domain_bodies_by_id(domain_id)

        for body in bodies:
            page_source = body[0]

            # parsing
            candidates = self.parse_candidate_text(page_source)
            candidates = self.parse_candidate_type(candidates)
            anchor_text_candidates = self.candidate_parse.parse_anchor_text(candidates)
            short_text_candidates = self.candidate_parse.parse_short_text(candidates)
            long_text_candidates = self.candidate_parse.parse_long_text(candidates)

            # storage
            # 3. class-level information parsing and storage
            # store each list into different tables

        logging.info("Parsing of domain {} complete".format(domain_id))

    def parse_candidate_text(self, page_source):
        """
        parse page source into candidates that contain only text and source html

        """
        soup = build_clean_soup(page_source)

        candidates = []

        for child in soup.find('body').findChildren():
            if self.candidate_parse.is_atomic(child):
                text = child.text.strip()

                if "\n" in text:
                    text = " ".join(list(map(lambda x: x.strip(), text.split("\n"))))

                if text != '':
                    candidates.append(CandidateText(text=text, analysed_html=child))

        return candidates

    def parse_candidate_type(self, candidates):
        """
        parse (classify) the type of candidates based on existing available data
        such as source HTML and text

        """
        for candidate in candidates:

            if self.candidate_parse.is_anchor_text(candidate):
                candidate.type = 'anchor'
            elif self.candidate_parse.is_short_text(candidate):
                candidate.type = 'short'
            else:
                candidate.type = 'long'

        return candidates


class CandidateParser:

    def parse_anchor_text(self, candidates):
        for candidate in candidates:
            if candidate.type == 'anchor':
                direction = self.complete_link(candidate.analysed_html['href'])
                print(AnchorText(direction=direction, parent_object=candidate))

    def parse_short_text(self, candidates):
        """
        Phone
        Fax
        Time
        Address
        Copyright

        Rule-based method for identifying short objects

        attributes:

        1. text
        2. analysed_html
        3. type
        4. object_type
        5. value

        :param candidates:
        :return:
        """
        for candidate in candidates:
            if candidate.type == 'short':
                logging.info(candidate)

    def parse_long_text(self, candidates):
        """This section will contain the exact parsing logic for relation, a relation is counted as an attribute
        similar to the href value in anchor text


        1. text
        2. analysed_html
        3. type
        4. object 1 (applicable for search)
        5. object 2 (applicable for search)
        6. relation (applicable for search)

        """

        for candidate in candidates:
            if candidate.type == 'long':
                logging.info(candidate)

    def complete_link(self, link):
        if link[:4] != "http":
            return self.domain + link
        else:
            return link

    @staticmethod
    def is_anchor_text(candidate):
        return candidate.analysed_html.has_attr('href') or candidate.analysed_html.has_attr('src')

    @staticmethod
    def is_short_text(candidate):
        tags = tag(candidate.text)
        list_of_tags = set(map(lambda x: x[1], tags))

        diversity_of_tags = len(list_of_tags)

        if diversity_of_tags >= 10:  # more likely to be a sentence if the diversity of tags are high
            return True
        else:
            return False

    @staticmethod
    def is_atomic(soup_object):
        for child in soup_object.findChildren():
            if child.text != '':
                return False

        return True


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    SimpleGenericParser().execute(1)
