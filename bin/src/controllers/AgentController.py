import numpy as np

class Agent:

    def __init__(self):
        self.action_space = np.array([0,1,2]) # 0: move left, 1: move right, 2: rotate
        self.observation_space = ... # FIXME: Implement the observation space.
        self.state = ... # FIXME: State not implemented
        # self.memory = np.array([[0,0,0]]) TODO: Might be important later.

    def step(self, action) -> tuple:
        """
        Proceeds the action chosen by the agent.

        Parameters
        -
        action: int -> random value of self.action_space

        Returns
        -
        step: tuple -> (action, reward, state)
        """
        pass # TODO: Implement what the agent does and calculate the reward

    def reset(self) -> None:
        """
        Resets the environment to the default settings.

        Returns
        -
        None
        """
        pass # TODO: Implement the reset of the state and reset the rewards

agent = Agent()