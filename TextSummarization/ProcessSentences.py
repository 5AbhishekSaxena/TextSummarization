import re
from collections import Counter
from TextSummarization.ProcessStopwords import processStopwords
from TextSummarization.BaseNewsArticle import BaseNewsArticle
from textblob import TextBlob
from TextSummarization.Utils import countNumberOfWords
from TextSummarization.Utils import similar


class ProcessSentences:
    sentences = []

    def __init__(self, newsArticle: BaseNewsArticle):
        self.newsArticle = newsArticle
        self.sentences = self.getTokenizedSentences()

    def getTokenizedSentences(self):
        if self.newsArticle.article == "":
            return

        textBlob = self.newsArticle.getTextBlob()

        sentences = list()
        for sentence in textBlob.sentences:
            sentences.append(str(sentence))

        return sentences

    # 1 Term Frequency
    def calculateTermFrequency(self):
        if self.newsArticle.getArticle() == "":
            print("No Article from calculateTermFrequency")
            return

        termCounterDictionary = dict()
        termFrequencyDictionary = dict()
        if len(self.sentences) < 1:
            self.sentences = self.getTokenizedSentences()

        docWordList = processStopwords(self.newsArticle)
        for word in docWordList:
            for sentence in self.sentences:
                if word in sentence:
                    if word in termCounterDictionary:
                        termCounterDictionary[word] = termCounterDictionary[word] + 1
                    else:
                        termCounterDictionary[word] = 1

                    termFrequencyDictionary[word] = \
                        termCounterDictionary[word] / len(self.newsArticle.getArticle())

        return termFrequencyDictionary

    # 2 Number Feature
    def hasNumbers(self):
        """
        :return: dictionary of sentences, key: sentence and value: 0 or 1
        """
        numberDictionary = dict()
        if len(self.sentences) < 1:
            self.sentences = self.getTokenizedSentences()

        for sentence in self.sentences:
            if bool(re.search(r'\d', sentence)):
                numberDictionary[sentence] = 1
            else:
                numberDictionary[sentence] = 0
        # return bool(re.search(r'\d',))
        return numberDictionary

    # 3 Sentence length feature
    def sentenceLengthFeature(self):
        if len(self.sentences) < 1:
            self.sentences = self.getTokenizedSentences()

        sentenceLengthDictionary = dict()

        for sentence in self.sentences:
            number_of_words = countNumberOfWords(sentence)
            if number_of_words < 7:
                sentenceLengthDictionary[sentence] = 0.0
            else:
                sentenceLengthDictionary[sentence] = number_of_words / 10

        return sentenceLengthDictionary

    # 4 Proper Noun Feature
    def nounFeatureScoring(self):

        if len(self.sentences) < 1:
            self.sentences = self.getTokenizedSentences()

        sentenceNounScore = {}
        sentenceNounScore1 = {}
        for sentence in self.sentences:
            textBlobHindiSentence = TextBlob(sentence)
            textBlobEnglishSentence = textBlobHindiSentence.translate()
            sentenceNounScore[sentence] = 0
            sentenceNounScore1[sentence] = 0

            for words, tag in tuple(textBlobHindiSentence.tags):
                # print(words, tag, end=", ", sep=": ")

                if "NNP" == tag:
                    sentenceNounScore[sentence] = int(sentenceNounScore[sentence]) + 1

            print("\n\nEnglish Pos-tagging data  print======")
            for words, tag in tuple(textBlobEnglishSentence.tags):
                # print(words, tag, end=", ", sep=": ")

                if "NNP" == tag:
                    sentenceNounScore1[sentence] = int(sentenceNounScore1[sentence]) + 1

            print(sentenceNounScore)
            print(textBlobEnglishSentence)

        return sentenceNounScore1

    # 5 Unique Term Frequency
    def calculateTermUniqueness(self):

        wordCounter = Counter(self.newsArticle.getTextBlob().words)
        return wordCounter

    # 6 Relevance to title
    def relevanceToTitle(self):
        relevanceToTitleDictionary = dict()
        if len(self.sentences) < 1:
            self.sentences = self.getTokenizedSentences()

        for sentence in self.sentences:
            relevanceToTitleDictionary[sentence] = similar(self.newsArticle.getHeading(), sentence)
        return relevanceToTitleDictionary

    """IDF refers to inverse document frequency and can be calculated as follows:

    IDF: 
    (Total number of sentences (documents)) / (Number of sentences (documents) containing the word)
    """

    def calculateInverseDocumentFrequency(self):
        wordInSentenceDictionary = {}
        inverseDocumentFrequencyDictionary = {}
        wordList = processStopwords(self.newsArticle)

        if len(self.sentences) < 1:
            self.sentences = self.getTokenizedSentences()
        for word in wordList:
            for sentence in self.sentences:
                try:
                    if word in sentence:
                        if word in wordInSentenceDictionary:
                            wordInSentenceDictionary[word] += 1
                        else:
                            wordInSentenceDictionary[word] = 1

                    inverseDocumentFrequencyDictionary[word] = \
                        len(self.sentences) / wordInSentenceDictionary[word]

                except KeyError:
                    if word in wordInSentenceDictionary:
                        wordInSentenceDictionary.pop(word)
                    if word in inverseDocumentFrequencyDictionary:
                        inverseDocumentFrequencyDictionary.pop(word)

        return inverseDocumentFrequencyDictionary

    def getAggregateIDF(self, idfDictionary):
        wordList = processStopwords(self.newsArticle)
        inverseDocumentFrequencyDictionary = dict(idfDictionary)
        sumIDFDictionary = {}

        for word in wordList:
            for sentence in self.sentences:

                if sentence not in sumIDFDictionary:
                    sumIDFDictionary[sentence] = 0

                if word in sentence:
                    if word in inverseDocumentFrequencyDictionary:
                        sumIDFDictionary[sentence] = sumIDFDictionary[sentence] + inverseDocumentFrequencyDictionary[
                            word]

        return sumIDFDictionary

    def getAggregateTF(self, tfDictionary):
        wordList = processStopwords(self.newsArticle)
        termFrequencyDictionary = dict(tfDictionary)
        sumTFDictionary = {}

        for word in wordList:
            for sentence in self.sentences:

                if sentence not in sumTFDictionary:
                    sumTFDictionary[sentence] = 0

                if word in sentence:
                    if word in termFrequencyDictionary.keys():
                        sumTFDictionary[sentence] = sumTFDictionary[sentence] + termFrequencyDictionary[word]

        return sumTFDictionary
