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
    word_tokenizer = WordTokenizer('sanskrit')
    return word_tokenizer.tokenize(text)


def sentence_tokenizer(text):
    text.replace(".", " | ")
    text.replace("\n", "").strip()
    hindi_text_sentence_tokenize = TokenizeSentence('hindi').tokenize(text)
    return hindi_text_sentence_tokenize
