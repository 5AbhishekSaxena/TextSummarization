import xlrd
import xlwt
from xlwt import Workbook
from xlwt.compat import xrange


class ExportSummary:
    def __init__(self):
        self.wb = Workbook()
        # Set 1st Row
        self.sheet = self.wb.add_sheet('Sheet 1')

    def save_sentences(self, summary):
        numberOfSentences = len(summary)
        row_count = 0

        for i in summary:
            self.sheet.write(row_count, 0, i)

        self.wb.save(f'dataset/manual-dataset/summary.xlsx')