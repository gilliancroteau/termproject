from cmu_cs3_graphics import *
from pathandmazefunctions import *
import random


def onAppStart(app):
    app.rows = 20
    app.cols = 20
    template = makeGraph(app.rows, app.cols)
    app.maze = kruskals(template)
    app.margin = 0
    app.playerRow = 0
    app.playerCol = 0
    app.mobRow = 0
    app.mobCol = 0
    app.stepsPerSecond = 3
    app.map = None

def onKeyPress(app, key):
    if key == 'r':
        onAppStart(app)

def getCellBounds(app, row, col):
    cellWidth = (app.width - 2*app.margin) // app.cols
    cellHeight = (app.height - app.margin - app.margin) // app.rows
    left = app.margin + cellWidth * col
    top = app.margin + cellHeight * row
    return left, top, cellWidth, cellHeight


#draws grid in light gray borders
def drawGrid(app):
    for row in range(app.rows):
        for col in range(app.cols):
            left, top, cellWidth, cellHeight = getCellBounds(app, row, col)
            drawRect(left, top, cellWidth, cellHeight, border = 'lightgray', 
            fill = None, borderWidth = 1)

#returns coords of lines along cell border
def cellBorders(app, row, col, drow, dcol):
    left, top, cellWidth, cellHeight = getCellBounds(app, row, col)
    if (drow, dcol) == (-1, 0):
        x1, y1, x2, y2 = left, top, left+cellWidth, top
    elif (drow, dcol) == (1, 0):
        x1, y1, x2, y2 = left, top+cellHeight, left+cellWidth, top+cellHeight
    elif (drow, dcol) == (0, -1):
        x1, y1, x2, y2 = left, top, left, top+cellHeight
    elif (drow, dcol) == (0, 1):
        x1, y1, x2, y2 = left+cellWidth, top, left+cellWidth, top+cellHeight
    return x1, y1, x2, y2

#draws walls according to map
def drawWalls(app):
    for (row, col) in app.maze:
        for drow, dcol in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nrow = row + drow
            ncol = col + dcol
            if nrow < 0 or ncol < 0 or nrow >= app.rows or ncol >= app.cols:
                pass
            else:
                if (nrow, ncol) not in app.maze[(row, col)]:
                    x1, y1, x2, y2 = cellBorders(app, row, col, drow, dcol)
                    drawLine(x1, y1, x2, y2, fill = 'black', lineWidth = 8)


#pathfinding stuff
def onStep(app):
    app.map = BFS((app.mobRow, app.mobCol), (app.playerRow, app.playerCol), app.maze)
    if (app.mobRow, app.mobCol) != (app.playerRow, app.playerCol):
        app.mobRow, app.mobCol = app.map[1]

def drawMob(app):
    left, top, cellWidth, cellHeight = getCellBounds(app, app.mobRow, app.mobCol)
    mobX = left + cellWidth//2
    mobY = top + cellWidth//2
    drawCircle(mobX, mobY, cellWidth/2, fill = 'black')

def drawPlayer(app):
    left, top, cellWidth, cellHeight = getCellBounds(app, app.playerRow, app.playerCol)
    playerX = left + cellWidth//2
    playerY = top + cellWidth//2
    drawCircle(playerX, playerY, cellWidth/2, fill = 'blue')
    
def onMousePress(app, x, y):
    left, top, cellWidth, cellHeight = getCellBounds(app, app.mobRow, app.mobCol)
    app.playerRow = y//cellHeight
    app.playerCol = x//cellWidth

def redrawAll(app):
    drawGrid(app)
    drawWalls(app)
    drawPlayer(app)
    drawMob(app)

runApp(1000, 1000)