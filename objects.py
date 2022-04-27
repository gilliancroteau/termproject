from pathandmazefunctions import *

#room object
class Room(object):
    def __init__(self, path, width, height, rows, cols, graph, mummies, sand, gold):
        self.path = path
        self.width = width
        self.height = height
        self.graph = graph
        self.rows = rows
        self.cols = cols
        self.mummies = mummies
        self.sand = sand
        self.gold = gold
    def topCoords(self):
        return (1400//2-self.width//2, 1000//2 - self.height//2) #these have app.width and app.height hard coded
    def dimensions(self):
        coords = self.topCoords()
        leftX = coords[0]
        rightX = coords[0] + self.width
        topY = coords[1]
        bottomY = coords[1] + self.height
        return [leftX, rightX, topY, bottomY]
    def __repr__(self):
        return self.path

#mummy object
class Mummy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 10
        self.damage = 3
        self.alive = True
        self.reach = 60
        self.r = 25
        self.color = 'white'
        self.speed = 2
    def move(self, playerX, playerY, roomGraph):
        pass
    def takeDamage(self, playerDamage):
        self.health -= playerDamage
        if self.health <= 0:
            self.alive = False
    def pathfind(self, playerNode, mummyNode, roomGraph):
        path = BFS(mummyNode, playerNode, roomGraph)
        if len(path) > 1:
            nextNode = path[1]
            drow = nextNode[0] - mummyNode[0]
            dcol = nextNode[1] - mummyNode[1]
            self.x += self.speed * dcol
            self.y += self.speed * drow

#sand object
class Sand(object):
    time = 10
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edgeSize = 30
        self.color = 'khaki'
        self.onGround = True