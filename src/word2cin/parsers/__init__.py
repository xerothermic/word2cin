from word2cin.parsers.parse_bun5_peh_im_phrase import ParseBun5PehImPhrase
from word2cin.parsers.parse_khiunn_khau2_tsha_phrase import ParseKhiunnKhau2TshaPhrase
from word2cin.parsers.parse_one_to_one import ParseOneToOne
from word2cin.parsers.parse_simple_phrase import ParseSimplePhrase
from word2cin.parsers.parse_single_word import ParseSingleWord
from word2cin.parsers.parse_single_word_from_phrase import ParseSingleWordFromPhrase


PARSE_METHODS = {
    "parse_single_word_v2": ParseSingleWord,
    "parse_single_word_from_phrase": ParseSingleWordFromPhrase,
    "parse_simple_phrase": ParseSimplePhrase,
    "parse_bun5_peh_im_phrase": ParseBun5PehImPhrase,
    "parse_khiunn_khau2_tsha_phrase": ParseKhiunnKhau2TshaPhrase,
    "parse_one_to_one": ParseOneToOne,
}
