class BaseModel:

    def __repr__(self):
        return str(self.__dict__)


class CandidateText(BaseModel):

    def __init__(self, text, analysed_html):
        self.text = text
        self.analysed_html = analysed_html

