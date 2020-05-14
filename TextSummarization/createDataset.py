from TextSummarization.BaseNewsArticle import BaseNewsArticle
import csv

import xlrd
import xlwt
from xlwt import Workbook
from xlwt.compat import xrange

from textblob import TextBlob


class Temp:
    def __init__(self, baseNewsArticle: BaseNewsArticle, article_number: int):
        self.baseNewsArticle = baseNewsArticle
        self.article_number = article_number


def isEnglish(s: str) -> bool:
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


articleList = []
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
        elif len(row[1].strip()) > 5 and "VIDEO" not in row[2] and isEnglish(row[2][:10]) is False:
            heading, given_summary, article = row[0], row[1], row[2]
            try:
                if "।" in article:
                    article = article.replace("।", ".")  # FIXME for summarization
                    # temp = helper(article)
                    # print(f'Summary using library:\n{generated_summary}\n')
            except ValueError as e:
                continue
                # print(f'Error raised: {e}')
            else:

                baseNewsArticle = BaseNewsArticle(heading=heading, article=article,
                                                  summary=given_summary)
                temp = Temp(baseNewsArticle, article_count)
                articleList.append(temp)
                article_count += 1

            if article_count == 2:
                break


def exportToCsv():
    wb = Workbook()
    # Set 1st Row
    sheet = wb.add_sheet('Sheet 1')

    row_count = 0
    articleCountColumn = 0
    articleTitleColumn = 1
    articleSummaryColumn = 2
    articleTextColumn = 3
    articleEnglishTextColumn = 4

    for i in articleList:
        sheet.write(row_count, articleCountColumn, i.article_number)
        sheet.write(row_count, articleTitleColumn, i.baseNewsArticle.getHeading())
        sheet.write(row_count, articleSummaryColumn, i.baseNewsArticle.getSummary())
        sheet.write(row_count, articleTextColumn, i.baseNewsArticle.getArticle())
        sheet.write(row_count, articleEnglishTextColumn, i.baseNewsArticle.getEnglishArticle())
        row_count = row_count + 1

    wb.save(f'dataset/manual-dataset/article - temp_dataset.xlsx')


exportToCsv()
