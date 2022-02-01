import sys
import numpy as np
import math
import random
import gym
from pentago_env import PentagoEnv
from pent_view_2d import MazeView2D

if __name__ == "__main__":

    env = PentagoEnv(maze_size=(6, 6), enable_render=True)

    env.render()

    for i in range(20):
        # selected_action = input("please enter an action: ")
        # input = np.array(selected_action,dtype=int)
        agent_action = env.action_space.sample()

        # action = env.action_space(agent_action)

        while env.step(agent_action) is False:
            agent_action = env.action_space.sample()

        env.render()

        if env.is_game_over():
            sys.exit()

    print('bye')
    # maze = MazeView2D(screen_size=(640, 640), maze_size=(6, 6))
    # maze.update()
    # input("Enter any key to quit.")