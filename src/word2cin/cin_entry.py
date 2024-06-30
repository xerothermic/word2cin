
from dataclasses import dataclass


@dataclass
class CinEntry:
    """ Represent a cin file entry """
    key: str
    value: str
    src_name: str
    src_col: str
    weight: float = 0.0
    comment: str = ""

    def __lshift__(self, other):
        return self.merge(other)
    
    def merge(self, other):
        if self.key != other.key:
            raise ValueError(f"Merge failed! {self.key} != {other.key}")
        if self.value != other.value:
            raise ValueError(f"Merge failed! {self.value} != {other.value}")
        self.weight = self.weight + other.weight
        if other.comment != "":
            self.comment = self.comment + ";" + other.comment
        return self

    def __eq__(self, o: "CinEntry") -> bool:
        return (
            self.key == o.key and
            self.value == o.value and
            self.weight == o.weight
        )
    
    def __hash__(self) -> int:
        return hash(self.key + self.value + str(self.weight))