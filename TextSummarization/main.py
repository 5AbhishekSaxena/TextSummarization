import csv
import time
from TextSummarization.ProcessSentences import ProcessSentences
from TextSummarization.ProcessStopwords import processStopwords
from TextSummarization.Utils import getDictionaryAsString
from TextSummarization.Utils import convertListToString
from TextSummarization.Utils import helper
from TextSummarization.Constants import Type
from TextSummarization.BaseNewsArticle import BaseNewsArticle
from textblob import TextBlob
from TextSummarization.nltk_implementation import word_tokenize
from TextSummarization.nltk_implementation import sentence_tokenizer

with open('dataset/test_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    article_count = 0
    correct = 0
    incorrect = 0
    correctS = 0
    incorrectS = 0
    for row in csv_reader:
        if article_count == 0:
            print(f'Column names are {", ".join(row)}')
            article_count += 1
        elif len(row[1].strip()) > 5 and "VIDEO" not in row[2] and TextBlob(row[2][:10]).detect_language() == 'hi':

            heading, given_summary, article = row[0], row[1], row[2]
            try:
                if "।" in article:
                    article = article.replace("।", ".")  # FIXME for summarization
                temp = helper(article)
                # print(f'Summary using library:\n{generated_summary}\n')
            except ValueError as e:
                continue
                # print(f'Error raised: {e}')
            else:

                baseNewsArticle = BaseNewsArticle(heading=heading, article=article,
                                                  summary=given_summary)
                # print(
                #     f'Article #{article_count}\nHeading:\n{heading}  \n\nSummary:\n{given_summary} '
                #     f'\n\nArticle:\n{article}\n')
                e1 = time.process_time()
                processSentences = ProcessSentences(baseNewsArticle)
                lengthOfHeading = len(heading.strip().split(" "))
                numberOfWordsInArticle = baseNewsArticle.getTotalNumberOfWords()
                # e2 = time.process_time() - e1
                print(f'Time-total number of words: {time.process_time() - e1}')
                e1 = time.process_time()
                numberOfImpWords = len(processStopwords(baseNewsArticle))
                print(f'Time-total number of imp words: {time.process_time() - e1}')
                e1 = time.process_time()

                processSentences.generate_summary()
                generated_summary = convertListToString(temp)
                numberOfSentences = len(processSentences.getTokenizedSentences())
                print(f'Time-total number of sentences: {time.process_time() - e1}')
                e1 = time.process_time()
                termFrequency = getDictionaryAsString(processSentences.calculateTermFrequency(),
                                                      Type.TERM_FREQUENCY)
                print(f'Time-term frequency: {time.process_time() - e1}')
                e1 = time.process_time()
                inverseDocumentFrequency = getDictionaryAsString(processSentences.calculateInverseDocumentFrequency(),
                                                                 Type.INVERSE_DOCUMENT_FREQUENCY)
                print(f'Time-idf: {time.process_time() - e1}')
                e1 = time.process_time()

                termUniqueness = getDictionaryAsString(processSentences.calculateTermUniqueness(),
                                                       Type.TERM_UNIQUENESS)
                print(f'Time-term uniqueness: {time.process_time() - e1}')
                e1 = time.process_time()
                numberOfStopWordsRemoved = numberOfWordsInArticle - numberOfImpWords
                lengthOfGivenSummary = len(given_summary.strip().split(" "))

                e2 = time.process_time()
                print(f'Time: {e2 - e1}')
                # numberOfWordsUsingCLTKLib = len(word_tokenize(baseNewsArticle.getArticle()))
                # numberOfSentencesUsingCLTKLib = len(sentence_tokenizer(baseNewsArticle.getArticle()))

                # print(f' Total number of wortds in article: {numberOfWordsInArticle}'
                #       f'\nNumber of imp words: {numberOfImpWords}')
                # try:
                #     sentimentBlob = TextBlob(str(TextBlob(convertListToString(generated_summary)).translate())).sentiment
                # except NotTranslated:
                #     sentimentBlob = 0.0
                # if sentimentBlob is TextBlob:
                #     print(f'\n\nSentimentBlob: {sentimentBlob}\n\n')

                # if numberOfSentences < 10:
                    # print(f'Sentences: {baseNewsArticle.getArticle()}')
                print(f'\nMetaData.... '
                      f'\nHeading: {lengthOfHeading} '
                      f'\nArticle:{numberOfWordsInArticle}'
                      f'\nTotal Number of sentences: {numberOfSentences}'
                      # f'\nTerm Frequency: {termFrequency}'
                      # f'\nInverse Document Frequency: '
                      # f'{inverseDocumentFrequency}'
                      # f'\nTerm Uniqueness: '
                      # f'{termUniqueness}'
                      f'\nNumber of Stop words removed: '
                      f'{numberOfStopWordsRemoved}'
                      f'\nGiven Summary:{lengthOfGivenSummary}'
                    )

                print("=====" * 50 + '\n')

                article_count += 1

            if article_count == 6:
                break

print(f'Processed {article_count} articles.')