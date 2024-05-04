import random
# import time

# start_time = time.time()
NUMBER_OF_ROWS: int = 9
NUMBER_OF_COLUMNS: int = 9
SOLVED: bool = False
MAX_ATTEMPTS: int = 3500


def copy_array(arr: list[list[int]]) -> list[list[int]]:
    """Returns a copy of a given array by iterating, copies each row to a temp array and returns
    it. Ensuring that changes to the copy wont affect the original

    Args:
        arr (list[list[int]]): Array to copy

    Returns:
        list[list[int]]: Copy of array
    """
    temp_array:list[list[int]] = []
    for row in arr:
        temp_array.append(row.copy())

    return temp_array


def has_zeros(arr: list[list[int]]) -> bool:
    """Checks for any zeros (empty spaces) in the array

    Args:
        arr (list[list[int]]): Array to check

    Returns:
        bool: True if any zeroes left on the array
    """
    for row in arr:
        if 0 in row:
            return True

    return False


def get_row_numbers(row: int, column: int, sudoku_array: list[list[int]]) -> list[int]:
    """Returns a list of all numbers in the same row as a given (row, column) cell, excluding the cell
    itself

    Args:
        row (int): Cell row number
        column (int): Cell column number
        sudoku_array (list[list[int]]): Array to check the row of

    Returns:
        list[int]: List of all the numbers in the same row
    """
    row_numbers: list[int] = sudoku_array.copy()[row].copy()
    row_numbers.pop(column)

    return row_numbers


def get_column_numbers(
    row: int, column: int, sudoku_array: list[list[int]]
) -> list[int]:
    """Returns a list of all numbers in the same column as a given (row, column) cell, excluding the cell
    itself

    Args:
        row (int): Cell row number
        column (int): Cell column number
        sudoku_array (list[list[int]]): Array to check the column of

    Returns:
        list[int]: List of all the numbers in the same column
    """
    column_numbers: list[int] = []

    for n in range(9):
        if n != row:
            column_numbers.append(sudoku_array[n][column])

    return column_numbers


def get_nonet_coords(row: int, column: int) -> list[tuple[int, int]]:
    """Given a cell's (row, column), determines the current nonet where the cell is located.
    Returns the coordinates of the cells in said nonet

    None grid:
    1 2 3
    4 5 6
    7 8 9

    Nonet ranges:
    1. n<3 m<3
    2. n<3 3<=m<6
    3. n<3 6<=m
    4. 3<=n<6 m<3
    5. 3<=n<6 3<=m<6
    6. 3<=n<6 6<=m
    7. 6<=n m<3
    8. 6<=n 3<=m<6
    9. 6<=n 6<=m

    Args:
        row (int): Cell row number
        column (int): Cell column number

    Returns:
        list[tuple[int, int]]: List of cell coordinates in the same nonet
    """

    # Top 3 Nonets
    if row < 3 and column < 3:
        return [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

    if row < 3 and 3 <= column < 6:
        return [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)]

    if row < 3 and 6 <= column:
        return [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)]

    # Middle 3 Nonets
    if 3 <= row < 6 and column < 3:
        return [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)]

    if 3 <= row < 6 and 3 <= column < 6:
        return [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]

    if 3 <= row < 6 and 6 <= column:
        return [(3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)]

    # Bottom 3 Nonets
    if 6 <= row and column < 3:
        return [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)]

    if 6 <= row and 3 <= column < 6:
        return [(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)]

    if 6 <= row and 6 <= column:
        return [(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)]


def get_nonet_numbers(
    row: int, column: int, sudoku_array: list[list[int]]
) -> list[int]:
    """Given a cell's (row, column) and using a list of nonet cell coordinates determines the
    numbers in the same nonet as the cell, excluding the cell being checked

    Args:
        row (int): Cell row number
        column (int): Cell column number
        sudoku_array (list[list[int]]): Array to check the nonet of

    Returns:
        list[int]: List of numbers in the cell's nonet
    """

    nonet_coords: list[tuple[int, int]] = get_nonet_coords(row, column)

    nonet_numbers: list[int] = []

    for nonent_row, nonet_column in nonet_coords:
        if not (nonent_row == row and nonet_column == column):
            nonet_numbers.append(sudoku_array[nonent_row][nonet_column])

    return nonet_numbers


