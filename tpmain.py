from cmu_cs3_graphics import *
from objects import *
from rooms import *
from pathandmazefunctions import *


#defines start stuff
def onAppStart(app):
    app.paused = False
    app.playerX = 600#app.width//2
    app.playerY = 400#app.height//2
    app.speed = 10
    app.squares = ['red square.png', 'blue square.png']
    app.spriteTimer = 0
    app.spriteI = 0
    app.stepsPerSecond = 30
    app.sandTimer = 0
    app.direction = None
    app.rooms = createRooms()
    app.roomMap = roomMap(app.rooms)
    app.currentMapRowCol = (2, 2)
    app.currentRoom = app.rooms[0]
    app.currentRoomCoords = app.currentRoom.dimensions()  #[leftX, rightX, topY, bottomY]
    app.currentRoomDoors = ['left', 'right', 'top', 'bottom']
    app.timer = 120
    app.goldScore = 0
    app.goldPerGold = 10
    app.spriteSize = 25
    app.goldCoords = app.currentRoom.gold
    app.goldR = 20
    app.titleScreen = True
    app.inDungeon = False
    app.exited = False
    app.gameOver = False
    app.enterRect = (app.width//2-50, app.height*0.75-25, 100, 50) #left, top, width, height
    app.startHealth = 20
    app.health = app.startHealth
    app.swordStrength = 5
    app.swordReach = 70
    app.mummies = app.currentRoom.mummies
    app.inventorySand = 0
    app.sandInRoom = app.currentRoom.sand
    app.hourglass = (700, 400, 100, 150) #left, top, width, height
    app.portal = (750, 275, 300, 50) #centerX, centerY, width, height
    app.leftDoor = (500, 450, 50, 100)#left, top, width, height
    app.rightDoor = (950, 450, 50, 100)#left, top, width, height
    app.topDoor = (700, 250, 100, 30)#left, top, width, height
    app.bottomDoor = (700, 700, 100, 50)#left, top, width, height

#distance formula
def distance(x1, y1, x2, y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5

#controls timer, checks for game over, checks for mob attacks, moves mummies
def onStep(app):
    if not app.paused:
        if app.inDungeon:
            for mummy in app.mummies:
                if mummy.alive:
                    playerNode = rowAndCol(app, app.playerX, app.playerY)
                    mummyNode = rowAndCol(app, mummy.x, mummy.y)
                    mummy.pathfind(playerNode, mummyNode, app.currentRoom.graph)
            app.sandTimer += 1
            if app.sandTimer % app.stepsPerSecond == 0:
                app.timer -= 1
                for mummy in app.mummies:
                    if mummy.alive:
                        if distance(app.playerX, app.playerY, mummy.x, mummy.y) <= mummy.reach:
                            app.health -= mummy.damage
            if app.timer <= 0 or app.health <= 0:
                app.inDungeon = False
                app.gameOver = True

#checks for exiting door and switches room if so
def switchRoom(app):
    drow, dcol = None, None
    for door in app.currentRoomDoors:
        if door == 'left':
            if xyInside(app, app.playerX - app.spriteSize, app.playerY, 
            app.leftDoor[0], app.leftDoor[0] + app.leftDoor[2], 
            app.leftDoor[1], app.leftDoor[1] + app.leftDoor[1]):
                drow, dcol = 0, -1
        elif door == 'right':
            if xyInside(app, app.playerX + app.spriteSize, app.playerY, 
            app.rightDoor[0], app.rightDoor[0] + app.rightDoor[2], 
            app.rightDoor[1], app.rightDoor[1] + app.rightDoor[1]):
                drow, dcol = 0, 1
        elif door == 'top':
            if xyInside(app, app.playerX, app.playerY - app.spriteSize, 
            app.topDoor[0], app.topDoor[0] + app.topDoor[2], 
            app.topDoor[1], app.topDoor[1] + app.topDoor[3]):
                drow, dcol = -1, 0
        elif door == 'bottom':
            if xyInside(app, app.playerX, app.playerY + app.spriteSize, 
            app.bottomDoor[0], app.bottomDoor[0] + app.bottomDoor[2], 
            app.bottomDoor[1], app.bottomDoor[1] + app.bottomDoor[1]):
                drow, dcol = 1, 0
    if drow != None:
        newRoom = isRoom(app, drow, dcol)
        if newRoom != None and newRoom != False:
            app.currentRoom = newRoom
            app.mummies = app.currentRoom.mummies
            app.sandInRoom = app.currentRoom.sand
            app.goldCoords = app.currentRoom.gold
            app.currentMapRowCol = (app.currentMapRowCol[0] + drow, app.currentMapRowCol[1] + dcol)
            app.playerX += -dcol * 300
            app.playerY += -drow * 300

#controls image cycling for sprites, checks for gold collision and sand collision, checks for exit/doors
def doStep(app):
    app.spriteTimer += 1
    if app.spriteTimer%10 == 0:
        app.spriteI +=1
    if app.goldCoords != []:
        i = 0
        while i < len(app.goldCoords):
            coords = app.goldCoords[i]
            if distance(app.playerX, app.playerY, coords[0], coords[1]) <= app.spriteSize:
                app.goldScore += app.goldPerGold
                app.goldCoords.remove(coords)
            else:
                i += 1
    for sand in app.sandInRoom:
        if sand.onGround:
            if distance(app.playerX, app.playerY, sand.x, sand.y) <= sand.edgeSize/2 + app.spriteSize:
                app.inventorySand += 1
                sand.onGround = False
    if app.currentRoom == app.rooms[0]:
        if xyInside(app, app.playerX, app.playerY - app.spriteSize,
                app.portal[0]-app.portal[2]/2, app.portal[0] + app.portal[2]/2,
                    app.portal[1]-app.portal[3]/2, app.portal[1] + app.portal[3]/2):
            app.inDungeon = False
            app.exited = True
    switchRoom(app)

#moves sprite and checks for room bounds
def doMove(app, dx, dy):
    prevtopRowCol = rowAndCol(app, app.playerX, app.playerY - app.spriteSize)
    prevbottomRowCol = rowAndCol(app, app.playerX, app.playerY + app.spriteSize)
    prevrightRowCol = rowAndCol(app, app.playerX + app.spriteSize, app.playerY)
    prevleftRowCol = rowAndCol(app, app.playerX - app.spriteSize, app.playerY)
    prevRowCols = [prevtopRowCol, prevbottomRowCol, prevrightRowCol, prevleftRowCol]
    app.playerX += app.speed * dx
    app.playerY += app.speed * dy
    if (app.playerY-app.spriteSize < app.currentRoomCoords[2] or 
        app.playerY+app.spriteSize > app.currentRoomCoords[3]
        or app.playerX-app.spriteSize < app.currentRoomCoords[0] 
        or app.playerX+app.spriteSize > app.currentRoomCoords[1]):
        app.playerX -= app.speed * dx #within bounds of room
        app.playerY -= app.speed * dy
    topRowCol = rowAndCol(app, app.playerX, app.playerY - app.spriteSize)
    bottomRowCol = rowAndCol(app, app.playerX, app.playerY + app.spriteSize)
    rightRowCol = rowAndCol(app, app.playerX + app.spriteSize, app.playerY)
    leftRowCol = rowAndCol(app, app.playerX - app.spriteSize, app.playerY)
    newRowCols = [topRowCol, bottomRowCol, rightRowCol, leftRowCol]
    for i in range(len(newRowCols)):
        prevRowCol = prevRowCols[i]
        newRowCol = newRowCols[i]
        if prevRowCol != newRowCol:
            if newRowCol not in app.currentRoom.graph[prevRowCol]:
                app.playerX -= app.speed * dx #cannot move thru walls/holes in graph
                app.playerY -= app.speed * dy

#checks if there is a room there in the map and returns room if there is one
def isRoom(app, drow, dcol):
    newRow = app.currentMapRowCol[0] + drow
    newCol = app.currentMapRowCol[1] + dcol
    if newRow < 0 or newCol < 0 or newRow >4 or newCol > 4:
        return False
    nextRoom = app.roomMap[newRow][newCol]
    if nextRoom != None:
        return nextRoom
    return False

#gives current(row, col) location in room
def rowAndCol(app, x, y):
    leftMargin = app.currentRoomCoords[0]
    topMargin = app.currentRoomCoords[2]
    row = (y - topMargin) // (app.currentRoom.height/app.currentRoom.rows)
    col = (x - leftMargin) // (app.currentRoom.width/app.currentRoom.cols)
    return (row, col)

#mouse clicks
def onMousePress(app, x, y):
    if app.titleScreen:
        if xyInside(app, x, y, app.enterRect[0], app.enterRect[0] + app.enterRect[2],
                     app.enterRect[1], app.enterRect[1] + app.enterRect[3]):
            app.titleScreen = False
            app.inDungeon = True
    if not app.paused:
        if app.inDungeon:
            for mummy in app.mummies:
                if distance(app.playerX, app.playerY, mummy.x, mummy.y) <= app.swordReach:
                    mummy.takeDamage(app.swordStrength)
            if xyInside(app, x, y, app.hourglass[0], app.hourglass[0] + app.hourglass[2],
                     app.hourglass[1], app.hourglass[1] + app.hourglass[3]):
                if app.inventorySand > 0:
                    app.timer += Sand.time
                    app.inventorySand -= 1

#moves sprite
def onKeyHold(app, keys):
    if not app.paused:
        if keys == ['s']:
            doMove(app, 0, 1)
            app.direction = 'down'
        elif keys == ['w']:
            doMove(app, 0, -1)
            app.direction = 'up'
        elif keys == ['a']:
            doMove(app, -1, 0)
            app.direction = 'left'
        elif keys == ['d']:
            doMove(app, 1, 0)
            app.direction = 'right'
        doStep(app)

#pause and restart
def onKeyPress(app, key):
    if key == 'p':
        app.paused = not app.paused
    elif key == 'r':
        onAppStart(app)

#draws the sprite with the walking animation (right now that is only flashing red and blue when moving right)
def drawSprite(app):
    if app.direction == 'right':
        spriteList = app.squares
    else:
        spriteList = ['red square.png', 'red square.png']
    i = app.spriteI%2
    drawImage(spriteList[i], app.playerX, app.playerY, align = 'center')

#cell bounds
def getCellBounds(app, row, col):
    leftMargin = app.currentRoomCoords[0]
    topMargin = app.currentRoomCoords[2]
    cellWidth = (app.width - 2*leftMargin) // app.currentRoom.cols
    cellHeight = (app.height - 2*topMargin) // app.currentRoom.rows
    left = leftMargin + cellWidth * col
    top = topMargin + cellHeight * row
    return left, top, cellWidth, cellHeight

#returns True if x and y are inside these bounds
def xyInside(app, x, y, leftX, rightX, topY, bottomY):
    if leftX <= x <= rightX and topY <= y <= bottomY:
        return True
    return False

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
    for (row, col) in app.currentRoom.graph:
        for drow, dcol in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nrow = row + drow
            ncol = col + dcol
            if nrow < 0 or ncol < 0 or nrow >= app.currentRoom.rows or ncol >= app.currentRoom.cols:
                pass
            else:
                if (nrow, ncol) not in app.currentRoom.graph[(row, col)]:
                    x1, y1, x2, y2 = cellBorders(app, row, col, drow, dcol)
                    drawLine(x1, y1, x2, y2, fill = 'black', lineWidth = 8)

#draws doors
def drawDoors(app):
    for door in app.currentRoomDoors:
        if door == 'left':
            drow, dcol = 0, -1
            if isRoom(app, drow, dcol):
                drawRect(app.leftDoor[0], app.leftDoor[1], 
                app.leftDoor[2], app.leftDoor[3], fill = 'brown')
        elif door == 'right':
            drow, dcol = 0, 1
            if isRoom(app, drow, dcol):
                drawRect(app.rightDoor[0], app.rightDoor[1], 
                app.rightDoor[2], app.rightDoor[3], fill = 'brown')
        elif door == 'top':
            drow, dcol = -1, 0
            if isRoom(app, drow, dcol):
                drawRect(app.topDoor[0], app.topDoor[1], 
                app.topDoor[2], app.topDoor[3], fill = 'brown')
        elif door == 'bottom':
            drow, dcol = 1, 0
            if isRoom(app, drow, dcol):
                drawRect(app.bottomDoor[0], app.bottomDoor[1], 
                app.bottomDoor[2], app.bottomDoor[3], fill = 'brown')

#draws the room as a rectangle (will eventually be from an image)
def drawRoom(app):
    room = app.currentRoom
    for row in range(room.rows):
        for col in range(room.cols):
            color = 'orange' if (row, col) in room.graph else 'yellow'
            left, top, cellWidth, cellHeight = getCellBounds(app, row, col)
            drawRect(left, top, cellWidth, cellHeight, border = 'lightgray', 
            fill = color, borderWidth = 1)

#draws the countdown timer
def drawTimer(app):
    minutes = str(app.timer // 60)
    seconds = str(app.timer - int(minutes) * 60)
    if int(seconds) <10:
        seconds = '0' + seconds
    time = minutes+':'+seconds
    drawRect(0, 0, 100, 50, fill = 'blue')
    drawLabel(time, 50, 25, fill = 'white', size = 14)

#draws pile of gold and sand
def drawGoldandSand(app):
    for coords in app.goldCoords:
        drawCircle(coords[0], coords[1], app.goldR, fill = 'gold')
    for sand in app.sandInRoom:
        if sand.onGround:
            drawRect(sand.x, sand.y, sand.edgeSize, sand.edgeSize, fill = sand.color, align = 'center')

#draws mummies
def drawMummies(app):
    for mummy in app.mummies:
        if mummy.alive:
            drawCircle(mummy.x, mummy.y, mummy.r, fill = mummy.color, border = 'black')

#draws score
def drawScore(app):
    drawRect(1400, 0, 100, 50, fill = 'blue')
    drawLabel(app.goldScore, 1450, 25, fill = 'white', size = 14)

#draws amount of sand in inventory
def drawSandInventory(app):
    drawRect(1400, 60, 100, 50, fill = 'blue')
    drawLabel(f'Sand: {app.inventorySand}', 1450, 85, fill = 'white', size = 14)

#draws health bar
def drawHealth(app):
    percentHealth = app.health/app.startHealth
    barWidth = 100
    healthWidth = barWidth*percentHealth + 1
    #print(percentHealth, barWidth, healthWidth)
    drawRect(app.width//2-barWidth//2, 0, barWidth, 20, fill = 'red')
    drawRect(app.width//2-barWidth//2, 0, healthWidth, 20, fill = 'green')

#draws exit portal
def drawPortal(app):
    if app.currentRoom == app.rooms[0]:
        drawRect(app.portal[0], app.portal[1], app.portal[2], app.portal[3], 
        fill = 'purple', borderWidth = 10, border = 'black', align = 'center')

#draws title screen (eventually from image)
def drawTitleScreen(app):
    drawLabel('Sands of Time', app.width/2, app.height/2, size = 30, bold = True, fill = 'white')
    drawRect(app.enterRect[0], app.enterRect[1], app.enterRect[2], app.enterRect[3], 
            fill = None, border = 'white')
    drawLabel('Enter', app.enterRect[0]+app.enterRect[2]//2, 
            app.enterRect[1]+app.enterRect[3]//2, fill = 'white')

#active while playing game
def drawDungeon(app):
    drawRoom(app)
    drawDoors(app)
    drawSprite(app)
    drawTimer(app)
    drawGoldandSand(app)
    drawScore(app)
    drawMummies(app)
    drawHealth(app)
    drawSandInventory(app)
    drawPortal(app)
    drawWalls(app)

#checks if game is not over, then draws everything
def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = 'black')
    if app.titleScreen:
        drawTitleScreen(app)
    elif app.inDungeon:
        drawDungeon(app)
    elif app.gameOver:
        drawLabel('you died', app.width//2, app.height//2, fill = 'white', size = 20)
    elif app.exited:
        #maybe add funn messages depending on time left on timer
        #ex: only 10s left, say you barely made it out with your life
        drawLabel(f'You won {app.goldScore} gold! Congrats', app.width//2, app.height//2, fill = 'white', size = 20)

#run app (these are the game dimensions I am testing on, may eventually change)
runApp(1500, 1000)


'''
make mummies flash red briefly when taking damage
'''

'''
pathfinding: mobs will pathfind to player
have to pathfind in open rooms with occasional walls/features
or in more maze-like rooms
pathfinding goals: quickest route aka shortest
may use BFS for shortest path, but this is maybe only for graphs?
so may use DFS
 but could represent room as invisable grid, which translates to graph, 
       and walls break edges in graph, so then bfs return squares of grid to visit on way to player
'''

'''
next plans:
titlescreen/escape mode
hardcode a map and make it so you can move thru it
add sand to timer function
add mobs class/drawing/etc
add attacks for player to fight mobs and healthbar
pathfinding (lots of complexoty!)
add rooms with puzzles for extra gold- word unscrable, small drag and drop puzzle, etc, could be among us like tasks
add rooms with mazes and make sure mobs can still pathfind
add keys/vaults for more gold
randomly generate dungeons
pixel sprites/rooms
add extras- loot items like better swords, health potions, etc
'''

