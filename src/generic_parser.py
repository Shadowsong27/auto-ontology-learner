import logging

import natty
import usaddress
from src.common.model import CandidateText, AnchorText, ShortText, LongText
from src.common.utils import build_clean_soup, tag, remove_punctuation
from src.common.handler import ParserHandler
from src.language_extractor import SimpleRelationsExtractor


class BaseParser:

    def __init__(self, target_text):
        self.target_text = target_text

    def parse(self):
        """
        The result of parsing should contain
        1. primary search
        2. secondary search
        3. tertiary search
        4. search type
        5. hashed parse
        :return:
        """
        pass

    def has_probability(self):
        pass


class BaseGenericParser:

    def __init__(self):
        self.handler = ParserHandler()
        self.re = SimpleRelationsExtractor()
        self.domain = None

    def execute(self, domain_id):
        self.domain = self.handler.get_domain(domain_id)
        logging.info("Start parsing of domain {}".format(self.domain))
        bodies = self.handler.get_domain_bodies_by_id(domain_id)

        for body in bodies:
            page_source, hashed_url = body

            # parsing
            candidates = self._parse_candidate_text(page_source)
            self._parse_candidate_type(candidates)

            anchor_text_candidates = self._parse_anchor_text(candidates)
            short_text_candidates = self._parse_short_text(candidates)
            long_text_candidates = self._parse_long_text(candidates)

            # storage
            for anchor in anchor_text_candidates:
                self.handler.insert_anchor(anchor)

            for short in short_text_candidates:
                self.handler.insert_short(short)

            for long in long_text_candidates:
                self.handler.insert_long(long)

        self.handler.commit()

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
                    result.append(ShortText(
                        concept_type='copyright',
                        parent_object=candidate
                    ))

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
                relations = self.re.generate_relations(candidate.text)

                for relation in relations:
                    primary, secondary, verb, sentence = relation
                    long_text = LongText(
                        primary_noun=primary,
                        secondary_noun=secondary,
                        verb=verb,
                        parent_object=candidate,
                        sentence=sentence
                    )

                    result.append(long_text)

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
        try:
            if counter / len(test_string) > 0.7:
                return True
            else:
                return False
        except ZeroDivisionError:
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

        if diversity_of_tags >= 5:  # more likely to be a sentence if the diversity of tags are high
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
    logging.basicConfig(level=logging.INFO)
    BaseGenericParser().execute(1)
