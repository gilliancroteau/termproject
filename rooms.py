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
    centralRoom = Room('noPathYet', 500, 500, 10, 10, centralRoomGraph)
    roomList.append(centralRoom)
    #open1
    open1Graph = makeGraph(10, 10)
    open1 = Room('nopathyet', 500, 500, 10, 10, open1Graph)
    roomList.append(open1)
    #maze
    mazeGraph = kruskals(makeGraph(10, 10))
    maze = Room('nopathyet', 500, 500, 10, 10, mazeGraph)
    roomList.append(maze)
    return roomList


#this is extremely hard coded!!!! to be fixed with randmization
#makes a map of the rooms
def roomMap(rooms): 
    centralRoom = rooms[0]
    open1 = rooms[1]
    maze = rooms[2]
    map = [[None]*5 for _ in range(5)]
    map[2][2] = centralRoom
    map[2][3] = open1
    map[3][2] = maze
    return map
