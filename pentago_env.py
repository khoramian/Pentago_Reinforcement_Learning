import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from pent_view_2d import MazeView2D
import time


class PentagoEnv(gym.Env):

    def __init__(self, maze_size=None, enable_render=True):

        self.enable_render = enable_render

        if maze_size:
            self.maze_view = MazeView2D(maze_size=maze_size, screen_size=(640, 640), enable_render=enable_render)
        else:
            raise AttributeError("One must supply the maze_size (2D)")

        self.maze_size = self.maze_view.maze_size

        # action is like (x, y, board quarter )
        low = np.zeros((3,), dtype=int)
        high = np.array([5, 5, 3], dtype=int)
        self.action_space = spaces.Box(low, high, dtype=int)

        # observation is like
        # low = np.zeros(len(self.maze_size), dtype=int)
        # high = np.array(self.maze_size, dtype=int) - np.ones(len(self.maze_size), dtype=int)
        # self.observation_space = spaces.Box(low, high, dtype=np.int64)

        # initial condition env and agent representing state
        #self.env = [] #(or none)
        #self.agent = []

        self.done = False
        self.steps_beyond_done = None

        # Simulation related variables.
        self.seed()
        self.reset()

        # Just need to initialize the relevant attributes
        self.configure()

    def __del__(self):
        if self.enable_render is True:
            self.maze_view.quit_game()

    def configure(self, display=None):
        self.display = display

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, agent_action):

        if self.action_space.contains(agent_action) is False:
            raise AttributeError("Must supply an action from Action Box")

        if self.maze_view.is_taken(agent_action[0:2]):
            print("Button location for agent is taken. action was: " + str(agent_action))
            return False

        print('Agent action is:' + str(agent_action))
        self.maze_view.play_agent(agent_action)

        env_win = self.maze_view.env_horizontal_line() or self.maze_view.env_vertical_line() or self.maze_view.env_diagonal_line()
        agent_win = self.maze_view.agent_horizontal_line() or self.maze_view.agent_vertical_line() or self.maze_view.agent_diagonal_line()

        done = True

        if env_win and agent_win:
            print('Both has won the game. It is a draw!!!')
        elif env_win:
            print('Environment has won the game!!!')
        elif agent_win:
            print('Agent has won the game!!!')
        elif len(self.maze_view.env) + len(self.maze_view.agent) == self.maze_size[0] * self.maze_size[0]:
            print('No one has won the game. It is a draw!!!')
        else:    # continue the game
            done = False

        if done:
            time.sleep(20)
            raise ValueError('done')

        if self.enable_render is True:   ##############
            self.render()

        # choose a random button for env
        env_action = self.action_space.sample()

        while self.maze_view.is_taken(env_action[0:2]):
            print("Button location for env is taken. action was: " + str(env_action))
            env_action = self.action_space.sample()

        print('Environment action is:' + str(env_action))
        self.maze_view.play_env(env_action)

        env_win = self.maze_view.env_horizontal_line() or self.maze_view.env_vertical_line() or self.maze_view.env_diagonal_line()
        agent_win = self.maze_view.agent_horizontal_line() or self.maze_view.agent_vertical_line() or self.maze_view.agent_diagonal_line()

        done = True

        if env_win and agent_win:
            print('Both has won the game. It is a draw!!!')
        elif env_win:
            print('Environment has won the game!!!')
        elif agent_win:
            print('Agent has won the game!!!')
        elif len(self.maze_view.env) + len(self.maze_view.agent) == self.maze_size[0] * self.maze_size[0]:
            print('No one has won the game. It is a draw!!!')
        else:    # continue the game
            done = False

        if done:
            time.sleep(20)
            raise ValueError('done')


        # if np.array_equal(self.maze_view.robot, self.maze_view.goal):
        #     reward = 1
        #     done = True
        # else:
        #     reward = -0.1/(self.maze_size[0]*self.maze_size[1])
        #     done = False

        reward = False
        self.state = (self.maze_view.env, self.maze_view.agent)

        info = {}

        return self.state, reward, done, info

    def reset(self):
        action = self.action_space.sample()
        print('Environment action is (in reset):', str(action))

        self.maze_view.reset_pent(action)

        self.steps_beyond_done = None
        self.done = False
        return True
        # return self.maze_view.env , self.maze_view.agent

    def is_game_over(self):
        return self.maze_view.game_over

    def render(self, mode="human", close=False):
        if close:
            self.maze_view.quit_game()

        # time.sleep(2)
        x = self.maze_view.update(mode)

        return x


