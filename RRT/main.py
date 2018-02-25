import Maze
import RRT
import pygame

maze = Maze.Maze()

if __name__ == '__main__':
    RRT.rrt_star(maze)
    running = True
    while running:
       for event in pygame.event.get():
	    if event.type == pygame.QUIT:
               running = False
