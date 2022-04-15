from cmu_cs3_graphics import *
from pathandmazefunctions import *



graph = makeGraph(3, 3)
for key in graph:
    print(key, graph[key])


print('bfs of reg graph', BFS((0, 0), (2, 2), graph))


graphWithWall = createHole(graph, (1, 0))
print('bfs of wall graph', BFS((0, 0), (2, 2), graphWithWall))


def onAppStart(app):
    app.margin = 0
    app.rows = 10
    app.cols = 10
    app.playerRow = 0
    app.playerCol = 0
    app.mobRow = 0
    app.mobCol = 0
    app.stepsPerSecond = 1
    app.wall = (4, 4)
    app.graph = makeGraph(app.rows, app.cols)
    app.graph = createHole(app.graph, app.wall)
    app.graph = createWall(app.graph, (0, 0), (1, 0))
    app.map = None

def onStep(app):
    app.map = BFS((app.mobRow, app.mobCol), (app.playerRow, app.playerCol), app.graph)
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
    


#retrives coordinates of cell
def getCellBounds(app, row, col):
    cellWidth = (app.width - 2*app.margin) // app.cols
    cellHeight = (app.height - app.margin - app.margin) // app.rows
    left = app.margin + cellWidth * col
    top = app.margin + cellHeight * row
    return left, top, cellWidth, cellHeight

#draws grid
def drawGrid(app):
    for row in range(app.rows):
        for col in range(app.cols):
            left, top, cellWidth, cellHeight = getCellBounds(app, row, col)
            color = 'black' if app.wall == (row, col) else 'white'
            drawRect(left, top, cellWidth, cellHeight, border = 'black', 
            fill = color, borderWidth = 1)

def redrawAll(app):
    drawGrid(app)
    drawPlayer(app)
    drawMob(app)

runApp(1000, 1000)