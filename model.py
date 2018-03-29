class BaseModel:

    def __repr__(self):
        return str(self.__dict__)


class CandidateText(BaseModel):

    def __init__(self, text, analysed_html):
        self.text = text
        self.analysed_html = analysed_html
        self.type = None


class AnchorText(CandidateText):

    def __init__(self, direction, parent_object):
        super(AnchorText, self).__init__(self, direction)
        self.text = parent_object.text
        self.analysed_html = parent_object.analysed_html
        self.type = parent_object.type

        self.direction = direction


class ShortText(CandidateText):

    def __init__(self, concept_type, parent_object):
        super(ShortText, self).__init__(self, concept_type)
        self.text = parent_object.text
        self.analysed_html = parent_object.analysed_html
        self.type = parent_object.type

        self.concept_type = concept_type



