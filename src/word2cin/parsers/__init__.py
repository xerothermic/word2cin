
from word2cin.parsers.parse_single_word import ParseSingleWord
from word2cin.parsers.parse_single_word_from_phrase import ParseSingleWordFromPhrase


PARSE_METHODS = {
    "parse_single_word_v2": ParseSingleWord,
    "parse_single_word_from_phrase": ParseSingleWordFromPhrase,
}
