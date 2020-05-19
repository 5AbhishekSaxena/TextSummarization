import re
from TextSummarization import nltk_implementation as ck
from TextSummarization import BaseNewsArticle as bsa


def getListOfAllStopWords():
    return list(ck.get_hindi_stop_words())


def processStopwords(baseNewsArticle: bsa.BaseNewsArticle):
    """
    :param baseNewsArticle:
    :return list: It returns a list of unique important words from the news article.
    """
    # looking for all unique stopwords that are present in our corpus
    docWordList = set(baseNewsArticle.getTextBlob().words)
    stopWordList = getListOfAllStopWords()

    if '' in docWordList:
        docWordList.remove('')
    if " " in docWordList:
        docWordList.remove(" ")

    # removing stopwords
    for word in stopWordList:
        if word in docWordList:
            docWordList.remove(word)

    return docWordList


