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
                except:
                    print(f"Problem reading file '{self.path}': file vertex list contains types uncastable to floats")
            elif found_verts: # early return to prevent extra searching
                return verts
    
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
                    except:
                        print(f"Problem reading file '{self.path}': file face list contains types uncastable to ints")
                            
                for i in range(len(verts)):
                    first = verts[i]
                    second = verts[(i+1)%len(verts)] # return index to 0 at the end to close the shape
                    point = tuple(sorted([first, second])) # format to easily check for duplicates

                    if not point in lines: # ensure no duplicates in the list
                        lines.append(point)
        
        return lines