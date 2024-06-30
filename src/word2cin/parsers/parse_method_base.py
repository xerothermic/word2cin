from abc import ABC, abstractmethod

import pandas as pd

from word2cin.cin_entry import CinEntry

class ParseMethodBase(ABC):
    @abstractmethod
    def parse(self, data_source_name: str, dataframe: pd.DataFrame) -> dict[str, CinEntry]:
        return