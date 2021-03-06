#helper files
from objects import *
from rooms import *
from pathandmazefunctions import *
from filesystem import *
#modules
from cmu_cs3_graphics import *
from PIL import Image

#game settings for reset
def gameSettings(app):
    app.timer = 30 #start time in seconds
    app.paused = False
    app.playerX = app.width//2
    app.playerY = 350
    app.spriteTimer = 0
    app.spriteI = 0
    app.sandTimer = 0
    app.direction = 'down'
    app.rooms = createRooms()
    app.roomMap = roomMap(app.rooms)
    app.currentMapRowCol = (2, 2)
    app.currentRoom = app.rooms[0]
    app.currentRoomCoords = app.currentRoom.dimensions()  #[leftX, rightX, topY, bottomY]
    app.goldScore = 0
    app.goldCoords = app.currentRoom.gold
    app.titleScreen = True
    app.helpScreen = False
    app.inDungeon = False
    app.exited = False
    app.gameOver = False
    app.startHealth = 20
    app.health = app.startHealth
    app.mummies = app.currentRoom.mummies
    app.inventorySand = 0
    app.sandInRoom = app.currentRoom.sand
    app.leftDoor = (app.currentRoomCoords[0], app.currentRoomCoords[3] - (app.currentRoomCoords[3] - app.currentRoomCoords[2])/2 - 50, 30, 100)#left, top, width, height
    app.rightDoor = (app.currentRoomCoords[1]-30, app.currentRoomCoords[3] - (app.currentRoomCoords[3] - app.currentRoomCoords[2])/2 - 50, 30, 100)#left, top, width, height
    app.topDoor = (app.currentRoomCoords[0] + (app.currentRoomCoords[1]-app.currentRoomCoords[0])/2 - 50, app.currentRoomCoords[2], 100, 30)#left, top, width, height
    app.bottomDoor = (app.currentRoomCoords[0] + (app.currentRoomCoords[1]-app.currentRoomCoords[0])/2 - 50, app.currentRoomCoords[3]-30, 100, 30)#left, top, width, height

