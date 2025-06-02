from itertools import combinations
import json
from typing import Callable, Sequence
import random

from models import Line, Square
from ops import sum_op, product_op


def check_single_solution(square: Square, solution: list[tuple[int, int]]) -> bool:
    for i in range(square.size):
        # Check row and column
        row = square.get_row(i)
        col = square.get_column(i)
        curr_row_total = 1 if square.op == product_op else 0
        curr_col_total = 1 if square.op == product_op else 0
        for idx in solution:
            if idx[0] == i:
                curr_row_total = square.op([curr_row_total, square.get_number(idx)])
            if idx[1] == i:
                curr_col_total = square.op([curr_col_total, square.get_number(idx)])
        if curr_row_total != row.target or curr_col_total != col.target:
            return False
    return True


def get_all_solutions(square: Square, solution_size: int) -> list[list[tuple[int, int]]]:
    # Generate all possible cell coordinates
    all_cells = [(i, j) for i in range(square.size) for j in range(square.size)]

    # Generate all possible combinations of solution_size cells
    all_solutions = []
    for combo in combinations(all_cells, solution_size):
        if check_single_solution(square, combo):
            all_solutions.append(list(combo))

    return all_solutions


def get_line_sizes(size: int, solution_size: int) -> list[int]:
    line_sizes = [2] * size
    solution_size_left = solution_size - sum(line_sizes)
    for i in range(solution_size_left):
        random_idx_permutation = list(range(size))
        random.shuffle(random_idx_permutation)
        line_sizes[next(idx for idx in random_idx_permutation if line_sizes[idx] < 4)] += 1
    return line_sizes


def generate_square(
    size: int,
    solution_size: int,
    op: Callable[[Sequence[int]], int],
) -> Square:
    min_number = 1 if op == sum_op else 2
    max_number = 9

    solution: list[tuple[int, int]] = []
    rows: list[Line] = []
    line_sizes = get_line_sizes(size, solution_size)
    for i in range(size):
        solution_line_idx = random.sample(range(size), line_sizes[i])
        solution.extend([(i, idx) for idx in solution_line_idx])
        line_numbers = [random.randint(min_number, max_number) for _ in range(size)]
        target = op([num for i, num in enumerate(line_numbers) if i in solution_line_idx])
        rows.append(Line(numbers=line_numbers, target=target))
    
    columns_targets = []
    for col_idx in range(size):
        numbers = []
        for row_idx, row in enumerate(rows):
            if (row_idx, col_idx) in solution:
                numbers.append(row.numbers[col_idx])
        columns_targets.append(op(numbers))

    return Square(rows=rows, columns_targets=columns_targets, op=op)


def main():
    problems_and_solutions = []
    with open("data/problems_and_solutions.json", "r") as f:
        problems_and_solutions = json.load(f)

    for i in range(1000):
        print(f"iteration {i}")
        solution_size = random.randint(11, 15)
        generated_square = generate_square(5, solution_size, random.choice([sum_op, product_op]))
        generated_square_solutions = get_all_solutions(generated_square, solution_size)
        if len(generated_square_solutions) > 1:
            continue

        problem_data = {
            "square": generated_square.to_dict(),
            "solution": generated_square_solutions[0]
        }
        problems_and_solutions.append(problem_data)
        print(f"Generated {len(problems_and_solutions)} problems")
    
        with open("data/problems_and_solutions.json", "w") as f:
            json.dump(problems_and_solutions, f, indent=4)
    
    print(f"Successfully saved {len(problems_and_solutions)} problems to data/problems_and_solutions.json")


if __name__ == "__main__":
    main()
