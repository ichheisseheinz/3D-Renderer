from util.vector3 import Vector3
from objects.face import Face

class FileLoader:
    def __init__(self, path):
        self.path = path
        self.file = open(path, 'r')
        self.data = self.file.read().split('\n')
        self.file.close()
    
    def get_verts(self, scale):
        found_verts = False
        verts = []

        for text in self.data:
            if text[:2] == 'v ':
                found_verts = True
                point = text.split(' ')
                    
                try:
                    verts.append([float(point[1]) * scale, float(point[2]) * -scale, float(point[3]) * scale])
                except ValueError:
                    print(f"Problem reading file '{self.path}': file vertex list contains types uncastable to floats")
            elif found_verts: # early return to prevent extra searching
                return verts
    
    def get_vertex_normals(self):
        found_norms = False
        norms = []

        for text in self.data:
            if text[:2] == 'vn':
                found_norms = True
                point = text.split(' ')

                try:
                    norms.append(Vector3(float(point[1]), float(point[2]), float(point[3])))
                except ValueError:
                    print(f"Problem reading file '{self.path}': file vertex normal list contains types uncastable to floats")
            elif found_norms:
                return norms
    
    def get_lines(self):
        lines = []

        for text in self.data:
            if text[:2] == 'f ':
                line = text.split(' ')
                verts = [] # keep verts

                for num in range(1, len(line)):
                    point = line[num].split('/')

                    try:
                        verts.append(int(point[0]) - 1) # subtract 1 to prevent IndexError
                    except ValueError:
                        print(f"Problem reading file '{self.path}': file face list contains types uncastable to ints")
                            
                for i in range(len(verts)):
                    first = verts[i]
                    second = verts[(i+1)%len(verts)] # return index to 0 at the end to close the shape
                    point = tuple(sorted([first, second])) # format to easily check for duplicates

                    if not point in lines: # ensure no duplicates in the list
                        lines.append(point)
        
        return lines
    
    def get_faces(self):
        faces = []
        vert_norms = self.get_vertex_normals()

        for text in self.data:
            if text[:2] == 'f ':
                line = text.split(' ')
                verts = []
                norms = []

                for num in range(1, len(line)):
                    face = line[num].split('/')

                    try:
                        verts.append(int(face[0]) - 1)
                    except ValueError:
                        print(f"Problem reading file '{self.path}': file face list contains types uncastable to ints")
                    
                    try:
                        norms.append(int(face[2]) - 1)
                    except ValueError:
                        print(f"Problem reading file '{self.path}': file face list contains types uncastable to ints")
            
                face_norm_list = []
                for i in norms:
                    face_norm_list.append(vert_norms[i])
                
                faces.append(Face(tuple(verts), tuple(face_norm_list)))

        return faces