#defines start settings
#all images drawn by me using pixilart.com
def onAppStart(app):
    gameSettings(app)
    app.speed = 10
    app.stepsPerSecond = 30
    app.currentRoomDoors = ['left', 'right', 'top', 'bottom']
    app.spriteSize = 25
    app.goldR = 20
    app.helpScreenEnter = [600, 895, 230, 50]#left, top, width, height
    app.helpScreenExit = [1150, 250, 30, 30]#left, top, width, height
    app.enterRect = (app.width//2-92, app.height*0.75-25, 120, 122) #left, top, width, height
    app.swordStrength = 3
    app.swordReach = 70
    app.hourglass = (650, 400, 100, 150) #left, top, width, height
    app.portal = (700, 275, 300, 50) #centerX, centerY, width, height
    loadPlayerSprite(app)
    mummyFile = Image.open('mummy.png')
    app.mummyFile = CMUImage(mummyFile)
    goldFile = Image.open('gold.png')
    app.goldFile = CMUImage(goldFile)
    sandFile = Image.open('sand.png')
    app.sandFile = CMUImage(sandFile)
    app.endMessage = False
    gameStart(app)#json file

#distance formula
def distance(x1, y1, x2, y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5

#controls timer, checks for game over, checks for mob attacks, moves mummies
def onStep(app):
    if (app.gameOver or app.exited) and not app.endMessage:
        app.endMessage = True
        gameEnd(app)#json file
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
                app.goldScore = 0

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
            app.currentRoomCoords = app.currentRoom.dimensions()
            app.leftDoor = (app.currentRoomCoords[0], app.currentRoomCoords[3] - (app.currentRoomCoords[3] - app.currentRoomCoords[2])/2 - 50, 30, 100)#left, top, width, height
            app.rightDoor = (app.currentRoomCoords[1]-30, app.currentRoomCoords[3] - (app.currentRoomCoords[3] - app.currentRoomCoords[2])/2 - 50, 30, 100)#left, top, width, height
            app.topDoor = (app.currentRoomCoords[0] + (app.currentRoomCoords[1]-app.currentRoomCoords[0])/2 - 50, app.currentRoomCoords[2], 100, 30)#left, top, width, height
            app.bottomDoor = (app.currentRoomCoords[0] + (app.currentRoomCoords[1]-app.currentRoomCoords[0])/2 - 50, app.currentRoomCoords[3]-30, 100, 30)#left, top, width, height
            app.mummies = app.currentRoom.mummies
            app.sandInRoom = app.currentRoom.sand
            app.goldCoords = app.currentRoom.gold
            app.currentMapRowCol = (app.currentMapRowCol[0] + drow, app.currentMapRowCol[1] + dcol)
            if drow == -1:
                app.playerY = app.bottomDoor[1] - app.spriteSize - 10
            elif drow == 1:
                app.playerY = app.topDoor[1] + app.topDoor[2] + app.spriteSize 
            elif dcol == -1:
                app.playerX = app.rightDoor[0] - app.spriteSize - 10
            elif dcol == 1:
                app.playerX = app.leftDoor[0] + app.leftDoor[2] + app.spriteSize + 10

#controls image cycling for sprites, checks for gold and sand collision, checks for exit/doors
def doStep(app):
    app.spriteTimer += 1
    if app.spriteTimer%3 == 0:
        app.spriteI +=1
    if app.goldCoords != []:
        i = 0
        while i < len(app.goldCoords):
            coords = app.goldCoords[i]
            if distance(app.playerX, app.playerY, coords[0], coords[1]) <= app.spriteSize:
                app.goldScore += random.randint(1, 20)
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
    #previous rows and cols of player at edges
    prevtopRowCol = rowAndCol(app, app.playerX, app.playerY - app.spriteSize)
    prevbottomRowCol = rowAndCol(app, app.playerX, app.playerY + app.spriteSize)
    prevrightRowCol = rowAndCol(app, app.playerX + app.spriteSize, app.playerY)
    prevleftRowCol = rowAndCol(app, app.playerX - app.spriteSize, app.playerY)
    prevRowCols = [prevtopRowCol, prevbottomRowCol, prevrightRowCol, prevleftRowCol]
    app.playerX += app.speed * dx #movement
    app.playerY += app.speed * dy
    if (app.playerY-app.spriteSize < app.currentRoomCoords[2] or 
        app.playerY+app.spriteSize > app.currentRoomCoords[3]
        or app.playerX-app.spriteSize < app.currentRoomCoords[0] 
        or app.playerX+app.spriteSize > app.currentRoomCoords[1]):
        app.playerX -= app.speed * dx #within bounds of room
        app.playerY -= app.speed * dy
        return None
    #new rows and cols of player at edges
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
                return None
    if app.currentMapRowCol not in [(2, 0), (4, 2), (2, 4)]:
        if topRowCol != bottomRowCol and topRowCol not in app.currentRoom.graph[bottomRowCol]:
            app.playerX -= app.speed * dx #no impaling in maze
            app.playerY -= app.speed * dy
            return None
        if leftRowCol != rightRowCol and leftRowCol not in app.currentRoom.graph[rightRowCol]:
            app.playerX -= app.speed * dx #no impaling in maze
            app.playerY -= app.speed * dy
            return None

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
    row = int((y - topMargin) // (app.currentRoom.height/app.currentRoom.rows))
    col = int((x - leftMargin) // (app.currentRoom.width/app.currentRoom.cols))
    return (row, col)

#mouse clicks
def onMousePress(app, x, y):
    if app.titleScreen:
        if xyInside(app, x, y, app.enterRect[0], app.enterRect[0] + app.enterRect[2],
                     app.enterRect[1], app.enterRect[1] + app.enterRect[3]):
            app.titleScreen = False
            app.inDungeon = True
        elif app.helpScreen==False and xyInside(app, x, y, app.helpScreenEnter[0], 
                app.helpScreenEnter[0] + app.helpScreenEnter[2],
                app.helpScreenEnter[1], app.helpScreenEnter[1] + app.helpScreenEnter[3]):
            app.helpScreen = True
        elif app.helpScreen==True and xyInside(app, x, y, app.helpScreenExit[0], 
                app.helpScreenExit[0] + app.helpScreenExit[2],
                app.helpScreenExit[1], app.helpScreenExit[1] + app.helpScreenExit[3]):
            app.helpScreen = False
    if not app.paused:
        if app.inDungeon:
            for mummy in app.mummies:
                if distance(app.playerX, app.playerY, mummy.x, mummy.y) <= app.swordReach:
                    mummy.takeDamage(app.swordStrength)
            if xyInside(app, x, y, app.hourglass[0], app.hourglass[0] + app.hourglass[2],
                     app.hourglass[1], app.hourglass[1] + app.hourglass[3]):
                if app.inventorySand > 0 and app.currentMapRowCol == (2, 2):
                    app.timer += Sand.time
                    app.inventorySand -= 1

#moves player sprite
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
        gameSettings(app)

#makes sprite lists
#from PIL demo code by Melinda
#sprites drawn by me using pixilart.com
def loadPlayerSprite(app):
    spriteSheet = Image.open('player sprite sheet.png')
    app.leftSprites = []
    app.rightSprites = []
    app.upSprites = []
    app.downSprites = []
    leftStrip = spriteSheet.crop((0, 151, 200, 200))
    rightStrip = spriteSheet.crop((0, 51, 200, 100))
    upStrip = spriteSheet.crop((0, 101, 200, 150))
    downStrip = spriteSheet.crop((0, 0, 200, 50))
    for i in range(4):
        leftSprite = CMUImage(leftStrip.crop((i*50, 0, i*50+50, 50)))
        app.leftSprites.append(leftSprite)
        rightSprite = CMUImage(rightStrip.crop((i*50, 0, i*50+50, 50)))
        app.rightSprites.append(rightSprite)
        upSprite = CMUImage(upStrip.crop((i*50, 0, i*50+50, 50)))
        app.upSprites.append(upSprite)
        downSprite = CMUImage(downStrip.crop((i*50, 0, i*50+50, 50)))
        app.downSprites.append(downSprite)

#draws the sprite with the walking animation 
def drawSprite(app):
    if app.direction == 'right':
        spriteList = app.rightSprites
    elif app.direction == 'left':
        spriteList = app.leftSprites
    elif app.direction == 'up':
        spriteList = app.upSprites
    elif app.direction == 'down':
        spriteList = app.downSprites
    i = app.spriteI%4
    drawImage(spriteList[i], app.playerX, app.playerY, align = 'center', width = 60, height = 60)

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
    if app.currentMapRowCol != (2, 2):
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
                app.leftDoor[2], app.leftDoor[3], fill = 'saddleBrown')
        elif door == 'right':
            drow, dcol = 0, 1
            if isRoom(app, drow, dcol):
                drawRect(app.rightDoor[0], app.rightDoor[1], 
                app.rightDoor[2], app.rightDoor[3], fill = 'saddleBrown')
        elif door == 'top':
            drow, dcol = -1, 0
            if isRoom(app, drow, dcol):
                drawRect(app.topDoor[0], app.topDoor[1], 
                app.topDoor[2], app.topDoor[3], fill = 'saddleBrown')
        elif door == 'bottom':
            drow, dcol = 1, 0
            if isRoom(app, drow, dcol):
                drawRect(app.bottomDoor[0], app.bottomDoor[1], 
                app.bottomDoor[2], app.bottomDoor[3], fill = 'saddleBrown')

#draws the room from image
def drawRoom(app):
    room = app.currentRoom
    drawImage(room.path, app.currentRoomCoords[0], app.currentRoomCoords[2],
                width = room.width, height = room.height)

#draws the countdown timer
def drawTimer(app):
    minutes = str(app.timer // 60)
    seconds = str(app.timer - int(minutes) * 60)
    if int(seconds) <10:
        seconds = '0' + seconds
    time = minutes+':'+seconds
    drawRect(0, 0, 100, 50, fill = 'blue')
    drawLabel(time, 50, 25, fill = 'white', size = 18)

#draws pile of gold and sand
def drawGoldandSand(app):
    for coords in app.goldCoords:
        drawImage(app.goldFile, coords[0], coords[1], align = 'center')
    for sand in app.sandInRoom:
        if sand.onGround:
            drawImage(app.sandFile, sand.x, sand.y, align = 'center')

#draws mummies
def drawMummies(app):
    for mummy in app.mummies:
        if mummy.alive:
            drawImage(app.mummyFile, mummy.x, mummy.y, align = 'bottom')

#draws score
def drawScore(app):
    drawRect(1300, 0, 100, 50, fill = 'blue')
    drawLabel(app.goldScore, 1350, 25, fill = 'white', size = 18)

#draws amount of sand in inventory
def drawSandInventory(app):
    drawRect(1300, 60, 100, 50, fill = 'blue')
    drawLabel(f'Sand: {app.inventorySand}', 1350, 85, fill = 'white', size = 18)

#draws health bar
def drawHealth(app):
    percentHealth = app.health/app.startHealth
    barWidth = 100
    healthWidth = barWidth*percentHealth + 1
    drawRect(app.width//2-barWidth//2, 0, barWidth, 20, fill = 'red')
    drawRect(app.width//2-barWidth//2, 0, healthWidth, 20, fill = 'green')

#draws title screen 
def drawTitleScreen(app):
    titleScreenImage = Image.open('sot title screen 500x500.png')
    titleScreenImage = CMUImage(titleScreenImage)
    drawImage(titleScreenImage, 200, 0, width = 1000, height = 1000)

#draws help screen if active
def drawHelpScreen(app):
    howToPlay = Image.open('howtoplayscreen.png')
    howToPlay = CMUImage(howToPlay)
    drawImage(howToPlay, 150, 200, width = 1100, height = 600)
    drawRect(app.helpScreenExit[0], app.helpScreenExit[1], app.helpScreenExit[2], 
            app.helpScreenExit[3], fill = None, border = 'white')
    drawLabel('X', app.helpScreenExit[0]+app.helpScreenExit[2]/2, 
                app.helpScreenExit[1]+app.helpScreenExit[3]/2, fill = 'white')

#active while playing game
def drawDungeon(app):
    drawRoom(app)
    drawTimer(app)
    drawHealth(app)
    drawSandInventory(app)
    drawDoors(app)
    drawWalls(app)
    drawGoldandSand(app)
    drawScore(app)
    drawMummies(app)
    drawSprite(app)

#checks if game is not over, then draws everything
def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = 'black')
    if app.titleScreen:
        drawTitleScreen(app)
        if app.helpScreen:
            drawHelpScreen(app)
    elif app.inDungeon:
        drawDungeon(app)
    elif app.gameOver:
        drawLabel('You Died', app.width//2, app.height//2, fill = 'white', size = 20)
    elif app.exited:
        drawLabel(f'You won {app.goldScore} gold! Congrats', app.width//2, app.height//2, fill = 'white', size = 20)

#run app 
runApp(1400, 1000)



