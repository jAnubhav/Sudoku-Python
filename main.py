import pygame as pg
from pygame import display, draw, font, mixer, mouse
from random import sample

### ========================================= Particular Sizes ========================================= ###

SCREEN_DIMS = (410, 600)

CELL_SIZE = 38
CELL_GAP = 2

BLOCK_SIZE = CELL_SIZE*3 + CELL_GAP*2
BLOCK_GAP = 3

GRID_SIZE = BLOCK_SIZE*3 + BLOCK_GAP*4
PAD = [(SCREEN_DIMS[0] - GRID_SIZE)/2 + BLOCK_GAP + 30*i for i in range(2)]

### ======================================== Particular Colors ========================================= ###

myColors = {"BLACK": "#000000", "BLUE": "#4A4ADD", "DARK": "#121212",
            "DARK2": "#2A2A2A", "GRAY": "#3A3A3A", "WHITE": "#FFFFFF"}

### ========================================== Grid Creation =========================================== ###

def shuffledList(extra=0):
    return [i*3+j+extra for i in sample(range(3), 3) for j in sample(range(3), 3)]

def gridCreation():
    row, col, num = list(map(lambda x: shuffledList(x//2), range(3)))
    grid = [[num[(3*(r % 3)+r//3+c) % 9] for r in row] for c in col]

    spaces = sample(range(81), 45)
    puzzle = [[' ' if (i*9+j in spaces) else grid[i][j] for j in range(9)] for i in range(9)]

    return grid, puzzle

### ========================================== Cell Creation =========================================== ###

def cellCreation(left, top, bg, text="", width=CELL_SIZE, height=CELL_SIZE):
    draw.rect(screen, bg, pg.Rect(PAD[0] + left, PAD[1] + top, width, height))
    screen.blit(textFont.render(str(text), True, myColors["WHITE"]), (PAD[0] + left + (width - 8)/2, PAD[1] + top + (height - 16)/2))

def gridCells(pos_x, pos_y, bg=myColors["BLUE"]):
    cellCreation((BLOCK_SIZE + BLOCK_GAP)*(pos_x//3) + (CELL_SIZE + CELL_GAP)*(pos_x%3),  (BLOCK_SIZE + BLOCK_GAP)*(pos_y//3) + (CELL_SIZE + CELL_GAP)*(pos_y%3), bg, puzzle[pos_y][pos_x])

def numberCells(index, bg=myColors["BLUE"]):
    cellCreation((CELL_SIZE + BLOCK_GAP)*(index-1)+1, (CELL_SIZE + CELL_GAP)*10+2, bg, index, 30, 34)

### ============================================ Mark Cells ============================================ ###

def markCells(num):
    global cNumber

    numberCells(num)
    if (cNumber != ' '):
        numberCells(cNumber, myColors["GRAY"])
    
    for i in range(9):
        for j in range(9):
            if (puzzle[i][j] == cNumber):
                gridCells(j, i, myColors["GRAY"])
            elif (puzzle[i][j] == num):
                gridCells(j, i)
    cNumber = [num, ' '][cNumber == num]

### ========================================== Board Creation ========================================== ###

def boardCreation():
    cellCreation(-BLOCK_GAP, -BLOCK_GAP, bg=myColors["BLACK"], width=GRID_SIZE, height=GRID_SIZE)
    for i in range(9):
        cellCreation((CELL_SIZE + BLOCK_GAP)*i-1, (CELL_SIZE + CELL_GAP)*10, myColors["BLACK"], width=34)
        numberCells(i+1, myColors["GRAY"])
        for j in range(9):
            if (not(i%3 or j%3)):
                cellCreation((BLOCK_SIZE + BLOCK_GAP)*(j//3), (BLOCK_SIZE + BLOCK_GAP)*(i//3), bg=myColors["DARK"], width=BLOCK_SIZE, height=BLOCK_SIZE)
            gridCells(j, i, myColors["GRAY"])

### ========================================= Main Game Starts ========================================= ###

if __name__ == "__main__":
    grid, puzzle = gridCreation()
    mistakes, cNumber = 0, ' '

    pg.init()

    screen = display.set_mode(SCREEN_DIMS)
    display.set_caption("Sudoku")
    screen.fill(myColors["DARK2"])

    correctSound = mixer.Sound("./assets/correct.mp3")
    incorrectSound = mixer.Sound("./assets/incorrect.mp3")
    gameoverSound = mixer.Sound("./assets/gameover.mp3")
    successSound = mixer.Sound("./assets/success.mp3")

    textFont = font.SysFont(None, 26)
    extraFont = font.SysFont(None, 21)

    boardCreation()

    status = True
    while (status):
        ticks = pg.time.get_ticks()//1000
        mm, ss = ticks//60, ticks%60
        
        draw.rect(screen, myColors["DARK2"], pg.Rect(PAD[0] - BLOCK_GAP, PAD[1] - 24, 100, 21))
        screen.blit(extraFont.render(f"Time  {mm:02} : {ss:02}", True, myColors["WHITE"]), (PAD[0], PAD[1] - 21))

        draw.rect(screen, myColors["DARK2"], pg.Rect(GRID_SIZE - CELL_SIZE*2, PAD[1] - 24, 100, 21))
        screen.blit(extraFont.render(f"Mistakes : {mistakes}/3", True, myColors["WHITE"]), (GRID_SIZE - CELL_SIZE*2, PAD[1] - 21))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                status = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mx, my = [int(cord - PAD[index])//(CELL_SIZE + CELL_GAP) for index, cord in enumerate(mouse.get_pos())]
                if (my == 10):
                    markCells(mx+1)
                elif(my in range(9) and cNumber != ' ' and puzzle[my][mx] == ' '):
                    if (grid[my][mx] == cNumber):
                        puzzle[my][mx] = cNumber
                        gridCells(mx, my)
                        correctSound.play()
                    else:
                        mistakes += 1
                        if (mistakes == 3):
                            gameoverSound.play()
                            pg.time.wait(1200)
                            status = False
                        else:
                            incorrectSound.play()

        display.update()

        if (puzzle == grid):
            successSound.play()
            pg.time.wait(1400)
            status = False

    pg.quit()
