__version__ = 0.251

from rlenvs.river import *
from rlenvs.hunting import *
from rlenvs.texas_holdem_simp import *
from rlenvs.cart_pole_custom import *

from gymnasium import register

register(
    id='custom/CartPole-v1',
    entry_point='rlenvs.cart_pole_custom:CustomCartPoleEnv',
    vector_entry_point="rlenvs.cart_pole_custom:CustomCartPoleVectorEnv",
    max_episode_steps=500,
    reward_threshold=475.0,
)


register(
    id='custom/DiscreteCartPole-v1',
    entry_point='rlenvs.cart_pole_custom:CustomDiscreteCartPoleEnv',
    vector_entry_point="rlenvs.cart_pole_custom:CustomDiscreteCartPoleVectorEnv",
    max_episode_steps=500,
    reward_threshold=475.0,
)
