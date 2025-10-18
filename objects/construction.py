import math

from file.file_loader import FileLoader

class Shape:
    def __init__(self, x, y, z):
        self.shape = [
            (x, y, z), # Origin
            [], # Points
            [], # Lines
            [] # Faces
        ]

class Box(Shape):
    def __init__(self, x, y, z, length, width, height):
        super().__init__(x, y, z)
        self.length = length
        self.width = width
        self.height = height
    
    def construct(self):
        # Points
        self.shape[1].append([self.length/2 + self.shape[0][0], self.height/2 + self.shape[0][1], self.width/2 + self.shape[0][2]])
        self.shape[1].append([self.length/2 + self.shape[0][0], -self.height/2 + self.shape[0][1], self.width/2 + self.shape[0][2]])
        self.shape[1].append([-self.length/2 + self.shape[0][0], self.height/2 + self.shape[0][1], self.width/2 + self.shape[0][2]])
        self.shape[1].append([-self.length/2 + self.shape[0][0], -self.height/2 + self.shape[0][1], self.width/2 + self.shape[0][2]])
        self.shape[1].append([self.length/2 + self.shape[0][0], self.height/2 + self.shape[0][1], -self.width/2 + self.shape[0][2]])
        self.shape[1].append([self.length/2 + self.shape[0][0], -self.height/2 + self.shape[0][1], -self.width/2 + self.shape[0][2]])
        self.shape[1].append([-self.length/2 + self.shape[0][0], self.height/2 + self.shape[0][1], -self.width/2 + self.shape[0][2]])
        self.shape[1].append([-self.length/2 + self.shape[0][0], -self.height/2 + self.shape[0][1], -self.width/2 + self.shape[0][2]])

        # Lines
        self.shape[2] = [(0,1), (1,3), (3,2), (2,0), (0,4), (1,5), (3,7), (2,6), (4,5), (5,7), (7,6), (6,4)]

class Pyramid(Shape):
    def __init__(self, x, y, z, length, width, height):
        super().__init__(x, y, z)
        self.length = length
        self.width = width
        self.height = height

    def construct(self):
        # Points
        self.shape[1].append([self.length/2 + self.shape[0][0], self.height/2 + self.shape[0][1], self.width/2 + self.shape[0][2]])
        self.shape[1].append([self.length/2 + self.shape[0][0], self.height/2 + self.shape[0][1], -self.width/2 + self.shape[0][2]])
        self.shape[1].append([-self.length/2 + self.shape[0][0], self.height/2 + self.shape[0][1], self.width/2 + self.shape[0][2]])
        self.shape[1].append([-self.length/2 + self.shape[0][0], self.height/2 + self.shape[0][1], -self.width/2 + self.shape[0][2]])
        self.shape[1].append([self.shape[0][0], -self.height/2 + self.shape[0][1], self.shape[0][2]])

        # Lines
        self.shape[2] = [(0,1), (1,3), (3,2), (2,0), (0,4), (1,4), (2,4), (3,4)]

class Prism(Shape):
    def __init__(self, x, y, z, radius, height, resolution):
        super().__init__(x, y, z)
        self.radius = radius
        self.height = height
        self.resolution = resolution
    
    def construct(self):
        # Points
        for i in range(self.resolution):
            theta = ((2 * math.pi) / self.resolution) * i
            self.shape[1].append([(self.radius * -math.sin(theta)) + self.shape[0][0], self.height/2 + self.shape[0][1], (self.radius * math.cos(theta)) + self.shape[0][2]])
        for i in range(self.resolution):
            theta = ((2 * math.pi) / self.resolution) * i
            self.shape[1].append([(self.radius * -math.sin(theta)) + self.shape[0][0], -self.height/2 + self.shape[0][1], (self.radius * math.cos(theta)) + self.shape[0][2]])
        
        # Lines
        for i in range(self.resolution):
            if not i == self.resolution - 1:
                self.shape[2].append((i, i+1))
            else:
                self.shape[2].append((i, 0))
        for i in range(self.resolution, 2*self.resolution):
            if not i == 2*self.resolution - 1:
                self.shape[2].append((i, i+1))
            else:
                self.shape[2].append((i, self.resolution))
        for i in range(self.resolution):
            self.shape[2].append((i, i+self.resolution))

class Cone(Shape):
    def __init__(self, x, y, z, radius, height, resolution):
        super().__init__(x, y, z)
        self.radius = radius
        self.height = height
        self.resolution = resolution
    
    def construct(self):
        # Points
        for i in range(self.resolution):
            theta = ((2 * math.pi) / self.resolution) * i
            self.shape[1].append([(self.radius * -math.sin(theta)) + self.shape[0][0], self.height/2 + self.shape[0][1], (self.radius * math.cos(theta)) + self.shape[0][2]])
        self.shape[1].append([self.shape[0][0], -self.height/2 + self.shape[0][1], self.shape[0][2]])
        
        # Lines
        for i in range(self.resolution):
            if not i == self.resolution - 1:
                self.shape[2].append((i, i+1))
            else:
                self.shape[2].append((i, 0))
        for i in range(self.resolution):
            self.shape[2].append((i, self.resolution))

class CustomOBJ(Shape):
    def __init__(self, x, y, z, path, scale):
        super().__init__(x, y, z)
        self.loader = FileLoader(path)
        self.scale = scale

    def construct(self):
        self.shape[1] = self.loader.get_verts(self.scale)
        self.shape[2] = self.loader.get_lines()
        self.shape[3] = self.loader.get_faces()
