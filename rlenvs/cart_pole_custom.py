import numpy as np
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



class DiscreteCartPole():
    def __init__(   self, 
                    sizes = (1,20,20,4),
                    steps = (1,2,45,192),
                    scales = (1,.1,.0001,.001),
                    *args,
                    **keyArgs
                ):
        self.sizes = sizes
        self.steps = steps
        self.scales = scales
        self.cart_position_params, self.cart_velocity_params, self.pole_angle_params, self.angular_velocity_params = [
            {"size": size, "step": step, "scale": scale} 
            for size,step,scale in zip(sizes, steps, scales)
        ]

        self.enumerated_state = None

    def discretize(self, state):
        cart_position, cart_velocity, pole_angle, angular_velocity = state
        def func(val, step, size, scale):
            limits = [ i*scale for i in range(-(size-2)//2*step, (size+1)//2*step, step or 1)]
            ids = [i for i,v in enumerate(limits) if val<v]
            return size-1 if len(ids) == 0 else ids[0]
        return (
                func(cart_position, **self.cart_position_params),
                func(cart_velocity, **self.cart_velocity_params),
                func(pole_angle, **self.pole_angle_params),
                func(angular_velocity, **self.angular_velocity_params)
        )
    
    def undiscretize(self, state):
        cart_position, cart_velocity, pole_angle, angular_velocity = state
        def func(val, step, size, scale):
            limits = [ i*scale for i in range(-(size-2)//2*step, (size+1)//2*step, step)]
            return limits[-1] if val >= len(limits) else limits[val]

        return (
                func(cart_position, **self.cart_position_params),
                func(cart_velocity, **self.cart_velocity_params),
                func(pole_angle, **self.pole_angle_params),
                func(angular_velocity, **self.angular_velocity_params)
        )

    def enumerate_state(self, factored_state):
        s = np.meshgrid(*[np.arange(f) for f in self.sizes])
        grid = np.vstack([si.ravel() for si in s])
        return int(np.argwhere([p==factored_state for p in zip(*grid)])[0][0])

    def factor_state(self, enum_state):
        s = np.meshgrid(*[np.arange(f) for f in self.sizes])
        grid = np.vstack([si.ravel() for si in s])
        return tuple(int(i) for i in grid[:,enum_state])

class CustomDiscreteCartPoleEnv(CustomCartPoleEnv, DiscreteCartPole):
    def __init__(self, *args, **keyArgs):
        # super().__init__(*args, **keyArgs)
        CustomCartPoleEnv.__init__(self, *args, **keyArgs)
        DiscreteCartPole.__init__(self, *args, **keyArgs)

    def reset(self, *args, **keyArgs):
        observation, info = CustomCartPoleEnv.reset(self, *args, **keyArgs)
        discrete_observation = self.discretize(observation)
        self.enumerated_state = self.enumerate_state(discrete_observation)
        self.state = np.array(self.undiscretize(discrete_observation))
        return np.array(self.state, dtype=np.float32), info
    
    def step(self, *args, **keyArgs):
        observation, reward, terminated, truncated, info = CustomCartPoleEnv.step(self, *args, **keyArgs)
        discrete_observation = self.discretize(observation)
        self.enumerated_state = self.enumerate_state(discrete_observation)
        self.state = np.array(self.undiscretize(discrete_observation))
        return np.array(self.state, dtype=np.float32), reward, terminated, truncated, info

class CustomDiscreteCartPoleVectorEnv(CustomCartPoleVectorEnv, DiscreteCartPole):
    def __init__(self, *args, **keyArgs):
        # super().__init__(*args, **keyArgs)
        CustomCartPoleVectorEnv.__init__(self, *args, **keyArgs)
        DiscreteCartPole.__init__(self, *args, **keyArgs)

    def reset(self, *args, **keyArgs):
        CustomCartPoleVectorEnv.reset(self, *args, **keyArgs)
        
        observation, info = CustomCartPoleVectorEnv.reset(self, *args, **keyArgs)
        discrete_observation = self.discretize(observation)
        self.enumerated_state = self.enumerate_state(discrete_observation)
        self.state = np.array(self.undiscretize(discrete_observation))
        return np.array(self.state, dtype=np.float32), info
    
    def step(self, *args, **keyArgs):
        observation, reward, terminated, truncated, info = CustomCartPoleVectorEnv.step(self, *args, **keyArgs)
        discrete_observation = self.discretize(observation)
        self.enumerated_state = self.enumerate_state(discrete_observation)
        self.state = np.array(self.undiscretize(discrete_observation))
        return np.array(self.state, dtype=np.float32), reward, terminated, truncated, info


