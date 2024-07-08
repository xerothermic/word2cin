import logging
from pandas import DataFrame
from word2cin.cin_entry import CinEntry
from word2cin.parsers.parse_method_base import ParseMethodBase

logger = logging.getLogger(__name__)

class ParseOneToOne(ParseMethodBase):
    """
    For Google Sheet, we want to parse one to one (e.g. KipInput -> KipUnicode)
    """
    def parse(self, data_source_name: str, taigi_df: DataFrame) -> list[CinEntry]:
        cin_list = []
        for _idx, row in taigi_df.iterrows():
            kip_input = row["KipInput"]
            weight = row["weight"]
            cin_list.append(
                CinEntry(
                    key=kip_input,
                    value=row["KipUnicode"],
                    src_name=data_source_name,
                    src_col="KipUnicode",
                    parse_method=self.__class__.__name__,
                    weight=weight,
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
                        weight=weight,
                    )
                )
        return cin_list