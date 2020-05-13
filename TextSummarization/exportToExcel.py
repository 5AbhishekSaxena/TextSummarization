import csv

import xlrd
import xlwt
from xlwt import Workbook
from xlwt.compat import xrange

from TextSummarization.Constants import DictionaryType


class ExportToExcel:
    def __init__(self, article_count, featureDictionary):

        self.article_count = article_count
        self.featureDictionary = featureDictionary
        self.wb = Workbook()
        # Set 1st Row
        self.sheet = self.wb.add_sheet('Sheet 1')
        # self.sheet.write(0, 0, 'Sentences')
        # self.sheet.write(0, 1, 'Noun Feature')
        # self.sheet.write(0, 2, 'Sentence Length Feature')
        # self.sheet.write(0, 3, 'Number Feature')
        # self.sheet.write(0, 4, 'Relevance to title Feature')
        # self.sheet.write(0, 5, 'Sentence Usefulness')

    def saveData(self):
        nounFeatureScoring = dict(self.featureDictionary[DictionaryType.NOUN_FEATURE])
        sentenceLengthFeature = dict(self.featureDictionary[DictionaryType.SENTENCE_LENGTH_FEATURE])
        hasNumberFeature = dict(self.featureDictionary[DictionaryType.HAS_NUMBER_FEATURE])
        relevanceToTitleFeature =\
            dict(self.featureDictionary[DictionaryType.RELEVANCE_TO_TITLE_FEATURE])
        aggregateIDFDictionary = dict(self.featureDictionary[DictionaryType.AGGREGATE_IDF])
        aggregateTFDictionary = dict(self.featureDictionary[DictionaryType.AGGREGATE_TF])

        row_count = 0
        nounColumn = 1
        sentenceLength_column = 2
        hasNumberColumn = 3
        relevanceToTitleColumn = 4
        aggregateIDFColumn = 5
        aggregateTFColumn = 6

        for i in nounFeatureScoring.keys():
            self.sheet.write(row_count, 0, row_count)
            self.sheet.write(row_count, nounColumn, nounFeatureScoring[i])
            self.sheet.write(row_count, sentenceLength_column, sentenceLengthFeature[i])
            self.sheet.write(row_count, hasNumberColumn, hasNumberFeature[i])
            self.sheet.write(row_count, relevanceToTitleColumn, relevanceToTitleFeature[i])
            self.sheet.write(row_count, aggregateIDFColumn, aggregateIDFDictionary[i])
            self.sheet.write(row_count, aggregateTFColumn, aggregateTFDictionary[i])
            row_count = row_count + 1

        self.wb.save(f'dataset/manual-dataset/article - {self.article_count}.xlsx')

    def csvFromExcel(self):
        wb = xlrd.open_workbook(f'dataset/manual-dataset/article - {self.article_count}.xlsx')
        sh = wb.sheet_by_index(0)
        csv_file = open(f'dataset/manual-dataset/csv-files/csv file - {self.article_count}.csv', 'w')
        wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

        for rownum in xrange(sh.nrows):
            wr.writerow(sh.row_values(rownum))

        csv_file.close()
