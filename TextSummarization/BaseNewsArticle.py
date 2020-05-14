from textblob import TextBlob


class BaseNewsArticle:
    HEADING = 0
    ARTICLE = 1
    SUMMARY = 3

    def __init__(self, article: str, heading="", summary=""):
        self.heading = heading
        self.article = article  # .replace("[^a-zA-Z]", " ")
        self.summary = summary
        self.englishTextBlob = TextBlob(article).translate()

    def getHeading(self):
        return str(self.heading)

    def getArticle(self):
        return str(self.article)

    def getSummary(self):
        return str(self.summary)

    def getEnglishArticle(self):
        return str(self.englishTextBlob)

    def getTextBlob(self, type=ARTICLE) -> TextBlob:
        return {self.HEADING: TextBlob(self.getHeading()),
                self.ARTICLE: TextBlob(self.getArticle()),
                self.SUMMARY: TextBlob(self.getSummary())
                }[type]

    def getTotalNumberOfWords(self, type=ARTICLE):
        return len(self.getTextBlob(type).words)
