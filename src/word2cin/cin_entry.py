from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class CinEntry:
    """ Represent a cin file entry """
    key: str
    value: str
    src_name: str
    src_col: str
    parse_method: str
    weight: float = 0.0
    comment: str = ""

    def __lshift__(self, other: "CinEntry"):
        " <<= to merge two CinEntries"
        if self.key != other.key:
            raise ValueError(f"Merge failed! {self.key} != {other.key}")
        if self.value != other.value:
            raise ValueError(f"Merge failed! {self.value} != {other.value}")
        self.weight = self.weight + other.weight
        self.src_name = self._merge_str(self.src_name, other.src_name)
        self.src_col = self._merge_str(self.src_col, other.src_col)
        self.parse_method = self._merge_str(
            self.parse_method, other.parse_method)
        self.comment = self._merge_str(self.comment, other.comment)
        return self

    def _merge_str(self, a, b):
        set_a = set(a.split(";"))
        set_b = set(b.split(";"))
        set_a.update(set_b)
        return ';'.join(set_a)

    def __eq__(self, o: "CinEntry") -> bool:
        return (
            self.key == o.key and
            self.value == o.value and
            self.weight == o.weight and
            set(self.src_name.split(";")) == set(o.src_name.split(";")) and
            set(self.src_col.split(";")) == set(o.src_col.split(";")) and
            set(self.parse_method.split(";")) == set(o.parse_method.split(";")) and
            set(self.comment.split(";")) == set(o.comment.split(";"))
        )

    def __hash__(self) -> int:
        return hash(self.key + self.value + str(self.weight))
