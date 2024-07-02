import logging
from pandas import DataFrame
from word2cin.cin_entry import CinEntry
from word2cin.parsers.parse_method_base import ParseMethodBase

logger = logging.getLogger(__name__)


class ParseKhiunnKhau2TshaPhrase(ParseMethodBase):
    def parse(self, data_source_name: str, taigi_df: DataFrame) -> list[CinEntry]:
        cin_list = []
        df = taigi_df[taigi_df.KipInput.str.contains("/", na=False)]
        df2 = df[["KipInput","KipUnicode"]].map(lambda x: x.split("/"))
        if "HanLoTaibunKip" in df.columns:
            df2["HanLoTaibunKip"] = df["HanLoTaibunKip"]
        # expand each / to two rows
        df2 = df2.explode(["KipInput","KipUnicode"])
        for _idx, row in df2.iterrows():
            k = row["KipInput"].replace(" ", "").replace("-", "")
            cin_list.append(
                CinEntry(
                    key=k,
                    value=row["KipUnicode"],
                    src_name=data_source_name,
                    src_col="KipUnicode",
                    parse_method=self.__class__.__name__,
                    weight=0.0,
                )
            )
            if "HanLoTaibunKip" not in row:
                continue
            elif row["HanLoTaibunKip"].strip() == "":
                logger.warning(f"HanLoTaibunKip is empty for {row=}")
                continue
            cin_list.append(
                CinEntry(
                    key=k,
                    value=row["HanLoTaibunKip"],
                    src_name=data_source_name,
                    src_col="HanLoTaibunKip",
                    parse_method=self.__class__.__name__,
                    weight=0.0,
                )
            )
        return cin_list
