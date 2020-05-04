class Type:
    DEFAULT = 0
    TERM_FREQUENCY = 1
    TERM_UNIQUENESS = 2
    INVERSE_DOCUMENT_FREQUENCY = 3


class DictionaryType:
    NOUN_FEATURE = 'noun_feature'
    SENTENCE_LENGTH_FEATURE = 'sentence_length_feature'
    HAS_NUMBER_FEATURE = 'has_number_feature'
    RELEVANCE_TO_TITLE_FEATURE = 'relevance_to_title_feature'
    AGGREGATE_IDF = 'aggregate_idf'
    AGGREGATE_TF = 'aggregate_tf'
