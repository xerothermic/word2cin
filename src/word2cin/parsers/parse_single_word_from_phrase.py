import logging
import pandas as pd
from word2cin.cin_entry import CinEntry
from word2cin.parsers.parse_method_base import ParseMethodBase

logger = logging.getLogger(__name__)


class ParseSingleWordFromPhrase(ParseMethodBase):
    """ parse phrase with pattern <word>-<word> ... to single word unicode and hanlo """

    def _put_kip_unicode(self, src_name, kip_input_list,
                         kip_utf8_list) -> list[CinEntry]:
        cin_list = []
        for k, v in zip(kip_input_list, kip_utf8_list):
            cin_list.append(
                CinEntry(
                    k,
                    v,
                    src_name,
                    src_col="KipUnicode",
                    parse_method=self.__class__.__name__,
                )
            )
        return cin_list

    def _put_kip_hanlo(self, src_name, kip_input_list,
                       kip_hanlo_list) -> list[CinEntry]:
        cin_list = []
        for k, v in zip(kip_input_list, kip_hanlo_list):
            cin_list.append(
                CinEntry(
                    k,
                    v,
                    src_name,
                    src_col="KipUnicode",
                    parse_method=self.__class__.__name__,
                )
            )
        return cin_list

    def parse(self, src_name: str, taigi_df: pd.DataFrame) -> list[CinEntry]:
        cin_list = []
        single_phrase_df = taigi_df[
            (~taigi_df.KipInput.str.contains("/", na=False)) &
            taigi_df.KipInput.str.contains("^[a-zA-Z2345789]+(-[a-zA-Z2345789]+)+$")]
        for _idx, row in single_phrase_df.iterrows():
            kip_input_list = row["KipInput"].split("-")
            kip_utf8_list = row["KipUnicode"].split("-")
            if len(kip_input_list) == len(kip_utf8_list):
                cin_list.extend(
                    self._put_kip_unicode(
                        src_name,
                        kip_input_list,
                        kip_utf8_list))
            else:
                logger.debug(
                    f"{len(kip_input_list)=} != {len(kip_utf8_list)=}")

            if "HanLoTaibunKip" not in row:
                continue
            if isinstance(row["HanLoTaibunKip"], float):
                logger.debug(
                    f"HanLoTaibunKip has unexpected float type for {row=}")
                continue
            kip_hanlo_list = row["HanLoTaibunKip"]
            if len(kip_input_list) == len(kip_hanlo_list):
                cin_list.extend(
                    self._put_kip_hanlo(
                        src_name,
                        kip_input_list,
                        kip_hanlo_list))
            else:
                logger.debug(f"{kip_input_list} != {kip_hanlo_list}")
        return cin_list
