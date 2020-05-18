from TextSummarization.HindiTokenizer import Tokenizer

negative_words_file = open("dataset/negative_words_hi.txt", "r")
positive_word_file = open("dataset/positive_words_hi.txt", "r")
negative_words = set()
positive_words = set()

for x in negative_words_file:
    negative_words.add(x.strip())

for x in positive_word_file:
    positive_words.add(x.strip())


def determineSentiment():
    pos_count = []
    neg_count = []

    summary = open("/Users/rajeshwari/Documents/TextSummarization/TextSummarization/dataset/manual-dataset/csv-files/wordlist.txt", "r")
    summary_sentences_list = [line.split(".") for line in summary]

    print(len(summary_sentences_list))

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

    print(pos_count)
    print(neg_count)




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

    print (sentiment)

    return sentiment


determineSentiment()