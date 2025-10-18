from util.vector3 import Vector3

class Face:
    def __init__(self, verts, norms):
        self.verts = verts
        self.normal = self.calc_norms(norms)
        self.color = self.calc_color()
    
    def calc_norms(self, norms) -> Vector3:
        current = Vector3(0, 0, 0)
        for norm in norms:
            current.add(norm.x, norm.y, norm.z)
        
        current.normalize()
        return current
    
    def calc_color(self):
        x = int(self.normal.x * 122.5) if self.normal.x >= 0 else abs(int(self.normal.x * 255))
        y = int(self.normal.y * 122.5) if self.normal.y >= 0 else abs(int(self.normal.y * 255))
        z = int(self.normal.z * 122.5) if self.normal.z >= 0 else abs(int(self.normal.z * 255))

        return (x, y, z)