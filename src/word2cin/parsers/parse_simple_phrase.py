import logging
from pandas import DataFrame
from word2cin.cin_entry import CinEntry
from word2cin.parsers.parse_method_base import ParseMethodBase

logger = logging.getLogger(__name__)

class ParseSimplePhrase(ParseMethodBase):
    """
    parse phrase with pattern <word>-<word> ..., so we can type longer phrase at a time
    """
    def parse(self, data_source_name: str, taigi_df: DataFrame) -> list[CinEntry]:
        cin_list = []
        # ignore /
        single_phrase_df = taigi_df[
            (~taigi_df.KipInput.str.contains("/", na=False)) &
            taigi_df.KipInput.str.contains("^[a-zA-Z2345789]+(-[a-zA-Z2345789]+)+$")]
        logger.info(single_phrase_df.shape)
        for _idx, row in single_phrase_df.iterrows():
            kip_input = row["KipInput"].replace("-", "")
            cin_list.append(
                CinEntry(
                    key=kip_input,
                    value=row["KipUnicode"],
                    src_name=data_source_name,
                    src_col="KipUnicode",
                    parse_method=self.__class__.__name__,
                    weight=0.0,
                )
            )
            if "HanLoTaibunKip" not in row:
                continue
            if not isinstance(row["HanLoTaibunKip"], str):
                logger.debug(f"HanLoTaibunKip is not str for {row=}")
            elif row["HanLoTaibunKip"].strip() == "":
                logger.debug(f"no HanLoTaibunKip for {row=}")
            else:
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
        return cin_list
