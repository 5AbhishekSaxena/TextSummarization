import csv

import xlrd
from xlwt import Workbook
from xlwt.compat import xrange

f = open("dataset/negative_words_hi.txt", "r")
sentiment_word_set = set()
pos = 0
neg = 0
for x in f:
  sentiment_word_set.add(x)
  neg += 1

f = open("dataset/positive_words_hi.txt", "r")
for x in f:
  sentiment_word_set.add(x)
  pos += 1

print(f'pos: {pos}, neg: {neg}, sum: {pos + neg}, words: {len(sentiment_word_set)}')


def saveData(sentiment_word_set, wb, sheet):

    row_count = 0

    for i in sentiment_word_set:
        sheet.write(row_count, 0, i)
        row_count = row_count + 1

    wb.save(f'dataset/manual-dataset/sentiment.xlsx')


def csvFromExcel():
    wb = xlrd.open_workbook(f'dataset/manual-dataset/sentiment.xlsx')
    sh = wb.sheet_by_index(0)
    csv_file = open(f'dataset/manual-dataset/sentiment.csv', 'w')
    wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

    for rownum in xrange(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    csv_file.close()


# self.article_count = article_count
# self.featureDictionary = featureDictionary
wb = Workbook()
# Set 1st Row
sheet = wb.add_sheet('Sheet 1')

saveData(sentiment_word_set, wb, sheet)
csvFromExcel()

