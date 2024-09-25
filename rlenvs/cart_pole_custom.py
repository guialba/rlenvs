import gymnasium as gym
from gymnasium.envs.classic_control.cartpole import CartPoleEnv, CartPoleVectorEnv

class CustomCartPoleEnv(CartPoleEnv):
    def __init__(   self, 
                    gravity = 9.8,
                    masscart = 1.0,
                    masspole = 0.1,
                    length = 0.5,
                    *args,
                    **keyArgs
                ):
        super().__init__(*args, **keyArgs)

        self.gravity = gravity
        self.masscart = masscart
        self.masspole = masspole
        self.length = length

    def reset(  self, 
                gravity = 9.8,
                masscart = 1.0,
                masspole = 0.1,
                length = 0.5,
                *args,
                **keyArgs
            ):
        ret = super().reset(*args, **keyArgs)

        self.gravity = gravity
        self.masscart = masscart
        self.masspole = masspole
        self.length = length

        return ret

class CustomCartPoleVectorEnv(CartPoleVectorEnv):
    def __init__(   self, 
                    gravity = 9.8,
                    masscart = 1.0,
                    masspole = 0.1,
                    length = 0.5,
                    *args,
                    **keyArgs
                ):
        super().__init__(*args, **keyArgs)

        self.gravity = gravity
        self.masscart = masscart
        self.masspole = masspole
        self.length = length

    def reset(  self, 
                gravity = 9.8,
                masscart = 1.0,
                masspole = 0.1,
                length = 0.5,
                *args,
                **keyArgs
            ):
        ret = super().reset(*args, **keyArgs)

        self.gravity = gravity
        self.masscart = masscart
        self.masspole = masspole
        self.length = length

        return ret


