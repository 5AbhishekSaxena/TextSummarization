from cltk.stop.classical_hindi.stops import STOPS_LIST
from cltk.tokenize.word import WordTokenizer
from cltk.tokenize.sentence import TokenizeSentence
from cltk.corpus.utils.importer import CorpusImporter


def get_hindi_stop_words():
    hindi_stop_words = set(STOPS_LIST)
    return hindi_stop_words


def getHindiCorpus():
    ci = CorpusImporter('hindi')
    return ci.list_corpora


def word_tokenize(text):
    print("Word Tokenizer triggered")
    word_tokenizer = WordTokenizer('sanskrit')
    # print("word tokenize: ", word_tokenizer.tokenize(self.sentence))
    return word_tokenizer.tokenize(text)


def sentence_tokenizer(text):
    text.replace(".", " | ")
    text.replace("\n", "").strip()
    print("Sentence Tokenizer triggered")
    hindi_text_sentence_tokenize = TokenizeSentence('hindi').tokenize(text)
    return hindi_text_sentence_tokenize
    # print(f'hindi text sentence tokenize {hindi_text_sentence_tokenize}')
    # temp_sentence = ""
    # # print("\nHindi sentence tokenize")
    # for i in hindi_text_sentence_tokenize:
    #     # print(i)
    #     if len(temp_sentence) > 0:
    #         temp_sentence = temp_sentence + "\n"
    #
    #     temp_sentence = temp_sentence + i
    # # print(temp_sentence)
    # return temp_sentence.strip()
