import pygame as pg
class AstarNode:
    def __init__(self, pos : tuple, parent : object, is_obstacle : bool = False) -> None:
        self.pos : tuple = pos
        self.obstacle : bool = is_obstacle
        self.parent : object = parent
        self.child : object = None
    
    def __str__(self) -> str:
        return f"node at {self.pos}: is obstacle {self.obstacle}: parent {self.parent}: child {self.child}"

    def position(self) -> tuple:
        return self.pos

    def is_obstacle(self) -> bool:
        return self.obstacle

    def f_cost(self, goal) -> int:
        return self.g_cost() + self.h_cost(goal)

    def g_cost(self, path : list = [None]) -> int:
        cost = 0
        node = self
        while node.parent is not None:
            dx, dy = abs(node.pos[0] - node.parent.pos[0]), abs(node.pos[1] - node.parent.pos[1])
            cost += 14 if dx != 0 and dy != 0 else 10
            node = node.parent
        return cost
    
    def h_cost(self, goal) -> int: 
        cx, cy = abs(self.pos[0] - goal.pos[0]), abs(self.pos[1] - goal.pos[1])
        return 14 * min(cx, cy) + 10 * abs(cx - cy)
    

    def update_path(self, new_parent : object) -> int:
        path = self.get_path(True)
        path[-1] = new_parent
        return self.g_cost(path)

    def optimize_path(self, current : object) -> int:
        if self.update_path(current) < self.g_cost():
            self.parent = current
            return 1
        return -1

    def get_path(self, include_self : bool = False) -> list:
        parent = self.parent
        path = []
        while True:
            if parent == None:
                break
            path.insert(0, parent)
            parent = parent.parent
            
        if include_self:
            path.insert(-1, self)
        
        return path
    
    def get_path_positions(self, include_self : bool = False):
        return [x.position() for x in self.get_path(include_self)]
    
    def find_neighbours(self) -> list:
        neighbours = []
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    continue
                x = i - 1
                y = j - 1
                neighbours.append((self.pos[0] + x, self.pos[1] + y))

        return neighbours

    
class VisualNode(pg.sprite.Sprite): 
    def __init__(self, WW : int, WH : int, position : tuple, size : tuple, color : tuple = (0, 0 ,0), eval_status = None) -> None:
        super(VisualNode, self).__init__()
        self.surf = pg.Surface(size)
        self.surf.fill(color)
        self.map_position = (position[0], abs(position[1]) if position[1] < 0 else -position[1]) #((abs(position[0]) if position[0] < 0 else -position[0]), (abs(position[1]) if position[1] < 0 else -position[1]))
        self.rect = self.surf.get_rect(center=((self.map_position[0] * (size[0] * 2) + WW) / 2, (self.map_position[1] * (size[1] * 2) + WH) / 2))

        self.WW = WW
        self.WH = WH
        self.Astar_position = position

        self.eval_status = eval_status
    
    def __str__(self) -> str:
        return f"size: {self.surf}, position: {self.rect}, Astar position: {self.Astar_position}"

    def get_Astar_position(self) -> tuple:
        return self.Astar_position
    
    def create_text(self, position : tuple, text : str, size : int = 10, color : tuple = (255, 255, 255)) -> tuple:
        font = pg.font.Font('freesansbold.ttf', size) 
        text = font.render(text, True, color) 
        textRect = text.get_rect(center=position)
        return (text, textRect)

    def show_node_position(self):
        return self.create_text((self.rect.centerx, self.rect.centery), f"{str(self.Astar_position)}")

    def change_color(self, new_color):
        self.surf.fill(new_color)