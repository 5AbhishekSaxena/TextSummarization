negative_words_file = open("dataset/negative_words_hi.txt", "r")
positive_word_file = open("dataset/positive_words_hi.txt", "r")
negative_words = set()
positive_words = set()

for x in negative_words_file:
    negative_words.add(x.strip())

for x in positive_word_file:
    positive_words.add(x.strip())


class SentimentAnalysis:
    summary = ""

    def __init__(self, summary):
        self.summary = summary

    def determineSentiment(self):

        total_score = 0
        for word in self.summary:
            if word in positive_words:
                total_score += 1
            elif word in negative_words:
                total_score -= 1

        sentiment = "neutral"
        if total_score > 0:
                sentiment = "positive"
        elif total_score < 0:
                sentiment = "negative"

        return sentiment