from textblob import TextBlob

from TextSummarization.Utils import randomnumber, randomword
import string

print(f'random number: {randomnumber()}')
print(f'random word: {randomword()}')
str = """#$%&*@^*!"""
print(f'sgtring punctuations: {str}')


tb = TextBlob("Helo World!")
print(tb.detect_language())