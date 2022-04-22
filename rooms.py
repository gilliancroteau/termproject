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
    centralRoom = Room('noPathYet', 500, 500, 10, 10, centralRoomGraph, 
                        centralMummies, centralSand, centralGold)
    roomList.append(centralRoom)
    #open1
    open1Graph = makeGraph(10, 10)
    mummies = [Mummy(650, 500), Mummy(850, 600)]
    sand = [Sand(750, 700), Sand(900, 300)]
    open1 = Room('nopathyet', 500, 500, 10, 10, open1Graph, mummies, sand, [])
    roomList.append(open1)
    #maze
    mazeGraph = kruskals(makeGraph(9, 9))
    mummies = [Mummy(525, 725)]
    gold = [(625, 745)]
    maze = Room('nopathyet', 900, 900, 9, 9, mazeGraph, mummies, [], gold)
    roomList.append(maze)
    #vertical hallway
    graph = makeGraph(10, 5)
    vertHallway = Room('nopathyet', 250, 500, 10, 5, graph, [], [], [])
    roomList.append(vertHallway)
    #vault
    graph = makeGraph(10, 10)
    sand = []
    gold = []
    for i in range(10):
        x1 = random.randint(550, 950)
        y1 = random.randint(300, 700)
        gold.append((x1, y1))
        if i % 2 == 0:
            x2 = random.randint(550, 950)
            y2 = random.randint(300, 700)
            sand.append(Sand(x2, y2))
    vault = Room('nopathyet', 400, 400, 10, 10, graph, [], sand, gold)
    roomList.append(vault)
    #monster room
    graph = makeGraph(12, 12)
    sand = []
    gold = []
    mummies = []
    for i in range(8):
        mummies.append(Mummy(random.randint(400, 1100), random.randint(150, 850)))
    mobRoom = Room('nopathyet', 700, 700, 12, 12, graph, mummies, sand, gold)
    roomList.append(mobRoom)
    return roomList


#this is extremely hard coded!!!! to be fixed with randmization
#makes a map of the rooms
def roomMap(rooms): 
    centralRoom = rooms[0]
    open1 = rooms[1]
    maze = rooms[2]
    vertHallway = rooms[3]
    vault = rooms[4]
    mobRoom= rooms[5]
    map = [[None]*5 for _ in range(5)]
    map[2][2] = centralRoom
    map[2][3] = open1
    map[3][2] = maze
    map[3][3] = vertHallway
    map[4][2] = vault
    map[2][1] = mobRoom
    return map
