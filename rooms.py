from objects import *
from pathandmazefunctions import *
import random

#returns list of rooms to be put in dungeon
def createRooms():
    roomList = []
    #centralRoom
    centralRoomGraph = makeGraph(10, 10)
    hourglass = [(3, 4), (3, 5), (4, 4), (4, 5), (5, 4), (5, 5)]
    for coord in hourglass:
        centralRoomGraph = createHole(centralRoomGraph, coord)
    centralMummies = [Mummy(650, 500)]
    centralSand = [Sand(650, 650)]
    centralGold = [(900, 500), (600, 500)]
    centralRoom = Room('centralRoom', 500, 500, 10, 10, centralRoomGraph, 
                        centralMummies, centralSand, centralGold)
    roomList.append(centralRoom)
    #open1
    open1Graph = makeGraph(10, 10)
    mummies = [Mummy(650, 500), Mummy(850, 600)]
    sand = [Sand(750, 700), Sand(900, 300)]
    open1 = Room('open1', 500, 500, 10, 10, open1Graph, mummies, sand, [])
    roomList.append(open1)
    #maze
    mazeGraph = kruskals(makeGraph(9, 9))
    mummies = [Mummy(525, 725)]
    gold = [(625, 730)]
    maze = Room('maze', 900, 900, 9, 9, mazeGraph, mummies, [], gold)
    roomList.append(maze)
    #vertical hallway
    graph = makeGraph(10, 5)
    vertHallway = Room('vertHallway', 250, 500, 10, 5, graph, [], [], [])
    roomList.append(vertHallway)
    #vault
    graph = makeGraph(10, 10)
    sand = []
    gold = []
    for i in range(10):
        x1 = random.randint(600, 900)
        y1 = random.randint(350, 650)
        gold.append((x1, y1))
        if i % 2 == 0:
            x2 = random.randint(600, 900)
            y2 = random.randint(350, 650)
            sand.append(Sand(x2, y2))
    vault = Room('vault', 400, 400, 10, 10, graph, [], sand, gold)
    roomList.append(vault)
    #monster room
    graph = makeGraph(12, 12)
    sand = []
    gold = []
    mummies = []
    for i in range(8):
        mummies.append(Mummy(random.randint(400, 1100), random.randint(150, 850)))
    mobRoom = Room('mobRoom', 700, 700, 12, 12, graph, mummies, sand, gold)
    roomList.append(mobRoom)
    #horizontal hallway
    graph = makeGraph(5, 10)
    horHallway = Room('horHallway', 500, 250, 5, 10, graph, [], [], [])
    roomList.append(horHallway)
    #open with corners
    open2Graph = makeGraph(10, 10)
    for node in [(0, 0), (0, 9), (9, 0), (9, 9)]:
        open2Graph = createHole(open2Graph, node)
    mummies = [Mummy(850, 500), Mummy(650, 600)]
    sand = [Sand(850, 650), Sand(550, 300)]
    gold = [(950, 680), (575, 300), (625, 550)]
    open2 = Room('open2', 500, 500, 10, 10, open2Graph, mummies, sand, gold)
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

    map[2][2] = centralRoom

    firstRingRooms = [(2, 1), (3, 2), (2, 3)]
    random.shuffle(firstRingRooms)
    mazeCoords = firstRingRooms[0]
    mobRoomCoords = firstRingRooms[1]
    open1Coords = firstRingRooms[2]
    
    map[mazeCoords[0]][mazeCoords[1]] = maze
    map[mobRoomCoords[0]][mobRoomCoords[1]] = mobRoom
    map[open1Coords[0]][open1Coords[1]] = open1

    vaultConnection = random.choice([mazeCoords, mobRoomCoords])
    if vaultConnection == (2, 1):
        vaultCoords = (2, 0)
    elif vaultConnection == (3, 2):
        vaultCoords = (4, 2)
    elif vaultConnection == (2, 3):
        vaultCoords = (2, 4)
    map[vaultCoords[0]][vaultCoords[1]] = vault
    
    horHallwayCoords = random.choice([(3, 1), (3, 3)])
    map[horHallwayCoords[0]][horHallwayCoords[1]] = horHallway

    if open1Coords == (2, 1):
        vertHallwayCoords = (2, 0)
    elif open1Coords == (3, 2):
        vertHallwayCoords = (4, 2)
    elif open1Coords == (2, 3):
        vertHallwayCoords = (2, 4)
    map[vertHallwayCoords[0]][vertHallwayCoords[1]] = vertHallway

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

