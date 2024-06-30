
from collections import defaultdict
import logging
import pandas as pd
from word2cin.cin_entry import CinEntry
from word2cin.parsers.parse_method_base import ParseMethodBase

logger = logging.getLogger(__name__)


class ParseSingleWord(ParseMethodBase):
    """ convert single word to unicode or hanlo """

    def parse(self, data_source_name: str, taigi_df: pd.DataFrame) -> dict[str, CinEntry]:
        cin_map = defaultdict(set)

        # Ignore KipInput with () / space and japanese
        single_word_df = taigi_df[~taigi_df.KipInput.astype(str).str.contains("\\(|/|-| |な")]
        for _idx, row in single_word_df.iterrows():
            try:
                k = row["KipInput"].lower()
            except AttributeError as e:
                logger.warning(
                    "Failed to convert KipInput to lower case\n" +
                    f"{row}\n" +
                    f"Err: {e}")
                continue
            v1 = row["KipUnicode"].lower()
            cin_map[k].add(
                CinEntry(
                    k,
                    v1,
                    src_name=data_source_name,
                    src_col="KipUnicode",
                    weight=0,
                )
            )
            v2 = row["HanLoTaibunKip"]
            if v2.strip() != "":
                cin_map[k].add(
                    CinEntry(
                        k,
                        v2,
                        src_name=data_source_name,
                        src_col="HanLoTaibunKip",
                        weight=0,
                    )
                )
            else:
                logger.warning(f"{k} has no HanLoTaibunKip")

        return cin_map
