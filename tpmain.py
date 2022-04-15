from cmu_cs3_graphics import *
from objects import *


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
    app.startRoom = Room('no path yet', 500, 500)
    app.startRoomCoords = app.startRoom.dimensions()  #[leftX, rightX, topY, bottomY]
    app.walls = [Wall('noPathYet', 100, 200, 700, 350)]
    app.timer = 120
    app.goldScore = 0
    app.goldPerGold = 10
    app.spriteSize = 25
    app.goldCoords = [(900, 500), (600, 500)]
    app.goldR = 20
    app.titleScreen = True
    app.inDungeon = False
    app.exited = False
    app.gameOver = False
    app.enterRect = (app.width//2-50, app.height*0.75-25, 100, 50) #left, top, width, height
    app.startHealth = 20
    app.health = app.startHealth
    app.swordStrength = 5
    app.swordReach = 40
    app.mummies = [Mummy(650, 500)]
    app.inventorySand = 0
    app.sandInRoom = [Sand(650, 650)]
    app.hourglass = (700, 350, 100, 200) #left, top, width, height
    app.portal = (app.width//2, 250, 300, 50) #centerX, centerY, width, height


#distance formula
def distance(x1, y1, x2, y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5

#controls timer, checks for game over, checks for mob attacks
def onStep(app):
    if not app.paused:
        if app.inDungeon:
            app.sandTimer += 1
            if app.sandTimer % app.stepsPerSecond == 0:
                app.timer -= 1
                for mummy in app.mummies:
                    if distance(app.playerX, app.playerY, mummy.x, mummy.y) <= mummy.reach:
                        app.health -= mummy.damage
            if app.timer <= 0 or app.health <= 0:
                app.inDungeon = False
                app.gameOver = True
        

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
    
    if xyInside(app, app.playerX, app.playerY - app.spriteSize,
             app.portal[0]-app.portal[2]/2, app.portal[0] + app.portal[2]/2,
                app.portal[1]-app.portal[3]/2, app.portal[1] + app.portal[3]/2):
        app.inDungeon = False
        app.exited = True

#moves sprite and checks for room bounds
def doMove(app, dx, dy):
    app.playerX += app.speed * dx
    app.playerY += app.speed * dy
    if (app.playerY-app.spriteSize < app.startRoomCoords[2] or 
        app.playerY+app.spriteSize > app.startRoomCoords[3]
        or app.playerX-app.spriteSize < app.startRoomCoords[0] 
        or app.playerX+app.spriteSize > app.startRoomCoords[1]):
        app.playerX -= app.speed * dx #within bounds of room
        app.playerY -= app.speed * dy
    for wall in app.walls:
        wallCoords = wall.dimensions()
        if (app.playerX+app.spriteSize >= wallCoords[0] and
            app.playerX-app.spriteSize <= wallCoords[1] and
            app.playerY+app.spriteSize >= wallCoords[2] and
            app.playerY-app.spriteSize <= wallCoords[3]):
            app.playerX -= app.speed * dx #outsode of wall
            app.playerY -= app.speed * dy

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

#draws the room as a rectangle (will eventually be from an image)
def drawRoom(app):
    room = app.startRoom
    coords = room.topCoords()
    drawRect(coords[0], coords[1], room.width, room.height, fill= 'orange')

#draws walls as a rectangle for testing purposes, will eventually be drawn only in room image
def drawWalls(app):
    for wall in app.walls:
        drawRect(wall.topX, wall.topY, wall.width, wall.height, fill = 'yellow')

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
    drawRect(app.portal[0], app.portal[1], app.portal[2], app.portal[3], 
    fill = 'purple', borderWidth = 10, border = 'black', align = 'center')

#returns True if x and y are inside these bounds
def xyInside(app, x, y, leftX, rightX, topY, bottomY):
    if leftX <= x <= rightX and topY <= y <= bottomY:
        return True
    return False


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
    drawWalls(app)
    drawSprite(app)
    drawTimer(app)
    drawGoldandSand(app)
    drawScore(app)
    drawMummies(app)
    drawHealth(app)
    drawSandInventory(app)
    drawPortal(app)


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

