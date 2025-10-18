from math import sqrt

class Vector3:
    def __init__(self, x:float, y:float, z:float):
        self.x = x
        self.y = y
        self.z = z
    
    def normalize(self):
        magnitude = sqrt(self.x**2 + self.y**2 + self.z**2)

        self.x /= magnitude
        self.y /= magnitude
        self.z /= magnitude
    
    def add(self, x:float, y:float, z:float):
        self.x += x
        self.y += y
        self.z += z