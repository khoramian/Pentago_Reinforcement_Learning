import sys
from pentago_env import PentagoEnv

if __name__ == "__main__":

    env = PentagoEnv(maze_size=(6, 6), enable_render=True)

    env.render()

    for i in range(20):

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