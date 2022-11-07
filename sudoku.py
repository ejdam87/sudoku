from typing import List, Tuple

Board = List[List[int]]
Square = Tuple[int, int]


class Sudoku:
    def __init__(self, board: Board) -> None:
        self.board = board
        self.squares = [(i, j) for i in range(3) for j in range(3)]

    def solve(self) -> bool:
        """
        Finds ONE solution of sudoku (there might be more)
        """
        return self.place_number(self.board, self.squares, 1)

    def place_number(self,
                     board: Board,
                     squares_left: List[Square],
                     num: int) -> bool:

        if squares_left == []:

            ## Filled all squares with all numbers
            if num == 9:
                return True

            return self.place_number(board, self.squares, num + 1)

        possible = self.get_possible(board, squares_left[0], num)

        if possible == []:
            return False

        for x, y in possible:

            prev = board[x][y]
            board[x][y] = num

            if self.place_number(board, squares_left[1:], num):
                return True

            board[x][y] = prev

        return False

    def check_squares(self, board: Board, num: int) -> bool:

        present = False

        for sx, sy in self.squares:
            for i in range(3 * sx, 3 * sx + 3):
                for j in range(3 * sy, 3 * sy + 3):

                    if num == board[i][j]:
                        present = True

            if not present:
                return False

            present = False

        return True

    def get_possible(self, board: Board, square: Square, num: int) -> List[Tuple[int, int]]:

        possible = []
        sx, sy = square
        for row in range(3 * sx, 3 * sx + 3):
            for column in range(3 * sy, 3 * sy + 3):

                ## Already present in square
                if board[row][column] == num:
                    return [(row, column)]

                if board[row][column] != 0:
                    continue

                if self.is_in_row(board, num, row):
                    continue

                if not self.is_in_column(board, num, column):
                    possible.append((row, column))

        return possible

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

                sep = "│" if j % 3 == 2 else " "
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
        return str(val) if val != 0 else " "


test_board_2 = [

            [1, 0, 0,    0, 0, 0,    0, 0, 0],
            [0, 0, 0,    1, 0, 0,    0, 0, 0],
            [0, 0, 0,    0, 0, 0,    1, 0, 0],

            [0, 1, 0,    0, 0, 0,    0, 0, 0],
            [0, 0, 0,    0, 1, 0,    0, 0, 0],
            [0, 0, 0,    0, 0, 0,    0, 1, 0],

            [0, 0, 1,    0, 0, 0,    0, 0, 0],
            [0, 0, 0,    0, 0, 1,    0, 0, 0],
            [0, 0, 0,    0, 0, 0,    0, 0, 1]

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
sudoku.solve()
sudoku.draw_board()
