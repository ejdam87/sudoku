from typing import List, Tuple
from functools import cmp_to_key
import random


Board = List[List[int]]
Square = Tuple[int, int]


class Sudoku:

    def __init__(self, board: Board) -> None:

        self.board = board
        self.squares = [(i, j) for i in range(3) for j in range(3)]


    def fill_board(self) -> None:

        self.place_number(self.board, self.squares, 1)


    def place_number(self,
                     board: Board,
                     squares_left: List[Square],
                     num: int) -> bool:

        if squares_left == []:

            if num == 9:
                return True

            if self.place_number(board, self.squares, num + 1):
                return True

            return

        squares_left = sorted(squares_left, key=cmp_to_key(self.compare_squares))
        possible = self.get_possible(board, squares_left[0], num)

        if possible == []:
            return

        for option in possible:

            x, y = option

            prev = board[x][y]
            board[x][y] = num

            if self.place_number(board, squares_left[1:], num):
                return True

            board[x][y] = prev


    def compare_squares(self, s1: Square, s2: Square) -> int:
        
        return self.count_filled(s1) - self.count_filled(s2)

    def compare_options(self, o1: Tuple[int, int], o2: Tuple[int, int]) -> int:
        
        a = self.count_row(o1[0]) - self.count_row(o2[0])
        b = self.count_col(o1[1]) - self.count_col(o2[1])

        if abs(a) > abs(b):
            return a

        return b

    def count_row(self, row: int) -> int:

        total = 0
        for num in self.board[row]:
            if num != 0:
                total += 1

        return total

    def count_col(self, col: int) -> int:

        total = 0

        for row in self.board:

            if row[col] != 0:
                total += 1

        return total

    def count_filled(self, square: Square) -> int:

        total = 0
        for i in range(3 * square[0], 3 * square[0] + 3):
            for j in range(3 * square[1], 3 * square[1] + 3):
                
                if self.board[i][j] != 0:
                    total += 1

        return total

    def check_squares(self, board: Board, num: int) -> bool:

        present = False

        for square in self.squares:

            for i in range(3 * square[0], 3 * square[0] + 3):
                for j in range(3 * square[1], 3 * square[1] + 3):

                    if num == board[i][j]:
                        present = True

            if not present:
                return False

            present = False

        return True

    def get_possible(self, board: Board, square: Square, num: int) -> List[Tuple[int, int]]:

        possible = []
        for row in range(3 * square[0], 3 * square[0] + 3):

            for column in range(3 * square[1], 3 * square[1] + 3):

                if board[row][column] == num:
                    return [(row, column)]

                if board[row][column] != 0:
                    continue

                if self.is_in_row(board, num, row):
                    continue

                if not self.is_in_column(board, num, column):
                    possible.append((row, column))

        return possible


    def is_in_square(self, board: Board, square: Square, num: int) -> bool:

        for i in range(3 * square[0], 3 * square[0] + 3):
            for j in range(3 * square[1], 3 * square[1] + 3):
                if board[i][j] == num:
                    return True

        return False

    def is_in_row(self, board: Board, num: int, row: int) -> bool:
        
        return num in board[row]

    def is_in_column(self, board: Board, num: int, column: int) -> bool:

        for row in board:

            if num == row[column]:
                return True

        return False


    def draw_board(self) -> None:

        self._draw_line(0)

        for i in range(9):

            print("│", end="")

            for j in range(9):

                if j % 3 == 2:
                    sep = "│"
                else:
                    sep = " "

                print(f" {self._draw_value(self.board[i][j])} {sep}", end="")

            print()

            self._draw_line(i + 1)

    def _draw_line(self, row: int) -> None:

        first, last, mid, base = "", "", "", "─"

        if row == 0:
            first, last, mid = "┌", "┐", "┬"

        elif row == 9:
            first, last, mid = "└", "┘", "┴"

        else:
            first, last, mid = "├", "┤", "┼"

        if row % 3 != 0:
            mid, base = "┼", " "

        print(first, end="")
        for i in range(9):

            if i == 8:
                print(3 * base, end="")
                break

            print(3 * base + mid, end="")

        print(last)

    def _draw_value(self, val: int) -> str:

        if val == 0:
            return " "

        return str(val)



chars = ["┌", "┐", "┘", "└", "│", "┤", "├", "┬", "┴", "┼", "─"]


test_board_2 = [

            [1, 0, 0,    0, 0, 0,    0, 0, 0],
            [0, 0, 0,    0, 0, 0,    0, 0, 0],
            [0, 0, 0,    0, 0, 0,    0, 0, 0],

            [0, 0, 0,    0, 0, 0,    0, 0, 0],
            [0, 0, 0,    0, 1, 0,    0, 0, 0],
            [0, 0, 0,    0, 0, 0,    0, 0, 0],

            [0, 0, 0,    0, 0, 0,    0, 0, 0],
            [0, 0, 0,    0, 0, 0,    0, 0, 0],
            [0, 0, 0,    0, 0, 0,    0, 0, 0]

            ]

test_board = [

            [0, 0, 0,    2, 6, 0,    7, 0, 1],
            [6, 8, 0,    0, 7, 0,    0, 9, 0],
            [1, 9, 0,    0, 0, 4,    5, 0, 0],

            [8, 2, 0,    1, 0, 0,    0, 4, 0],
            [0, 0, 4,    6, 0, 2,    9, 0, 0],
            [0, 5, 0,    0, 0, 3,    0, 2, 8],

            [0, 0, 9,    3, 0, 0,    0, 7, 4],
            [0, 4, 0,    0, 5, 0,    0, 3, 6],
            [7, 0, 3,    0, 1, 8,    0, 0, 0]

            ]


sudoku = Sudoku(test_board)
sudoku.fill_board()
sudoku.draw_board()
