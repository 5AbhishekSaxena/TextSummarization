import xlwt
from xlwt import Workbook
from TextSummarization.Constants import DictionaryType


class ExportToExcel:
    def __init__(self, article_count, featureDictionary):
        wb = Workbook()
        # Set 1st Row
        self.sheet = wb.add_sheet('Sheet 1')
        self.sheet.write(0, 0, 'Sentences')
        self.sheet.write(0, 1, 'Noun Feature')
        self.sheet.write(0, 2, 'Sentence Length Feature')
        self.sheet.write(0, 3, 'Number Feature')
        self.sheet.write(0, 4, 'Relevance to title Feature')
        self.sheet.write(0, 5, 'Sentence Usefulness')

        nounFeatureScoring = dict(featureDictionary[DictionaryType.NOUN_FEATURE])
        sentenceLengthFeature = dict(featureDictionary[DictionaryType.SENTENCE_LENGTH_FEATURE])
        hasNumberFeature = dict(featureDictionary[DictionaryType.HAS_NUMBER_FEATURE])
        relevanceToTitleFeature = dict(featureDictionary[DictionaryType.RELEVANCE_TO_TITLE_FEATURE])
        row_count = 1
        nounColumn = 1
        sentenceLength_column = 2
        hasNumberColumn = 3
        relevanceToTitleColumn = 4
        for i in nounFeatureScoring.keys():
            self.sheet.write(row_count, 0, i)
            self.sheet.write(row_count, nounColumn, nounFeatureScoring[i])
            self.sheet.write(row_count, sentenceLength_column, sentenceLengthFeature[i])
            self.sheet.write(row_count, hasNumberColumn, hasNumberFeature[i])
            self.sheet.write(row_count, relevanceToTitleColumn, relevanceToTitleFeature[i])
            row_count = row_count + 1

        wb.save(f'dataset/manual-dataset/article - {article_count}.xlsx')
