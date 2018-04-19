from src.common.utils import BaseParser
from src.common.model import *


class AnchorParser(BaseParser):

    def _parse(self):
        result = []
        direction = self.complete_link(self.candidate.analysed_html['href'])
        result.append(AnchorText(direction=direction, parent_object=self.candidate))
        return result

    def _has_probability(self):
        if self.candidate.analysed_html.has_attr('href'):
            return 1
        else:
            return 0

    def complete_link(self, link):
        if link[:4] != "http":
            return self.context['domain'] + link
        else:
            return link


