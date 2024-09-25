__version__ = 0.1

from rlenvs.river import *
from rlenvs.hunting import *
from rlenvs.texas_holdem_simp import *
from rlenvs.cart_pole_custom import *

from gymnasium.envs.registration import register

register(
    id='custom/CartPole-v1',
    entry_point='rlenvs.cart_pole_custom:CustomCartPoleEnv',
    vector_entry_point="rlenvs.cart_pole_custom:CustomCartPoleVectorEnv",
    max_episode_steps=500,
    reward_threshold=475.0,
)
