import csv
from TextSummarization.ProcessSentences import ProcessSentences
from TextSummarization.ProcessStopwords import processStopwords
from MultiLanguageSummarizer import MultiLanguageSummarizer as ms
from TextSummarization.Utils import getDictionaryAsString
from TextSummarization.Utils import convertListToString
from TextSummarization.Constants import Type
from TextSummarization.BaseNewsArticle import BaseNewsArticle
from textblob import TextBlob
from textblob.exceptions import NotTranslated
from TextSummarization.nltk_implementation import word_tokenize
from TextSummarization.nltk_implementation import sentence_tokenizer

with open('dataset/test_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    correct = 0
    incorrect = 0
    correctS = 0
    incorrectS = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        elif len(row[1].strip()) > 5 and "VIDEO" not in row[2] and TextBlob(row[2][:10]).detect_language() == 'hi':

            heading, given_summary, article = row[0], row[1], row[2]
            try:
                if "।" in article:
                    article = article.replace("।", ".")  # FIXME for summarization
                generated_summary = ms.summarize_text(article, split=True)
                # print(f'Summary using library:\n{generated_summary}\n')
            except ValueError as e:
                continue
                # print(f'Error raised: {e}')
            else:

                baseNewsArticle = BaseNewsArticle(heading=heading, article=article,
                                                  summary=given_summary)
                print(
                    f'Article #{line_count}\nHeading:\n{heading}  \n\nSummary:\n{given_summary} '
                    f'\n\nArticle:\n{article}\n')
                print(f'Summary using library:\n{convertListToString(generated_summary)}\n')

                processSentences = ProcessSentences(baseNewsArticle)
                lengthOfHeading = len(heading.strip().split(" "))
                numberOfWordsInArticle = baseNewsArticle.getTotalNumberOfWords()
                numberOfImpWords = len(processStopwords(baseNewsArticle))
                numberOfSentences = len(processSentences.getTokenizedSentences())
                termFrequency = getDictionaryAsString(processSentences.calculateTermFrequency(),
                                                      Type.TERM_FREQUENCY)
                inverseDocumentFrequency = getDictionaryAsString(processSentences.calculateInverseDocumentFrequency(),
                                                                 Type.INVERSE_DOCUMENT_FREQUENCY)

                termUniqueness = getDictionaryAsString(processSentences.calculateTermUniqueness(),
                                                       Type.TERM_UNIQUENESS)
                numberOfStopWordsRemoved = numberOfWordsInArticle - numberOfImpWords
                lengthOfGivenSummary = len(given_summary.strip().split(" "))
                medium_summary = processSentences.generate_summary(1.5)

                # numberOfWordsUsingCLTKLib = len(word_tokenize(baseNewsArticle.getArticle()))
                # numberOfSentencesUsingCLTKLib = len(sentence_tokenizer(baseNewsArticle.getArticle()))

                # print(f' Total number of wortds in article: {numberOfWordsInArticle}'
                #       f'\nNumber of imp words: {numberOfImpWords}')
                try:
                    sentimentBlob = TextBlob(str(TextBlob(convertListToString(generated_summary)).translate())).sentiment
                except NotTranslated:
                    sentimentBlob = 0.0
                if sentimentBlob is TextBlob:
                    print(f'\n\nSentimentBlob: {sentimentBlob}\n\n')

                if numberOfSentences < 10:
                    print(f'Sentences: {baseNewsArticle.getArticle()}')
                print(f'\nMetaData.... '
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
                      f'\nGiven Summary:{lengthOfGivenSummary}'
                      f'\nGenerated summary using MultiLangSummarizer({len(convertListToString(generated_summary).strip().split(" "))}):'
                      f' {convertListToString(generated_summary)}'  # FIXME
                      f'\nGenerated summary using Medium Article'
                      f'({len(medium_summary.strip().split(" "))}): {medium_summary}' # FIXME: IMPORTANT
                      # f'\nNumber Of words using cltk lib : {numberOfWordsUsingCLTKLib}'
                      # f'\nNumber Of sentences using cltk lib : {numberOfSentencesUsingCLTKLib}'
                      f'\nSentiment: {sentimentBlob}'
                    )
            # if numberOfWordsInArticle == numberOfWordsUsingCLTKLib:
            #     correct += 1
            # else:
            #     incorrect += 1
            #
            # if numberOfSentences == numberOfSentencesUsingCLTKLib:
            #     correctS += 1
            # else:
            #     incorrectS += 1

            print("=====" * 50 + '\n')

            line_count += 1

            if line_count == 21:
                break

print(f'Processed {line_count} lines.')
# print(f'\nWords\nCorrect : {correct}\nIncorrect: {incorrect}')
# print(f'\n\nSentences\nCorrect : {correct}\nIncorrect: {incorrect}')