def find_posibilities_for_cell(
    row: int,
    column: int,
    lowest_amount_of_possibilities: int,
    lowest_possibilities_cell: tuple[int, int],
    lowest_possibilities_values: list[int],
    sudoku_array: list[list[int]],
) -> tuple[int, tuple[int, int], list[int]]:
    """Determines the possible numbers that a cell can have based on the numbers in the row, column, and nonet.
    If the amount of current possible numbers is the lowest yet discovered, it updates lowest_amount_of_possibilities, 
    lowest_possibilities_cell, and lowest_possibilities_values. Returns the updated values if so, if not returns the same values

    Args:
        row (int): Cell row number
        column (int): Cell column number
        lowest_amount_of_possibilities (int): Previously found lowest amount of possibilities in a cell
        lowest_possibilities_cell (tuple[int, int]): Previously found cell's (row, column) with lowest possibilities
        lowest_possibilities_values (list[int]): Previously found possible values for a given cell
        sudoku_array (list[list[int]]): Array to check the cell's possibilities

    Returns:
        tuple[int, tuple[int, int], list[int]]: Updated lowest_posibilities variables
    """

    numbers_in_row: list[int] = get_row_numbers(row, column, sudoku_array)
    numbers_in_column: list[int] = get_column_numbers(row, column, sudoku_array)
    numbers_in_nonet: list[int] = get_nonet_numbers(row, column, sudoku_array)

    posibilities: list[int] = []

    for i in range(1, 10):
        if (
            (i not in numbers_in_row)
            and (i not in numbers_in_column)
            and (i not in numbers_in_nonet)
        ):
            posibilities.append(i)

    if 0 < len(posibilities) < lowest_amount_of_possibilities:
        lowest_amount_of_possibilities = len(posibilities)
        lowest_possibilities_cell = (row, column)
        lowest_possibilities_values = posibilities

    return (
        lowest_amount_of_possibilities,
        lowest_possibilities_cell,
        lowest_possibilities_values,
    )


def sudoku_solver(sudoku_array: list[list[int]]) -> tuple[int, list[list[int]]]:
    """Attempts to solve a sudoku array by iterating through each cell, finding the lowest possibility cell
    and filling the value.
    If the possibilities is more than one, it choses at random. It keeps repeating until the sudoku is solved
    (has_zeros() returns false) or it rans out of possibilities (IndexError exception)

    Args:
        sudoku_array (list[list[int]]): Array to check

    Returns:
        tuple[int, list[list[int]]]: Tuple of amount of iterations and the array (solved or None)
    """
    global SOLVED

    iterations: int = 0
    lowest_amount_of_possibilities: int = 9999
    lowest_possibilities_cell = (9999, 9999)
    lowest_possibilities_values = []

    try:
        while has_zeros(sudoku_array):
            unedited_array: list[list[int]]= copy_array(sudoku_array)

            for row in range(9):
                for column in range(9):
                    if sudoku_array[row][column] == 0:

                        (
                            lowest_amount_of_possibilities,
                            lowest_possibilities_cell,
                            lowest_possibilities_values,
                        ) = find_posibilities_for_cell(
                            row,
                            column,
                            lowest_amount_of_possibilities,
                            lowest_possibilities_cell,
                            lowest_possibilities_values,
                            sudoku_array,
                        )

            if lowest_amount_of_possibilities == 1:
                sudoku_array[lowest_possibilities_cell[0]][
                    lowest_possibilities_cell[1]
                ] = lowest_possibilities_values[0]
            else:
                sudoku_array[lowest_possibilities_cell[0]][
                    lowest_possibilities_cell[1]
                ] = random.choice(lowest_possibilities_values)

            lowest_amount_of_possibilities = 9999
            lowest_possibilities_cell = (9999, 9999)
            lowest_possibilities_values = []

            if unedited_array == sudoku_array:
                break

            iterations = iterations + 1
        else:
            SOLVED = True

    except IndexError:
        return iterations, None

    return iterations, sudoku_array


def solver_thread(sudoku_array: list[list[int]]) -> list[list[int]]:
    """Thread that solves the array by repeating the sudoku_solver() function until a
    solved sudoku array is received.

    Args:
        sudoku_array (list[list[int]]): Array to solve

    Returns:
        list[list[int]]: Solved array or None if MAX_ATTEMPTS is reached
    """
    global SOLVED, MAX_ATTEMPTS

    attempts: int = 0
    total_iterations: int = 0

    while not SOLVED:
        temp_array: list[list[int]] = copy_array(sudoku_array)
        
        iterations: int
        solved_array: list[list[int]]

        iterations, solved_array = sudoku_solver(temp_array)

        # print(f"Attempt #{attempts} -> {iterations} iterations")

        total_iterations += iterations
        attempts += 1

        if solved_array != None:
            # print(f"Solve Time: {time.time() - start_time:.2f}s")

            if __name__ == "__main__":
                print(f"Total Attempts: {attempts}")
                print(f"Total Iterations: {total_iterations}")
            # print("Solved Sudoku Array:")

            # for row in solved_array:
            #     print(row)

            return solved_array

        if attempts >= MAX_ATTEMPTS:
            # print("Max Attempts Reached")
            return None



#Main for testing
def main():
    original_sudoku_array: list[list[int]] = [
        [0, 0, 0, 2, 0, 1, 0, 0, 0],
        [0, 0, 2, 0, 0, 5, 0, 0, 9],
        [0, 5, 0, 0, 8, 0, 0, 0, 6],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 5, 0, 0, 9, 0],
        [0, 8, 0, 0, 7, 0, 0, 0, 4],
        [0, 4, 0, 0, 9, 0, 0, 7, 0],
        [0, 2, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 8, 0, 1, 0, 0, 3, 0],
    ]

    print("Initial Sudoku Array:")
    for row in original_sudoku_array:
        print(row)

    print("----------------------------------")

    print("Solving...")

    temp_array: list[list[int]] = copy_array(original_sudoku_array)

    solved_array: list[list[int]] = solver_thread(temp_array)
    print("----------------------------------")

    print("Solved Sudoku Array:")
    for row in solved_array:
        print(row)


if __name__ == "__main__":
    main()
