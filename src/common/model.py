class BaseModel:

    def __repr__(self):
        return str(self.__dict__)


class Keyword(BaseModel):

    def __init__(self, text):
        self.text = text
        self.sentence_index = None
        self.sentence_start_pos = None
        self.sentence_end_pos = None
        self.tokens = text.split(" ")
        self.length = len(self.tokens)

    def __eq__(self, other):
        return self.text == other.text


class CandidateText(BaseModel):

    def __init__(self, text, analysed_html):
        self.text = text
        self.analysed_html = analysed_html
        self.type = None


class AnchorText(BaseModel):

    def __init__(self, direction, parent_object):
        self.text = parent_object.text
        self.analysed_html = parent_object.analysed_html
        self.type = parent_object.type
        self.direction = direction


class ShortText(BaseModel):

    def __init__(self, concept_type, parent_object):
        self.text = parent_object.text
        self.analysed_html = parent_object.analysed_html
        self.type = parent_object.type
        self.concept_type = concept_type


class LongText(BaseModel):

    def __init__(self, primary_noun, verb, parent_object, sentence, secondary_noun=None):
        self.text = parent_object.text
        self.analysed_html = parent_object.analysed_html
        self.type = parent_object.type
        self.primary_noun = primary_noun
        self.secondary_noun = secondary_noun
        self.verb = verb
        self.sentence = sentence


class KnowledgeUnit(BaseModel):

    def __init__(self, search_type, p_search, s_search=None, t_search=None, parsed_data=None, original_content=None):
        self.search_type = search_type
        self.p_search = p_search
        self.s_search = s_search
        self.t_search = t_search
        self.parsed_data = parsed_data
        self.original_content = original_content
