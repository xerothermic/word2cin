
import logging
import pandas as pd
from word2cin.cin_entry import CinEntry
from word2cin.parsers.parse_method_base import ParseMethodBase

logger = logging.getLogger(__name__)


class ParseSingleWord(ParseMethodBase):
    """ convert single word to unicode or hanlo """

    def _get_key(self, kip_input: str):
        try:
            k = kip_input.lower()
        except AttributeError:
            k = ""

        return k

    def _get_cin_from_unicode(self, data_source_name, k, v):
        return CinEntry(
            k,
            v,
            src_name=data_source_name,
            src_col="KipUnicode",
            parse_method=self.__class__.__name__,
            weight=0,
        )

    def _get_cin_from_hanlo(self, data_source_name, k, v):
        return CinEntry(
            k,
            v,
            src_name=data_source_name,
            src_col="HanLoTaibunKip",
            parse_method=self.__class__.__name__,
            weight=0,
        )

    def parse(
            self,
            data_source_name: str,
            taigi_df: pd.DataFrame) -> list[CinEntry]:
        cin_list = []

        # Ignore KipInput with () / space and japanese
        single_word_df = taigi_df[
            taigi_df.KipInput.astype(str).str.contains("^[a-z][A-Z]")
        ]
        for _idx, row in single_word_df.iterrows():
            k = self._get_key(row["KipInput"])
            if not k:
                logging.warning(f"fail to convert KipInput: {row=}")
                continue
            v1 = row["KipUnicode"].lower()
            cin_entry = self._get_cin_from_unicode(data_source_name, k, v1)
            cin_list.append(cin_entry)
            v2 = row["HanLoTaibunKip"]
            if not isinstance(v2, str):
                logger.warning(f"HanLoTaibunKip is not str for {row=}")
            elif v2.strip() == "":
                logger.debug(f"{k} has no HanLoTaibunKip")
            else:
                cin_entry = self._get_cin_from_hanlo(data_source_name, k, v2)
                cin_list.append(cin_entry)

        return cin_list
