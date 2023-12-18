from nodes import AstarNode

class AstarRuntime:
    def __init__(self, start : AstarNode, goal : AstarNode, map_size : int, obstacles : list[tuple] = []) -> None:
        self.map_size = map_size
        self.start = start
        self.goal = goal

        self.frontier = {start.position(): self.start}
        self.closed = {}
        # temp obstacles for bugfixing
        self.obstacles = {}
        for obsl in obstacles:
            self.obstacles[obsl] = AstarNode(obsl, None, is_obstacle = True)

    def tick(self):
        current = self.find_viable_node()
        popped_current = self.frontier.pop(current.position())
        self.closed[popped_current.position()] = popped_current

        if current.position() == self.goal.position():
            print("reached")
            return current.get_path(True) 
    
        for neighbour_position in current.find_neighbours():
            if neighbour_position in self.closed.keys() or neighbour_position in self.obstacles.keys() or self.out_of_bounds(neighbour_position):
                continue
            
            neighbour = self.define_neighbour(neighbour_position, current)
            
            neighbour.optimize_path(current)

            if neighbour_position not in self.frontier.keys():
                self.frontier[neighbour_position] = neighbour

    def loop_tick(self):
        while True:
            info = self.tick()
            if info != None:
                return info
    
    def Astar_generator(self):
        while True:
            info = self.tick()
            yield {"frontier": [x for x in self.frontier.keys()], "closed": [x for x in self.closed.keys()], "obstacles": [x for x in self.obstacles.keys()], "start": self.start.position(), "goal": self.goal.position()}
            if info != None:
                yield {"path": [x.position() for x in info]}
                return
            
    def out_of_bounds(self, position : tuple) -> bool:
        return abs(position[0]) > self.map_size or abs(position[1]) > self.map_size
    
    def find_viable_node(self):
        low = list(self.frontier.values())[0]
        for node in self.frontier.values():
            nodeFcost = node.f_cost(self.goal)
            lowFcost = low.f_cost(self.goal)

            if nodeFcost < lowFcost:
                low = node
            
            elif nodeFcost > lowFcost:
                if node.h_cost(self.goal) < low.h_cost(self.goal):
                    low = node
        return low

    def define_neighbour(self, position : tuple, current : object):
        if position in self.frontier.keys():
            return self.frontier[position]

        return AstarNode(position, current)

    def get_node_eval_position(self, position_of_node, Astar_run_path = None) -> str:
        if Astar_run_path != None:
            if position_of_node in [x.position() for x in Astar_run_path]:
                return "path"
        
        if position_of_node in self.frontier.keys():
            return "frontier"
        
        if position_of_node in self.closed.keys():
            return "closed"
        
        if position_of_node in self.obstacles.keys():
            return "obstacle"
        
        return "undefined"