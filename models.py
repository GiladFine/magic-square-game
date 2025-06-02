from dataclasses import dataclass
from typing import Callable, Sequence
from ops import sum_op, product_op


@dataclass
class Line:
    numbers: list[int]
    target: int

    def to_dict(self) -> dict:
        return {"numbers": self.numbers, "target": self.target}

    @classmethod
    def from_dict(cls, data: dict) -> "Line":
        return cls(numbers=data["numbers"], target=data["target"])

@dataclass
class Square:
    rows: list[Line]
    columns: list[Line]
    op: Callable[[Sequence[int]], int]
    size: int

    def __init__(self, rows: list[Line], columns_targets: list[int], op: Callable[[Sequence[int]], int]):
        self.op = op
        self.rows = rows
        self.size = len(rows)
        self.columns = [
            Line(numbers=[row.numbers[i] for row in rows], target=columns_targets[i])
            for i in range(self.size)
        ]

    def get_number(self, idx: tuple[int, int]) -> int:
        assert 0 <= idx[0] < self.size, "Row index out of bounds"
        assert 0 <= idx[1] < self.size, "Column index out of bounds"
        return self.rows[idx[0]].numbers[idx[1]]

    def get_row(self, idx: int) -> Line:
        assert 0 <= idx < self.size, "Line index out of bounds"
        return self.rows[idx]

    def get_column(self, idx: int) -> Line:
        assert 0 <= idx < self.size, "Column index out of bounds"
        return self.columns[idx]

    def __post_init__(self):
        assert len(self.rows) == len(self.columns) == self.size
        assert all(len(row.numbers) == self.size for row in self.rows)
        assert all(len(column.numbers) == self.size for column in self.columns)

        for row_idx, row in enumerate(self.rows):
            for col_idx, number in enumerate(row.numbers):
                assert number == self.columns[col_idx].numbers[row_idx]

    def to_dict(self) -> dict:
        op_name = "sum" if self.op == sum_op else "product"
        return {
            "rows": [row.to_dict() for row in self.rows],
            "columns_targets": [col.target for col in self.columns],
            "op": op_name,
            "size": self.size
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Square":
        op = sum_op if data["op"] == "sum" else product_op
        rows = [Line.from_dict(row_data) for row_data in data["rows"]]
        return cls(rows=rows, columns_targets=data["columns_targets"], op=op)
