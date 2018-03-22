from handler import ParserHandler
from bs4 import BeautifulSoup

import logging


class SimpleGenericParser:

    def __init__(self):
        self.handler = ParserHandler()

    def parse(self, domain_id):
        logging.info("Start parsing of domain {}".format(domain_id))
        bodies = self.handler.get_domain_bodies_by_id(domain_id)

        for body in bodies:
            self.parse_each(body)

            break

        logging.info("Parsing of domain {} complete".format(domain_id))

    def parse_each(self, body):
        soup = BeautifulSoup(body[0], 'lxml')

        # simple cleaning
        for script in soup("script"):
            script.decompose()

        # classification
        for child in soup.find('body').findChildren():
            if self.is_atomic(child):
                print("===a===")
                text = child.text.strip()

                if "\n" in text:
                    texts = list(map(lambda x: x.strip(), text.split("\n")))
                else:
                    texts = [text]

                if texts != ['']:
                    print(texts)
                    print(child)

        # parsing of each class

    def is_atomic(self, soup_object):
        for child in soup_object.findChildren():
            if child.text != '':
                return False

        return True

    def parse_anchor_text(self):
        pass

    def parse_short_text(self):
        pass

    def parse_long_text(self):
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    SimpleGenericParser().parse(1)
