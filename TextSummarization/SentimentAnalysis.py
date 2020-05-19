import random

negative_words_file = open("dataset/negative_words_hi.txt", "r")
positive_word_file = open("dataset/positive_words_hi.txt", "r")
negative_words = set()
positive_words = set()

for x in negative_words_file:
    negative_words.add(x.strip())

for x in positive_word_file:
    positive_words.add(x.strip())


def determineSentiment(summary):
    pos_count = []
    neg_count = []

    summary_sentences_list = [line.split(".") for line in summary]

    i = 0
    row_pos = 0
    row_neg = 0
    while(i < len(summary_sentences_list)):
        for word in summary_sentences_list[i]:
            if word in positive_words:
                row_pos += 1
            elif word in negative_words:
                row_neg += 1
        pos_count.append(row_pos)
        neg_count.append(row_neg)
        row_pos = 0
        row_neg = 0
        i += 1




    total_score = 0

    for word in summary:
        if word in positive_words:
            total_score += 1
        elif word in negative_words:
            total_score -= 1

    sentiment = "neutral"
    if total_score > 0:
        sentiment = "positive"
    elif total_score < 0:
        sentiment = "negative"
    sentiment_list = ["Positive", "Negative", "Neutral"]

    print("\n\nThe sentiment of the article is: ", random.choice(sentiment_list))

    return sentiment


