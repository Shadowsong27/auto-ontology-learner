from handler import ParserHandler
from model import CandidateText, AnchorText
from common import build_clean_soup, text_to_sentences, tag
from bs4 import Tag
import os

import logging


class SimpleGenericParser:

    def __init__(self):
        self.handler = ParserHandler()
        self.domain = None

    def execute(self, domain_id):
        self.domain = self.handler.get_domain(domain_id)
        logging.info("Start parsing of domain {}".format(self.domain))
        bodies = self.handler.get_domain_bodies_by_id(domain_id)

        for body in bodies:

            page_source = body[0]
            soup = build_clean_soup(page_source)
            candidates = self.parse_each(body[0])
            # self.parse_anchor_text(candidates)
            self.parse_short_text(candidates)
            self.parse_long_text(candidates)
            # TODO:
            # 1. depth indexing and obtain indexed HTML tree (pause)
            # 2. rule-based classification
            # 3. class-level information parsing and storage

            break

        logging.info("Parsing of domain {} complete".format(domain_id))

    def parse_each(self, body):
        soup = build_clean_soup(body)
        candidates = self.extract_candidate_text(soup)
        self.classify_candidate_type(candidates)
        return candidates

    def classify_candidate_type(self, candidates):
        for candidate in candidates:

            # is anchor test?
            resp = self.is_anchor_text(candidate)

            if resp:
                candidate.type = 'anchor'
            else:
                if self.is_complete_sentence(candidate.text):
                    candidate.type = 'long'
                else:
                    candidate.type = 'short'

    @staticmethod
    def is_anchor_text(candidate):
        try:
            resp = candidate.analysed_html['href']
            return resp
        except KeyError:
            return False

    @staticmethod
    def is_complete_sentence(text):
        tags = tag(text)
        list_of_tags = set(map(lambda x: x[1], tags))

        diversity_of_tags = len(list_of_tags)

        if diversity_of_tags >= 10:
            return True
        else:
            return False

    def extract_candidate_text(self, soup):
        candidates = []

        # classification
        for child in soup.find('body').findChildren():
            if self.is_atomic(child):
                text = child.text.strip()

                if "\n" in text:
                    text = " ".join(list(map(lambda x: x.strip(), text.split("\n"))))

                if text != '':
                    candidates.append(CandidateText(text=text, analysed_html=child))

        return candidates

    @staticmethod
    def is_atomic(soup_object):
        for child in soup_object.findChildren():
            if child.text != '':
                return False

        return True

    def parse_anchor_text(self, candidates):
        for candidate in candidates:
            if candidate.type == 'anchor':
                direction = self.complete_link(candidate.analysed_html['href'])
                print(AnchorText(direction=direction, parent_object=candidate))

    def parse_short_text(self, candidates):
        for candidate in candidates:
            if candidate.type == 'short':
                print(candidate)

    def parse_long_text(self, candidates):
        for candidate in candidates:
            if candidate.type == 'long':
                print(candidate)

    def complete_link(self, link):
        if link[:4] != "http":
            return self.domain + link
        else:
            return link


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    SimpleGenericParser().execute(1)
