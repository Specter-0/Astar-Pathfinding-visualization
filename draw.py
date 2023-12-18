import pygame as pg
import sys
from nodes import VisualNode, AstarNode
from runtime import AstarRuntime

from pygame.locals import (
  K_ESCAPE,
  QUIT,
  KEYDOWN
)

def get_map(size : int):
  for i in range(-size, size + 1):
    for j in range(-size, size + 1):
      yield (i, j)

def check_quit(event):
  if event.type == QUIT:
    return True
  
  if event.type == KEYDOWN:
    if event.key == K_ESCAPE:
      return True
  
  return False

pg.init()

FPS = 1000
WH = 700 # window-height
WW = 1000 # window-width
SM = (WW / 2, WH / 2) # center of screen

MAP_SIZE : int = int(10 / 2)

WHITE = (255, 255, 255)
SMOKEWHITE = (200, 200, 200)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 255, 30)
TEAL = (0, 255, 150)
LIGHTBLUE = (0, 100, 170)
RED = (230, 40, 40)

display = pg.display.set_mode((WW, WH))

clock = pg.time.Clock()

obstacles = [(-3, 5), (-2, 4), (-1, 3), (-2, 5), (0, 3), (-1, 3), (-2, 3), (-3, 3), (-4, 3)]
Astar = AstarRuntime(AstarNode((-5, 5), None), AstarNode((5, 5), None), MAP_SIZE, obstacles)

# -------------------- Create Nodes --------------------- #
visual_nodes = {}

"""
astar_run = Astar.loop_tick()

for position in get_map(MAP_SIZE):
  node_status = Astar.get_node_eval_position(position, astar_run)
  match node_status:
    case "path":
      color = (0, 255, 70)

    case "frontier":
      color = (0, 100, 30)
    
    case "closed":
      color = (150, 100, 100)

    case "obstacle":
      color = (0, 0, 0)
    
    case "undefined":
      color = (50, 50, 50)

  visual_nodes[position] = VisualNode(WW, WH, position, (60, 60), color, node_status)
"""

blank_node_color = (50, 50, 50)
for map_position in get_map(MAP_SIZE):
  visual_nodes[map_position] = VisualNode(WW, WH, map_position, (60, 60), blank_node_color)

Astar_generator = Astar.Astar_generator()

# -------------------- Mainloop --------------------- #
while True:
  # -------------------- Pygame Setup ------------------- #
  clock.tick(FPS)
  
  display.fill(SMOKEWHITE)
  
  for event in pg.event.get():
    if check_quit(event):
      pg.quit()
      sys.exit()  

  # ------------------------ Astar ---------------------- #
  try:
    for container, content in next(Astar_generator).items():
      match container:
        case "frontier":
          color = LIGHTBLUE
          for node_position in content:
            visual_nodes[node_position].change_color(color)

        case "closed":
          color = (120, 30, 30)
          for node_position in content:
            visual_nodes[node_position].change_color(color)

        case "obstacles":
          color = BLACK
          for node_position in content:
            visual_nodes[node_position].change_color(color)

        case "path":
          color = TEAL
          for node_position in content:
            visual_nodes[node_position].change_color(color)
        
        case "start":
          color = GREEN
          visual_nodes[content].change_color(color)
        
        case "goal":
          color = RED
          visual_nodes[content].change_color(color)
  except StopIteration:
    pass

  for node in visual_nodes.values():
    display.blit(node.surf, node.rect)
    text = node.show_node_position()
    display.blit(text[0], text[1])

  pg.display.flip() 