import natty
import usaddress

from src.common.utils import BaseParser
from src.common.model import *


class AnchorParser(BaseParser):

    def _parse(self):
        direction = self._complete_link(self.candidate.analysed_html['href'])
        return AnchorText(direction=direction, parent_object=self.candidate)

    def _has_probability(self):
        if self.candidate.analysed_html.has_attr('href'):
            return 1
        else:
            return 0

    def _complete_link(self, link):
        if link[:4] != "http":
            return self.context['domain'] + link
        else:
            return link


class TimeParser(BaseParser):

    def _parse(self):
        pass

    def _has_probability(self):
        dp = natty.DateParser(self.candidate.text)
        if dp.result() is not None:
            return 1

        return 0


class AddressParser(BaseParser):

    def _parse(self):
        pass

    def _has_probability(self):
        results = usaddress.parse(self.candidate.text)
        diversity = set(map(lambda x: x[1], results))
        if len(diversity) > 2:
            return 1
        else:
            return 0


class ContactParser(BaseParser):

    def _parse(self):
        pass

    def _has_probability(self):
        def is_phone(text):
            if "p" in text.lower():
                return True
            else:
                return False

        def is_fax(text):
            if "f" in text.lower():
                return True
            else:
                return False

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


class CopyrightParser(BaseParser):

    def _parse(self):
        pass

    def _has_probability(self):
        if "copyright" in text.lower():
            return True
        else:
            return False




