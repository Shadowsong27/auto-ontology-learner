from handler import ParserHandler
from model import CandidateText, AnchorText, ShortText
from common import build_clean_soup, tag, remove_punctuation, text_to_sentences
from src.language_extractor import SimpleKeywordsExtractor, SimpleRelationsExtractor

import re
import nltk
import logging
import natty
import usaddress


class SimpleGenericParser:

    def __init__(self):
        self.handler = ParserHandler()
        self.ke = SimpleKeywordsExtractor()
        self.re = SimpleRelationsExtractor()
        self.domain = None

    def execute(self, domain_id):
        self.domain = self.handler.get_domain(domain_id)
        logging.info("Start parsing of domain {}".format(self.domain))
        bodies = self.handler.get_domain_bodies_by_id(domain_id)

        for body in bodies[1:]:
            page_source = body[0]

            # parsing
            candidates = self._parse_candidate_text(page_source)
            self._parse_candidate_type(candidates)
            anchor_text_candidates = self._parse_anchor_text(candidates)
            short_text_candidates = self._parse_short_text(candidates)
            long_text_candidates = self._parse_long_text(candidates)

            # storage
            # 3. class-level information parsing and storage
            # store each list into different tables

            break

        logging.info("Parsing of domain {} complete".format(domain_id))

    def _parse_candidate_text(self, page_source):
        """
        parse page source into candidates that contain only text and source html

        """
        soup = build_clean_soup(page_source)

        candidates = []

        for child in soup.find('body').findChildren():
            if self.is_atomic(child):
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

            if self.is_anchor_text(candidate):
                candidate.type = 'anchor'
            elif self.is_short_text(candidate):
                candidate.type = 'short'
            else:
                candidate.type = 'long'

        return candidates

    def _parse_anchor_text(self, candidates):
        result = []
        for candidate in candidates:
            if candidate.type == 'anchor':
                direction = self.complete_link(candidate.analysed_html['href'])
                result.append(AnchorText(direction=direction, parent_object=candidate))

        return result

    def _parse_short_text(self, candidates):
        """
        Rule-based method for identifying short objects

        """
        result = []
        for candidate in candidates:

            if candidate.type == 'short':

                input_text = remove_punctuation(candidate.text)

                # copyright
                if self.is_copyright(input_text):
                    result.append(ShortText(concept_type='copyright', parent_object=candidate))
                    continue

                # check phone and fax
                elif self.is_numeric_text(input_text):
                    if self.is_phone(input_text):
                        result.append(ShortText(
                            concept_type='phone',
                            parent_object=candidate
                        ))
                    elif self.is_fax(input_text):
                        result.append(ShortText(
                            concept_type='fax',
                            parent_object=candidate
                        ))

                elif self.is_time(input_text):
                    result.append(ShortText(
                        concept_type='time',
                        parent_object=candidate
                    ))

                elif self.is_address(input_text):
                    result.append(ShortText(
                        concept_type='phone',
                        parent_object=candidate
                    ))

                elif candidate.analysed_html.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    result.append(ShortText(
                        concept_type='header',
                        parent_object=candidate
                    ))
                else:
                    result.append(ShortText(
                        concept_type='unknown',
                        parent_object=candidate
                    ))

        return result

    def _parse_long_text(self, candidates):
        """This section will contain the exact parsing logic for relation, a relation is counted as an attribute
        similar to the href value in anchor text


        1. text
        2. analysed_html
        3. type
        4. object 1 (applicable for search)
        5. object 2 (applicable for search)
        6. relation (applicable for search)

        """
        result = []

        for candidate in candidates:
            if candidate.type == 'long':
                keywords = self.ke.generate_final_keywords(candidate.text)
                relations = self.re.generate_relations(candidate.text, keywords)
                break

        return result

    @staticmethod
    def is_time(text):
        dp = natty.DateParser(text)
        if dp.result() is not None:
            return True
        return False

    @staticmethod
    def is_address(text):
        results = usaddress.parse(text)
        diversity = set(map(lambda x: x[1], results))
        if len(diversity) > 2:
            return True
        else:
            return False

    @staticmethod
    def is_copyright(text):
        if "copyright" in text.lower():
            return True
        else:
            return False

    @staticmethod
    def is_phone(text):
        if "p" in text.lower():
            return True
        else:
            return False

    @staticmethod
    def is_fax(text):
        if "f" in text.lower():
            return True
        else:
            return False

    @staticmethod
    def is_numeric_text(text):
        counter = 0
        test_string = remove_punctuation(text)
        for char in test_string:
            if char.isdigit():
                counter += 1

        if counter / len(test_string) > 0.6:
            return True
        else:
            return False

    def complete_link(self, link):
        if link[:4] != "http":
            return self.domain + link
        else:
            return link

    @staticmethod
    def is_anchor_text(candidate):
        return candidate.analysed_html.has_attr('href')  # or candidate.analysed_html.has_attr('src')

    @staticmethod
    def is_short_text(candidate):
        tags = tag(candidate.text)
        list_of_tags = set(map(lambda x: x[1], tags))

        diversity_of_tags = len(list_of_tags)

        if diversity_of_tags >= 10:  # more likely to be a sentence if the diversity of tags are high
            return False
        else:
            return True

    @staticmethod
    def is_atomic(soup_object):
        for child in soup_object.findChildren():
            if child.text != '':
                return False

        return True


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    SimpleGenericParser().execute(1)
