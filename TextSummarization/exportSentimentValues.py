
import xlrd
import xlwt
from xlwt import Workbook
from xlwt.compat import xrange


class ExportSentimentValues:
    def __init__(self):
        self.wb = Workbook()
        # Set 1st Row
        self.sheet = self.wb.add_sheet('Sheet 1')

    def save_sentences(self, summary, pos_count, neg_count):
        numberOfSentences = len(summary)
        row_count = 0
        pos_count_row = 1
        neg_count_row = 2

        for i in summary:
            self.sheet.write(row_count, 0, i)
            self.sheet.write(row_count, pos_count_row, pos_count[i])
            self.sheet.write(row_count, neg_count_row, neg_count[i])

        self.wb.save(f'dataset/manual-dataset/sentimentlist.xlsx')