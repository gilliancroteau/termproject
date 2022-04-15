from pathandmazefunctions import *

#room object
class Room(object):
    def __init__(self, path, width, height):
        self.path = path
        self.width = width
        self.height = height
    def topCoords(self):
        return (1500//2-self.width//2, 1000//2 - self.height//2) #these have app.width and app.height hard coded
    def dimensions(self):
        coords = self.topCoords()
        leftX = coords[0]
        rightX = coords[0] + self.width
        topY = coords[1]
        bottomY = coords[1] + self.height
        return [leftX, rightX, topY, bottomY]

#wall object, child of room cause it kinda works the same
class Wall(Room):
    def __init__(self, path, width, height, topX, topY):
        super().__init__(path, width, height)
        self.topX = topX
        self.topY = topY
    def dimensions(self):
        leftX = self.topX
        rightX = self.topX + self.width
        topY = self.topY
        bottomY = self.topY + self.height
        return [leftX, rightX, topY, bottomY]


#mummy object
class Mummy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 10
        self.damage = 1
        self.alive = True
        self.reach = 40
        self.r = 30
        self.color = 'white'
    def move(self, playerX, playerY, roomGraph):
        pass
    def takeDamage(self, playerDamage):
        self.health -= playerDamage
        if self.health <= 0:
            self.alive = False


#sand
class Sand(object):
    time = 10
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edgeSize = 30
        self.color = 'khaki'
        self.onGround = True