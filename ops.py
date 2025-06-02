import operator
from typing import Sequence
from functools import reduce


def sum_op(numbers: Sequence[int]) -> int:
    return sum(numbers)
    
def product_op(numbers: Sequence[int]) -> int:
    return reduce(operator.mul, numbers, 1)
