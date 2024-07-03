import logging
from pandas import DataFrame
from word2cin.cin_entry import CinEntry
from word2cin.parsers.parse_method_base import ParseMethodBase

logger = logging.getLogger(__name__)

class ParseBun5PehImPhrase(ParseMethodBase):
    """ parse 文|白|替|俗 """

    def parse(self, data_source_name: str, taigi_df: DataFrame) -> list[CinEntry]:
        cin_list = []
        alternative_phrase = taigi_df[taigi_df.KipInput.str.contains("(文|白|替|俗)", na=False)]
        # Drop -- / TODO: Handle this in the future
        alternative_phrase = alternative_phrase[~alternative_phrase.KipInput.str.contains("--|/")]
        for _idx, row in alternative_phrase.iterrows():
            kip_input = row["KipInput"].split("(")[0]
            kip_utf8 = row["KipUnicode"].split("(")[0]
            if not str.isascii(kip_input):
                logger.debug(f"KipInput is not ascii for {row=}")
            else:
                cin_list.append(
                    CinEntry(
                        key=kip_input,
                        value=kip_utf8,
                        src_name=data_source_name,
                        src_col="KipUnicode",
                        parse_method=self.__class__.__name__,
                        weight=0.0,
                    )
                )
                if row["HanLoTaibunKip"].strip() != "":
                    cin_list.append(
                        CinEntry(
                            key=kip_input,
                            value=row["HanLoTaibunKip"],
                            src_name=data_source_name,
                            src_col="HanLoTaibunKip",
                            parse_method=self.__class__.__name__,
                            weight=0.0,
                        )
                    )
                else:
                    logger.debug(f"HanLoTaibunKip is empty for {row=}")
            # Add other input if available
            if "KipInputOthers" in row and isinstance(row["KipInputOthers"], str):
                # TODO: handle - and /
                if row["KipInputOthers"].count('-') or row["KipInputOthers"].count('/'):
                    continue
                kip_input_others = row["KipInputOthers"].split("(")[0]
                kip_utf8_others = row["KipUnicodeOthers"].split("(")[0]
                cin_list.append(
                    CinEntry(
                        key=kip_input_others,
                        value=kip_utf8_others,
                        src_name=data_source_name,
                        src_col="KipUnicodeOthers",
                        parse_method=self.__class__.__name__,
                        weight=0.0,
                    )
                )
        return cin_list
