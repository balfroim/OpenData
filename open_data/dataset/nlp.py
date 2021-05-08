import spacy


class NLP:

    def __init__(self):
        self.nlp = spacy.load("fr_core_news_sm")

    @classmethod
    def instance(cls):
        try:
            return cls._instance
        except AttributeError:
            cls._instance = cls()
            return cls._instance
