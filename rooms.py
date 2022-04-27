from objects import *
from pathandmazefunctions import *
import random
from PIL import Image
from cmu_cs3_graphics import *

#Image module use from Melina PIL demo code
#all room images drawn by me using pixilart.com
#returns list of rooms to be put in dungeon
def createRooms():
    roomList = []
    #centralRoom
    centralRoomGraph = makeGraph(10, 10)
    hourglass = [(3, 4), (3, 5), (4, 4), (4, 5), (5, 4), (5, 5)]
    for coord in hourglass:
        centralRoomGraph = createHole(centralRoomGraph, coord)
    centralMummies = [Mummy(600, 500)]
    centralSand = [Sand(650, 650)]
    centralGold = [(900, 500), (600, 500)]
    centralRoomFile = CMUImage(Image.open('centralRoom.png'))
    centralRoom = Room(centralRoomFile, 500, 500, 10, 10, centralRoomGraph, 
                        centralMummies, centralSand, centralGold)
    roomList.append(centralRoom)
    #open1
    open1Graph = makeGraph(10, 10)
    mummies = [Mummy(650, 500), Mummy(850, 600)]
    sand = [Sand(750, 700), Sand(900, 300)]
    open1File = CMUImage(Image.open('open1.png'))
    open1 = Room(open1File, 500, 500, 10, 10, open1Graph, mummies, sand, [])
    roomList.append(open1)
    #maze
    mazeGraph = kruskals(makeGraph(9, 9))
    mummies = [Mummy(525, 725)]
    gold = []
    for _ in range(5):
        randX = random.randrange(300, 1100, 100)
        randY = random.randrange(100, 900, 100)
        gold.append((randX, randY))
    mazeFile = CMUImage(Image.open('maze.png'))
    maze = Room(mazeFile, 900, 900, 9, 9, mazeGraph, mummies, [], gold)
    roomList.append(maze)
    #vertical hallway
    graph = makeGraph(10, 5)
    vertHallwayFile = CMUImage(Image.open('vertHallway.png'))
    vertHallway = Room(vertHallwayFile, 250, 500, 10, 5, graph, [], [], [])
    roomList.append(vertHallway)
    #vault
    vaultGraph = makeGraph(10, 10)
    sand = []
    gold = []
    for i in range(random.randint(4, 10)):
        x1 = random.randint(600, 800)
        y1 = random.randint(350, 650)
        gold.append((x1, y1))
        if i % 2 == 0:
            x2 = random.randint(600, 800)
            y2 = random.randint(350, 650)
            sand.append(Sand(x2, y2))
    vaultFile = CMUImage(Image.open('vault.png'))
    vault = Room(vaultFile, 400, 400, 10, 10, vaultGraph, [], sand, gold)
    roomList.append(vault)
    #monster room
    graph = makeGraph(12, 12)
    sand = []
    gold = []
    mummies = []
    for i in range(8):
        mummies.append(Mummy(random.randint(400, 1000), random.randint(200, 850)))
    mobRoomFile = CMUImage(Image.open('mobRoom.png'))
    mobRoom = Room(mobRoomFile, 700, 700, 12, 12, graph, mummies, sand, gold)
    roomList.append(mobRoom)
    #horizontal hallway
    graph = makeGraph(5, 10)
    horHallwayFile = CMUImage(Image.open('horHallway.png'))
    horHallway = Room(horHallwayFile, 500, 250, 5, 10, graph, [], [], [])
    roomList.append(horHallway)
    #open with corners
    open2Graph = makeGraph(10, 10)
    for node in [(0, 0), (0, 9), (9, 0), (9, 9)]:
        open2Graph = createHole(open2Graph, node)
    mummies = [Mummy(850, 500), Mummy(650, 600)]
    sand = [Sand(850, 650), Sand(750, 300)]
    gold = [(850, 680), (675, 300), (625, 550)]
    open2File = CMUImage(Image.open('open2.png'))
    open2 = Room(open2File, 500, 500, 10, 10, open2Graph, mummies, sand, gold)
    roomList.append(open2)
    return roomList

#makes a map of the rooms
def roomMap(rooms): 
    centralRoom = rooms[0]
    open1 = rooms[1]
    maze = rooms[2]
    vertHallway = rooms[3]
    vault = rooms[4]
    mobRoom= rooms[5]
    horHallway = rooms[6]
    open2 = rooms[7]
    map = [[None]*5 for _ in range(5)]
    #set central room in middle
    map[2][2] = centralRoom
    #randomize rooms connected to central room
    firstRingRooms = [(2, 1), (3, 2), (2, 3)]
    random.shuffle(firstRingRooms)
    mazeCoords = firstRingRooms[0]
    mobRoomCoords = firstRingRooms[1]
    open1Coords = firstRingRooms[2]
    map[mazeCoords[0]][mazeCoords[1]] = maze
    map[mobRoomCoords[0]][mobRoomCoords[1]] = mobRoom
    map[open1Coords[0]][open1Coords[1]] = open1
    #set vault at end of mob room or maz
    vaultConnection = random.choice([mazeCoords, mobRoomCoords])
    if vaultConnection == (2, 1):
        vaultCoords = (2, 0)
    elif vaultConnection == (3, 2):
        vaultCoords = (4, 2)
    elif vaultConnection == (2, 3):
        vaultCoords = (2, 4)
    map[vaultCoords[0]][vaultCoords[1]] = vault
    #horizonal hallway in a corner
    horHallwayCoords = random.choice([(3, 1), (3, 3)])
    map[horHallwayCoords[0]][horHallwayCoords[1]] = horHallway
    #set hallway off of open room
    if open1Coords == (2, 1):
        vertHallwayCoords = (2, 0)
    elif open1Coords == (3, 2):
        vertHallwayCoords = (4, 2)
    elif open1Coords == (2, 3):
        vertHallwayCoords = (2, 4)
    map[vertHallwayCoords[0]][vertHallwayCoords[1]] = vertHallway
    #set second open room randomly off hallway
    DrowDcol = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random.shuffle(DrowDcol)
    for drow, dcol in DrowDcol:
        newRow = vertHallwayCoords[0] + drow
        newCol = vertHallwayCoords[1] + dcol
        if newCol < 0 or newRow < 0 or newCol > 4 or newRow > 4:
            pass
        elif map[newRow][newCol] == None:
            map[newRow][newCol] = open2
            break
    return map
