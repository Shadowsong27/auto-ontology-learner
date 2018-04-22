import natty
import usaddress

from src.common.utils import BaseShortParser, remove_punctuation
from src.common.model import *
from bs4 import BeautifulSoup


with open(r'parsers/resources/foodlist.htm', 'r', encoding='iso-8859-1') as f:
    page_source = f.read()
    soup = BeautifulSoup(page_source, 'lxml')
    tds = soup.find_all("td")

    food_list = []
    for td in tds[11:-9]:
        food_list.extend(td.text.strip().split("\n"))

    food_list = set(food_list)


class LinkParser(BaseShortParser):

    def _parse(self):
        direction = self._complete_link(self.candidate.analysed_html['href'])
        unit = KnowledgeUnit(
            domain_id=self.context['domain_id'],
            search_type='short',
            p_search='link',
            s_search=self.candidate.text,
            parsed_data=direction,
            original_content=self.candidate.text
        )
        return unit

    def _has_probability(self):
        if self.candidate.analysed_html.has_attr('href'):
            return True
        else:
            return False

    def _complete_link(self, link):
        if link[:4] != "http":
            return self.context['domain'] + link
        else:
            return link


class TimeParser(BaseShortParser):

    def _parse(self):
        dp = natty.DateParser(self.candidate.text)
        unit = KnowledgeUnit(
            domain_id=self.context['domain_id'],
            search_type='short',
            p_search='date',
            s_search=self.candidate.text,
            parsed_data=dp.result(),
            original_content=self.candidate.text
        )
        return unit

    def _has_probability(self):
        weekdays = ['monday', 'mon', 'tuesday', 'tue',
                   'wednesday', 'wed', 'thursday', 'thurs',
                   'friday', 'fri', 'saturday', 'sat',
                   'sunday', 'sun'
        ]

        time_codes = ['am', 'pm']
        tokens = remove_punctuation(self.candidate.text).lower().split(" ")

        for weekday in weekdays:
            for token in tokens:
                if weekday in token:
                    return True

        for time_code in time_codes:
            for token in tokens:
                if time_code in token:
                    return True

        return False


class AddressParser(BaseShortParser):

    def _parse(self):
        unit = KnowledgeUnit(
            domain_id=self.context['domain_id'],
            search_type='short',
            p_search='address',
            s_search=self.candidate.text,
            parsed_data=self.candidate.text,
            original_content=self.candidate.text
        )
        return unit

    def _has_probability(self):
        results = usaddress.parse(self.candidate.text)
        diversity = set(map(lambda x: x[1], results))
        if len(diversity) > 3:
            return True
        else:
            return False


class ContactParser(BaseShortParser):

    def _parse(self):
        if "p" in self.candidate.text.lower():
            return KnowledgeUnit(
                domain_id=self.context['domain_id'],
                search_type='short',
                p_search='phone',
                s_search=self.candidate.text,
                parsed_data=self.candidate.text,
                original_content=self.candidate.text
            )
        elif "f" in self.candidate.text.lower():
            return KnowledgeUnit(
                domain_id=self.context['domain_id'],
                search_type='short',
                p_search='fax',
                s_search=self.candidate.text,
                parsed_data=self.candidate.text,
                original_content=self.candidate.text
            )
        else:
            return KnowledgeUnit(
                domain_id=self.context['domain_id'],
                search_type='short',
                p_search='contact',
                s_search=self.candidate.text,
                parsed_data=self.candidate.text,
                original_content=self.candidate.text
            )

    def _has_probability(self):
        counter = 0
        test_string = remove_punctuation(self.candidate.text)
        for char in test_string:
            if char.isdigit():
                counter += 1
        try:
            if counter / len(test_string) > 0.5:
                if "(" in self.candidate.text or "-" in self.candidate.text:
                    return True
            else:
                return False
        except ZeroDivisionError:
            return False


class CopyrightParser(BaseShortParser):

    def _parse(self):
        unit = KnowledgeUnit(
            domain_id=self.context['domain_id'],
            search_type='short',
            p_search='copyright',
            s_search=self.candidate.text,
            parsed_data=self.candidate.text,
            original_content=self.candidate.text
        )
        return unit

    def _has_probability(self):
        if "copyright" in self.candidate.text.lower() or "©" in self.candidate.text.lower():
            return True
        else:
            return False


class FoodParser(BaseShortParser):

    def _parse(self):
        unit = KnowledgeUnit(
            domain_id=self.context['domain_id'],
            search_type='short',
            p_search='food',
            s_search=self.food,
            parsed_data=self.candidate.text,
            original_content=self.candidate.text
        )
        return unit

    def _has_probability(self):
        candidate_tokens = set(self.candidate.text.lower().split(" "))
        if len(food_list.intersection(candidate_tokens)) > 0:

            self.food = " ".join(food_list.intersection(candidate_tokens))

            return True

        return False



