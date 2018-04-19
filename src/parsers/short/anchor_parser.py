from src.parser_controller import BaseParser


class AnchorParser(BaseParser):

    def parse(self):
        result = []
        for candidate in candidates:
            if candidate.type == 'anchor':
                direction = self.complete_link(candidate.analysed_html['href'])
                result.append(AnchorText(direction=direction, parent_object=candidate))

        return result

    def has_probability(self):
        if self.target_text.has_attr('href'):
            return 1
        else:
            return 0
