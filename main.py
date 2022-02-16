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
        taken, done = env.step(agent_action)

        while taken is True:
            agent_action = env.action_space.sample()
            taken, done = env.step(agent_action)

        env.render()

        if env.is_game_over():
            sys.exit()

        if done:
            env.show_result()
            break

    print('bye')
    # maze = MazeView2D(screen_size=(640, 640), maze_size=(6, 6))
    # maze.update()
    # input("Enter any key to quit.")