class node:
    """
    node class representing a cell in the grid
    """
    def __init__(self, location, path=None, spath=None, unblocked=True):
        """
        Constructor for node class

        Args:
            location (tuple): tuple containing x and y location of cell
            f (int, optional): f value of cell equivalent to g+h. Defaults to 0.
            g (int, optional): g value representing distance from current cell to this cell. Defaults to 0.
            h (int, optional): h value representing distance from this cell to end. Defaults to 0.
        """
        super().__init__()
        self.location = location
        self.f = 0
        self.g = 0
        self.h = 0
        self.previous = None
        self.unblocked = unblocked
        self.path = path
        self.spath = spath
        self.neighbors = []
        self.previous = None

    def addNeighbors(self, grid):
        i = self.location[0]
        j = self.location[1]
        if i < len(grid[0])-1 and grid[self.location[0] + 1][j].unblocked is True:
            self.neighbors.append(grid[self.location[0] + 1][j])
        if i > 0 and grid[self.location[0] - 1][j].unblocked is True:
            self.neighbors.append(grid[self.location[0] - 1][j])
        if j < len(grid)-1 and grid[self.location[0]][j + 1].unblocked is True:
            self.neighbors.append(grid[self.location[0]][j + 1])
        if j > 0 and grid[self.location[0]][j - 1].unblocked is True:
            self.neighbors.append(grid[self.location[0]][j - 1])
