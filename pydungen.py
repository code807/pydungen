import random

def __init__():
    random.seed("203F44B90FA0BEC09CFC3BF2401DFF1B04039C3D7E2051775885BF99E62C44D50A8E58A19C1CA4DA26C942F6BEF5F326570695475077986F86FC43382C4060D3")

class vec2():

    def __repr__(self):
        return "".join(["v(",str(self.x),",",str(self.y),")"])
    
    def __str__(self):
        return "".join(["v(",str(self.x),",",str(self.y),")"])
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, another):
        return hasattr(another, 'x') and self.x == another.x and hasattr(another, 'y') and self.y == another.y
    
    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        if type(other) in [int, float]:
            x = self.x + other
            y = self.y + other
        elif type(other) == vec2:
            x = self.x + other.x
            y = self.y + other.y
        else:
            return None
        return vec2(x, y)
    
    def __sub__(self, other):
        if type(other) in [int, float]:
            x = self.x - other
            y = self.y - other
        elif type(other) == vec2:
            x = self.x - other.x
            y = self.y - other.y
        else:
            return None
        return vec2(x, y)
    
    def __mul__(self, other):
        if type(other) in [int, float]:
            x = self.x * other
            y = self.y * other
        elif type(other) == vec2:
            x = self.x * other.x
            y = self.y * other.y
        else:
            return None
        return vec2(x, y)
    
    def __truediv__(self, other):
        if type(other) in [int, float]:
            x = self.x / other
            y = self.y / other
        elif type(other) == vec2:
            x = self.x / other.x
            y = self.y / other.y
        else:
            return None
        return vec2(x, y)

    def round(self):
        self.x = round(self.x)
        self.y = round(self.y)
        return self
    
    def area(self):
        return self.x*self.y

def nopaths(cell):
    return len(cell.paths) == 0

class cell():
    def __init__(self, pos):
        self.pos = pos
        self.connections = []
        self.paths = []
        self.isRoom = False
    pass

def maybe(percent=50):
    return random.randrange(100) < percent

def gridgen(size):
    grid = {}
    for y in range(size.y):
        for x in range(size.x):
            pos = vec2(x, y)
            grid[pos] = cell(pos)
    for pos in grid.keys():
            working = grid[pos]
            for x2 in range(-1, 2, 2):
                offset = vec2(x2, 0)
                if pos+offset in grid.keys():
                    working.connections.append(pos+offset)
            for y2 in range(-1, 2, 2):
                offset = vec2(0, y2)
                if pos+offset in grid.keys():
                    working.connections.append(pos+offset)
    return grid

def recursivemaze(grid):
    path = [vec2(0, 0)]
    while len(path) > 0:
        cursor = path[-1]
        connections = [grid[c] for c in grid[cursor].connections]
        connections = [c.pos for c in filter(nopaths, connections)]
        if len(connections) == 0:
            path.pop(-1)
            continue
        goto = random.choice(connections)
        grid[cursor].paths.append(goto)
        grid[goto].paths.append(cursor)
        path.append(goto)

def randomrooms(max_size, dungeonsize):
    workingregions = [[vec2(0, 0), dungeonsize]]
    finsihedregions = []
    numo = 0
    while len(workingregions) > 0:
        """
        print("Working on:")
        [print(x) for x in workingregions]
        print("Finished:")
        [print(x) for x in finsihedregions]
        print()
        """
        numo += 1
        region = workingregions[0]
        pos = region[0]
        size = region[1]
        if maybe(1):
            vh = maybe(50)
            if size.x > 3:
                if vh:
                    splitpoint = random.randint(0, size.x-1)
                    newregions = [
                        [pos, vec2(splitpoint+1, size.y)],
                        [pos+vec2(splitpoint+1, 0), size-vec2(splitpoint+1, 0)]
                    ]
                    workingregions.pop(0)
                    for region in newregions:
                        workingregions.append(region)
                    continue
            if size.y > 3:
                if not vh:
                    splitpoint = random.randint(0, size.y-1)
                    newregions = [
                        [pos, vec2(size.x, splitpoint+1)],
                        [pos+vec2(0, splitpoint+1), size-vec2(0, splitpoint+1)]
                    ]
                    workingregions.pop(0)
                    for region in newregions:
                        workingregions.append(region)
                    continue
        if size.y <= max_size.y and size.x <= max_size.x:
            if maybe(30):
                finsihedregions.append(workingregions.pop(0))
        """
        else:
            print(str(size)+" was not less than "+str(max_size))
        """
    return finsihedregions

    

def mazeto2d(grid):
    draw = []
    drawgrid = []
    xmin = 0
    ymin = 0
    ymax = 0
    xmax = 0
    for pos in grid.keys():
        if pos.x*2 < xmin:
            xmin = pos.x*2
        if pos.x*2+1 > xmax:
            xmax = pos.x*2+1
        if pos.y*2 < ymin:
            ymin = pos.y*2
        if pos.y*2+1 > ymax:
            ymax = pos.y*2+1
        draw.append(pos*2)
        for path in grid[pos].paths:
            mid = ((pos*2+path*2)/2).round()
            draw.append(mid)
    for y in range(ymax-ymin):
        row = [" " for x in range(xmax-xmin)]
        drawgrid.append(row)
    for call in draw:
        drawgrid[call.y][call.x] = "▒"
        # drawgrid[call.y].replace(call.x,"x")
    """
    for row in drawgrid:
        print("".join(row))
    """
    return drawgrid


dungeonsize = vec2(24, 24)
dungeon = gridgen(dungeonsize)
recursivemaze(dungeon)
drawgrid = mazeto2d(dungeon)
rooms = randomrooms(vec2(8, 8), dungeonsize)

random.shuffle(rooms)
for room in rooms:
    if room[1].x > 2 and room[1].y > 2:
        # if maybe(100):
        pos = room[0]
        size = room[1]
        for y in range(size.y*2-1):
            for x in range(size.x*2-1):
                drawgrid[pos.y*2+y][pos.x*2+x] = "▒"

for row in drawgrid:
    print("".join(row))
