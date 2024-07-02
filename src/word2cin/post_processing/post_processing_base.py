

from abc import ABC, abstractmethod

from word2cin.cin_entry import CinEntry


class PostProcessingBase(ABC):
    @abstractmethod
    def process(
            self,
            cin_data: list[CinEntry],
     ) -> list[CinEntry]:
        return