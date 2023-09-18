import pygame
import numpy as np
pygame.init()

"""
File: sudoku.py
Author: Milt Rue
Purpose: Allows the user to play sudoku or to see the recursive backtracking solution visualized
"""
"""
Escape or close window to exit
Hold shift to annotate
Enter to start computer solve
"""

# Setting Variables
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
sideLength = 55
boxMargin = 3
edgeMargin = 6
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
#BACKGROUND_COLOR = (000, 100, 200)
BACKGROUND_COLOR = (250, 246, 220)
HIGHLIGHT_COLOR = (255, 255, 150)
SOLVE_COLOR = (0,220,120)
NUMBER_COLOR = (0, 70, 140)
WRONG_COLOR = (255,120,120)
maxSize = (sideLength+boxMargin)*9 + boxMargin + edgeMargin * 4
center = (SCREEN_WIDTH - maxSize) // 2
font = pygame.font.SysFont("arial",48)
smallFont = pygame.font.SysFont("arial",20,True)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku")

# Sudoku Boards have a 2d array representing the board using square objects and a zero counter


class SudokuBoard:
    def __init__(self, b):
        """
        Takes in a 2d array representing the board and assigns it to _board and counts the number of zeros
        Param: "b" - a 2d array representation of the sudoku board
        """
        self._board = np.zeros((9, 9), dtype=int)
        self._correctBoard = np.zeros((9, 9), dtype=int)
        self._GUIBoard = np.empty((9, 9), dtype=Square)
        self._numZeros = 81
        self._minMax = 0
        self._selectedSquare = [10,10]
        self._speed = 20
        for row in range(9):
            for col in range(9):
                self._board[row][col] = b[row][col]
                self._correctBoard[row][col] = b[row][col]
                self._GUIBoard[row][col] = Square(b[row][col], 0, 0, 0, 0)
                if b[row][col] != 0:
                    self._GUIBoard[row][col].lock()
                    self._numZeros -= 1
        self.setPositions()
        self.getCorrectBoard(0,0)
        self.setCorrectGUI()

    def setPositions(self):
        """
        Uses the variable values to set the start and end rows and cols for each square in GUI Board
        """
        for row in range(9):
            for col in range(9):
                square = self._GUIBoard[row][col]
                r1 = (sideLength+boxMargin)*col + boxMargin + \
                    edgeMargin * (1 + (col//3)) + center
                c1 = (sideLength+boxMargin)*row + \
                    boxMargin + edgeMargin * (4 + (row//3))
                r2 = r1 + sideLength
                c2 = c1 + sideLength
                square.setPositions(r1, c1, r2, c2)
        self._minMax = (self._GUIBoard[0][0].getPositions()[0], self._GUIBoard[0][0].getPositions()[1],
                        self._GUIBoard[8][8].getPositions()[2], self._GUIBoard[8][8].getPositions()[3])

    def getCorrectBoard(self, row, col):
        """
        Uses recursive backtracking to solve the board before user input, and stores this solution
        """
        if row == 9: return True
        if self._correctBoard[row][col] != 0:
            if col == 8:
                return self.getCorrectBoard(row+1, 0)
            else:
                return self.getCorrectBoard(row, col+1)
        else:
            for num in range(1, 10):
                if self.validSquareCB(num, row, col):
                    self._correctBoard[row][col] = num
                    result = False
                    if col == 8:
                        result = self.getCorrectBoard(row+1, 0)
                    else:
                        result = self.getCorrectBoard(row, col+1)
                    if result == True:
                        return True
                    self._correctBoard[row][col] = 0

    def setCorrectGUI(self):
        for row in range(9):
            for col in range(9):
                self._GUIBoard[row][col].setCorrectNum(self._correctBoard[row][col])

    def mouseClicked(self, pos):
        col = (pos[0] - boxMargin - 2 * edgeMargin - center) // (sideLength+boxMargin)
        row = (pos[1] - boxMargin - 5 * edgeMargin) // (sideLength+boxMargin)

        if col == 9 or col == 8 or col == 7:
            col = (pos[0] - boxMargin - 3 * edgeMargin - center) // (sideLength+boxMargin)

        if row == 9 or row == 8 or row == 7:
            row = (pos[1] - boxMargin - 6 * edgeMargin) // (sideLength+boxMargin)

        if col == -1 or col == 0 or col == 1:
            col = (pos[0] - boxMargin - edgeMargin - center) // (sideLength+boxMargin)

        if row == -1 or row == 0 or row == 1:
            row = (pos[1] - boxMargin - 4 * edgeMargin) // (sideLength+boxMargin)
            
        self._selectedSquare = [row,col]


    def zeros(self):
        return self._numZeros

    def board(self):
        return self._board

    def GUI(self):
        return self._GUIBoard

    def selectedSquare(self):
        return self._selectedSquare

    def get(self, row, col):
        return self._board[row][col]

    def set(self, num, row, col):
        """
        Sets the given square to num
        """
        if self._board[row][col] == 0 and num != 0:
            self._numZeros -= 1
        elif self._board[row][col] != 0 and num == 0:
            self._numZeros += 1
        self._board[row][col] = num
        self._GUIBoard[row][col].setNumber(num)

    def validSquare(self, num, row, col):
        """
        Returns true if the num can be placed in the square according to Sudoku rules
        """
        result = True
        removed = False
        
        # Check if num is already there
        if num == self._board[row][col]:
            self._board[row][col] = 0
            removed = True

        # Row check
        if num in self._board[row]:
            result = False

        # Col check
        for r in self._board:
            if num == r[col]:
                result = False

        # Box check
        for r in range(3*(row//3), 3*(row//3)+3):
            for c in range(3*(col//3), 3*(col//3)+3):
                if num == self._board[r][c]:
                    result = False

        if removed:
            self._board[row][col] = num

        return result

    def validSquareCB(self, num, row, col):
        """
        Returns true if the num can be placed in the square according to Sudoku rules
        """
        result = True
        removed = False
        
        # Check if num is already there
        if num == self._correctBoard[row][col]:
            self._correctBoard[row][col] = 0
            removed = True

        # Row check
        if num in self._correctBoard[row]:
            result = False

        # Col check
        for r in self._correctBoard:
            if num == r[col]:
                result = False

        # Box check
        for r in range(3*(row//3), 3*(row//3)+3):
            for c in range(3*(col//3), 3*(col//3)+3):
                if num == self._correctBoard[r][c]:
                    result = False

        if removed:
            self._correctBoard[row][col] = num

        return result

    def solve(self):
        for row in range(9):
            for col in range(9):
                square = self._GUIBoard[row][col]
                if square._correctNum != square._num:
                    self.set(0,row,col)
                    pygame.draw.rect(screen, WHITE, square.getRect())
                if square.annotated():
                    square.clearAnnotate()
                    
        solved = self.solveBoard(0,0)
        
    
    def solveBoard(self,row,col):
        """
        Shows the recusive backtracking solving the board
        """
        if self._numZeros == 0:
            return True
        square = self._GUIBoard[row][col]

        pygame.event.get()
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE] == True:
            self._speed = 0
        elif key[pygame.K_SPACE] == True:
            self._speed = 100
        elif key[pygame.K_RETURN] == True:
            self._speed = 20

        if square.locked():
            if col == 8:
                return self.solveBoard(row+1, 0)
            else:
                return self.solveBoard(row, col+1)
                
        elif square.getNum() != 0:
            if col == 8:
                return self.solveBoard(row+1, 0)
            else:
                return self.solveBoard(row, col+1)

        else:
            for num in range(1, 10):
                if self.validSquare(num, row, col):
                    self.set(num, row, col)

                    pygame.draw.rect(screen, SOLVE_COLOR, square.getRect())
                    text = font.render(" " + str(square.getNum()),False,NUMBER_COLOR,SOLVE_COLOR)
                    screen.blit(text,square.getRect())
                    pygame.display.update()
                    pygame.time.wait(self._speed)

                    result = False
                    if col == 8:
                        result = self.solveBoard(row+1, 0)
                    else:
                        result = self.solveBoard(row, col+1)
                    if result == True:
                        return True
                    self.set(0, row, col)
                    pygame.draw.rect(screen, SOLVE_COLOR, square.getRect())
                    pygame.display.update()
                    pygame.time.wait(self._speed)

    """
    def solveBoard(self, row, col):
        ""
        Uses recursive backtracking to solve the board
        ""
        if self._numZeros == 0:
            return True
        elif self._board[row][col] != 0:
            if col == 8:
                return self.solveBoard(row+1, 0)
            else:
                return self.solveBoard(row, col+1)
        else:
            for num in range(1, 10):
                if self.validSquare(num, row, col):
                    self.set(num, row, col)
                    result = False
                    if col == 8:
                        result = self.solveBoard(row+1, 0)
                    else:
                        result = self.solveBoard(row, col+1)
                    if result == True:
                        return True
                    self.set(0, row, col)"""

    def checkBoard(self):
        """
        Makes sure all numbers in the board are in valid squares
        """
        for row in range(9):
            for col in range(9):
                num = self._board[row][col]
                if num != 0:
                    if self.validSquare(num,row,col) == False:
                        return False
        return True

    def __str__(self):
        result = ""
        for r in self._board:
            for i in r:
                result += str(i) + ","
            result = result[0:-1]
            result += "\n"
        """
        result += "\n"*2
        for r in self._GUIBoard:
            for i in r:
                result += str(i) + ","
            result = result[0:-1]
            result += "\n"
        """
        return result

# A square has a number, empty checker, and information for the GUI


class Square:
    """
        Takes in a num for the number in the square (0 if empty), 
        and the start and end rows and cols for the GUI
        """

    def __init__(self, num, r1, c1, r2, c2):
        self._num = num
        self._isEmpty = (num == 0)
        self._selected = False
        self._locked = False
        self._annotate = set()
        self._positions = (r1, c1, r2, c2)
        self._correctNum = 0

    def setNumber(self, num):
        if num == 0:
            self.removeAnnotate(self._num)
        self._num = num
        self._isEmpty = (num == 0)

    def setCorrectNum(self,num):
        self._correctNum = num
    def getCorrectNum(self):
        return self._correctNum

    def getNum(self):
        return self._num

    def lock(self):
        self._locked = True
    def locked(self):
        return self._locked
    
    def addAnnotate(self,a):
        self._annotate.add(a)
    def removeAnnotate(self,a):
        if a in self._annotate:
            self._annotate.remove(a)
    def getAnnotate(self):
        return self._annotate
    def clearAnnotate(self):
        self._annotate = set()
    def annotated(self):
        return len(self._annotate) != 0

    def setPositions(self, r1, c1, r2, c2):
        self._positions = (r1, c1, r2, c2)

    def getPositions(self):
        return self._positions

    def getRect(self):
        return (self._positions[0], self._positions[1], sideLength, sideLength)

    def setSelected(self, sel):
        self._selected = sel

    def selected(self):
        return self._selected

    def __str__(self):
        # return "(" + str(self._num)+", " + str(self._positions) + ")"
        return str(self._num)


def runGame(sudokuBoard):
    """
    Opens the GUI and runs the game
    """
    board = SudokuBoard(sudokuBoard.board())
    run = True
    while run:
        # Checks for events occuring
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                board.mouseClicked(pos)

        # Checks for keys being pressed
        key = pygame.key.get_pressed()
        annotate = False
        keyNum = 10

        if key[pygame.K_ESCAPE] == True:
            run = False
        elif key[pygame.K_RETURN] == True:
            board.solve()
        
        # Numbers
        if key[pygame.K_1] == True:
            keyNum = 1
        elif key[pygame.K_2] == True:
            keyNum = 2
        elif key[pygame.K_3] == True:
            keyNum = 3
        elif key[pygame.K_4] == True:
            keyNum = 4
        elif key[pygame.K_5] == True:
            keyNum = 5
        elif key[pygame.K_6] == True:
            keyNum = 6
        elif key[pygame.K_7] == True:
            keyNum = 7
        elif key[pygame.K_8] == True:
            keyNum = 8
        elif key[pygame.K_9] == True:
            keyNum = 9
        elif key[pygame.K_0] == True:
            keyNum = 0
        elif key[pygame.K_BACKSPACE] == True:
            keyNum = 0
        

        if key[pygame.K_RSHIFT] == True or key[pygame.K_LSHIFT] == True:
            annotate = True

        

        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, BLACK, (center, 3*edgeMargin, maxSize, maxSize))
        for row in range(9):
            for col in range(9):
                square = board.GUI()[row][col]

                if square.locked():
                    pygame.draw.rect(screen, WHITE, square.getRect())
                    num = font.render(" " + str(square.getNum()),False,BLACK,WHITE)
                    screen.blit(num,square.getRect())
                else:
                    if board.selectedSquare()[0] == row and board.selectedSquare()[1] == col:
                        color = HIGHLIGHT_COLOR
                        if keyNum != 10 and not annotate:
                            board.set(keyNum,row,col)
                        elif keyNum != 10 and annotate:
                            if keyNum == 0:
                                square.clearAnnotate()
                            else:
                                square.addAnnotate(keyNum)
                    else:
                        color = WHITE
                    
                    if square.getNum() != square.getCorrectNum() and square.getNum() != 0:
                        color = WRONG_COLOR
                    
                    pygame.draw.rect(screen, color, square.getRect())
                    if square.getNum() != 0:
                        num = font.render(" " + str(square.getNum()),False,NUMBER_COLOR,color)
                        screen.blit(num,square.getRect())
                    else:
                        if square.annotated(): 
                            setStr = str(square.getAnnotate())[1:-1]
                            setStr = setStr.replace(", ", "")
                            num = smallFont.render(setStr,False,NUMBER_COLOR,color)
                            screen.blit(num,square.getRect())
                        

        pygame.display.update()


# Makes a board and runs the solving algorithm

def main():
    board = [
        [5, 9, 7, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 3, 9, 0, 0],
        [3, 0, 0, 0, 0, 4, 5, 1, 0],
        [0, 0, 0, 0, 9, 0, 8, 2, 0],
        [0, 0, 0, 3, 0, 7, 0, 0, 0],
        [0, 1, 6, 0, 5, 0, 0, 0, 0],
        [0, 2, 5, 6, 0, 0, 0, 0, 4],
        [0, 0, 4, 1, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 6, 5, 8]
    ]

    zerosBoard = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    board2 = [
        [1, 0, 8, 3, 0, 2, 0, 7, 0],
        [0, 0, 0, 0, 0, 6, 5, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 7, 0, 2, 0, 0, 0, 0, 0],
        [4, 0, 2, 0, 0, 3, 0, 0, 6],
        [0, 9, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 7],
        [9, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 0, 4, 8, 0, 0, 0, 1, 0]
    ]
    b1 = SudokuBoard(board2)
    runGame(b1)

main()
