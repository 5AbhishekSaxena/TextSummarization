import csv
import time

from TextSummarization.AdaBoostModel import generate_summary
from TextSummarization.ProcessSentences import ProcessSentences
from TextSummarization.ProcessStopwords import processStopwords
from TextSummarization.SentimentAnalysis import determineSentiment
from TextSummarization.Utils import getDictionaryAsString
from TextSummarization.Utils import isEnglish
from TextSummarization.Constants import Type, DictionaryType
from TextSummarization.BaseNewsArticle import BaseNewsArticle
from textblob import TextBlob
from TextSummarization.nltk_implementation import word_tokenize
from TextSummarization.nltk_implementation import sentence_tokenizer
from TextSummarization.exportToExcel import ExportToExcel


with open('dataset/test_case_2.csv') as csv_file:
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
        elif len(row[1].strip()) > 5 and "VIDEO" not in row[2] \
                and isEnglish(str(TextBlob(row[2][:10]))) is not True:

            heading, given_summary, article = row[0], row[1], row[2]
            try:
                if "।" in article:
                    article = article.replace("।", ".")
            except ValueError as e:
                continue
                # print(f'Error raised: {e}')
            else:

                baseNewsArticle = BaseNewsArticle(heading=heading, article=article,
                                                  summary=given_summary)

                processArticle = ProcessSentences(baseNewsArticle)
                sentences_in_article = processArticle.getTokenizedSentences()
                numberOfSentences = len(sentences_in_article)

                e1 = time.process_time()
                lengthOfHeading = len(heading.strip().split(" "))
                numberOfWordsInArticle = baseNewsArticle.getTotalNumberOfWords()

                e1 = time.process_time()
                numberOfImpWords = len(processStopwords(baseNewsArticle))
                e1 = time.process_time()

                e1 = time.process_time()
                termFrequencyDictionary = processArticle.calculateTermFrequency()
                termFrequency = getDictionaryAsString(termFrequencyDictionary,
                                                      Type.TERM_FREQUENCY)
                e1 = time.process_time()
                inverseDocumentFrequencyDictionary = processArticle.calculateInverseDocumentFrequency()
                inverseDocumentFrequency = getDictionaryAsString(inverseDocumentFrequencyDictionary,
                                                                 Type.INVERSE_DOCUMENT_FREQUENCY)
                e1 = time.process_time()

                termUniqueness = getDictionaryAsString(processArticle.calculateTermUniqueness(),
                                                       Type.TERM_UNIQUENESS)
                e1 = time.process_time()
                numberOfStopWordsRemoved = numberOfWordsInArticle - numberOfImpWords
                lengthOfGivenSummary = len(given_summary.strip().split(" "))

                e2 = time.process_time()
                numberOfWordsUsingCLTKLib = len(word_tokenize(baseNewsArticle.getArticle()))
                numberOfSentencesUsingCLTKLib = len(sentence_tokenizer(baseNewsArticle.getArticle()))

                nounFeatureScoring = processArticle.nounFeatureScoring()
                sentenceLengthFeature = processArticle.sentenceLengthFeature()
                hasNumberFeature = processArticle.hasNumbers()
                relevanceToTitleFeature = processArticle.relevanceToTitle()

                aggregateIDF = processArticle.getAggregateIDF(inverseDocumentFrequencyDictionary)
                aggregateTF = processArticle.getAggregateTF(termFrequencyDictionary)

                featureDictionaries = dict()
                featureDictionaries[DictionaryType.NOUN_FEATURE] = nounFeatureScoring
                featureDictionaries[DictionaryType.SENTENCE_LENGTH_FEATURE] = sentenceLengthFeature
                featureDictionaries[DictionaryType.HAS_NUMBER_FEATURE] = hasNumberFeature
                featureDictionaries[DictionaryType.RELEVANCE_TO_TITLE_FEATURE] = relevanceToTitleFeature
                featureDictionaries[DictionaryType.AGGREGATE_IDF] = aggregateIDF
                featureDictionaries[DictionaryType.AGGREGATE_TF] = aggregateTF

                exportToExcel = ExportToExcel(article_count, featureDictionaries)
                exportToExcel.saveData()

                useful_sentences = generate_summary("/Users/rajeshwari/Documents/TextSummarization/TextSummarization/dataset/manual-dataset/article - 1.xlsx")

                if numberOfSentences < 10:
                    print(f'Sentences: {baseNewsArticle.getArticle()}')

                summary = ""

                x = 0

                while (x < len(useful_sentences) - 1):
                    if useful_sentences[x] == 1.0:
                        summary = summary + sentences_in_article[x]
                    x += 1

                print(
                    f'Article #{article_count}\nHeading:\n{heading}'
                    f'\n\nArticle:\n{article}\n')
                print("\nGenerated summary is given as follows: \n\n", summary)

                determineSentiment(summary)

                print(f'\n\nMetaData.... '
                      f'\nHeading: {lengthOfHeading} '
                      f'\nArticle:{numberOfWordsInArticle}'
                      f'\nTotal Number of sentences: {numberOfSentences}'
                      f'\nTerm Frequency: {termFrequency}'
                      f'\nInverse Document Frequency: '
                      f'{inverseDocumentFrequency}'
                      f'\nTerm Uniqueness: '
                      f'{termUniqueness}'
                      f'\nNumber of Stop words removed: '
                      f'{numberOfStopWordsRemoved}'
                      f'\nNoun Feature: '
                      f'{nounFeatureScoring}'
                      f'\nSentence Length Feature: '
                      f'{sentenceLengthFeature}'
                      f'\nHas Number Feature Feature: '
                      f'{hasNumberFeature}'
                      f'\nRelevance to Title Feature: '
                      f'{relevanceToTitleFeature}'
                      f'\nGiven Summary:{lengthOfGivenSummary}'
                      )
