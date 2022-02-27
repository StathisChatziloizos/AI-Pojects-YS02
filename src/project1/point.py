import math


class Point2:
    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_

    def print(self):
        print("(%.2f, %.2f)" %(self.x, self.y))
    
    def printDistance(self, p2):
        distance = math.sqrt((self.x - p2.x) * (self.x - p2.x) + (self.y - p2.y) * (self.y - p2.y))
        print("Distance is","{:.2f}".format(distance))