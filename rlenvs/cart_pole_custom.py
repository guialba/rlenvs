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

    # def reset(  self, 
    #             gravity = 9.8,
    #             masscart = 1.0,
    #             masspole = 0.1,
    #             length = 0.5,
    #             *args,
    #             **keyArgs
    #         ):
    #     ret = super().reset(*args, **keyArgs)

    #     self.gravity = gravity
    #     self.masscart = masscart
    #     self.masspole = masspole
    #     self.length = length

    #     if self.render_mode == "human":
    #         self.render()
    #     return ret
    
    def reset( self, 
                *args,
                **keyArgs
            ):
        ret = super().reset(*args, **keyArgs)
        options =  keyArgs.get('options')
        if options:
            self.gravity = options.get('gravity') or self.gravity
            self.masscart = options.get('masscart') or self.masscart
            self.masspole = options.get('masspole') or self.masspole
            self.length = options.get('length') or self.length

            if self.render_mode == "human":
                self.render()
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
                    # sizes = (1, 15, 15, 15),
                    sizes = (1, 10, 10, 10),
                    # limits = (0, 1.5, .21, 1.5),
                    # smooth_factor = (2, 2, 1, 1.5),
                    gravity = 9.8,
                    masscart = 1.0,
                    masspole = 0.1,
                    length = 0.5, # actually half the pole's length
                    force_mag = 10.0,
                    tau = 0.02, # seconds between state updates
                    *args,
                    **keyArgs
                ):
        self.sizes = sizes
        # self.limits = limits
        # self.smooth_factor = smooth_factor
        self.gravity = gravity
        self.masscart = masscart
        self.masspole = masspole
        self.length = length
        self.force_mag = force_mag
        self.tau = tau

        # self.factor_spaces = [
        #     # np.concatenate([-np.linspace(0, limit**.5, ((size+1)//2))[::-1]**2, np.linspace(0, limit**.5, ((size+1)//2))[1:]**2])
        #     np.concatenate([
        #         -np.linspace(0, limit**(1/smooth_factor[i]), ((size+1)//2))[::-1]**smooth_factor[i], 
        #         np.linspace(0, limit**(1/smooth_factor[i]), ((size+1)//2))[1:]**smooth_factor[i]
        #     ])
        #     # np.linspace(0, (limit[1]*2)**.5, size-1)**2 + limit[0] 
        #     for i, (size,limit) in enumerate(zip(sizes, limits))
        # ]

        self.factor_spaces = [self.get_factor_limits(n,f) for f,n in enumerate(self.sizes)] 
        self.enumerated_state = None

    def apply_step(self, state, action=1):    
        total_mass = self.masspole + self.masscart
        polemass_length = self.masspole * self.length

        x, x_dot, theta, theta_dot = state
        force = self.force_mag if action == 1 else -self.force_mag
        costheta = np.cos(theta)
        sintheta = np.sin(theta)

        temp = (
            force + polemass_length * np.square(theta_dot) * sintheta
        ) / total_mass
        thetaacc = (self.gravity * sintheta - costheta * temp) / (
            self.length
            * (4.0 / 3.0 - self.masspole * np.square(costheta) / total_mass)
        )
        xacc = temp - polemass_length * thetaacc * costheta / total_mass

        x = x + self.tau * x_dot
        x_dot = x_dot + self.tau * xacc
        theta = theta + self.tau * theta_dot
        theta_dot = theta_dot + self.tau * thetaacc

        return np.array((x, x_dot, theta, theta_dot), dtype=np.float32)

    def get_factor_limits(self, n, f):
        s = [0,0,0,0]
        limits = []
        j = ((n-1) if n%2==0 else (n+1))//2
        for _ in range(j):
            s = self.apply_step(s)
            v = round(float(s[f]), 5)
            if v not in limits and n>1 and v!=0:
                limits.append(v)
        space = ([float(i*-1) for i in limits[::-1]]) + ([0] if n%2==0 else [])  + limits
        return space if len(space) == 0 else (space if space[-1]>space[0] else space[::-1])


    def __locate_in_space__(self, factor, value):
        value = round(float(value), 5)
        space = self.factor_spaces[factor]
        idx, val = 0, 0.0
        if len(space)==0: 
            pass
        elif value >= space[-1]: 
            idx = len(space)-1
            val = float(space[-1])
        elif value <= space[0]: 
            val = float(space[0])
        else: 
            tmp = [(i,v) for i,v in enumerate(space) if value<=v][0]
            idx, val = tmp
        return idx, val

    def discretize(self, state):
        ids, values = zip(*[self.__locate_in_space__(f, val) for f, val in enumerate(state)])
        return ids, values

    def enumerate_state(self, state):
        factored_state, _ = self.discretize(state)
        s = np.meshgrid(*[np.arange(f+1) for f in self.sizes])
        grid = np.vstack([si.ravel() for si in s])
        return int(np.argwhere([p==factored_state for p in zip(*grid)])[0][0])

    def factor_state(self, enum_state):
        s = np.meshgrid(*[np.arange(f+1) for f in self.sizes])
        grid = np.vstack([si.ravel() for si in s])
        factored_state = tuple(int(i) for i in grid[:,enum_state])
        return [space[i] for i, space in zip(factored_state, self.factor_spaces)]


# class CustomDiscreteCartPoleEnv(CustomCartPoleEnv, DiscreteCartPole):
class CustomDiscreteCartPoleEnv(CustomCartPoleEnv):
    def __init__(self, *args, **keyArgs):
        super().__init__(*args, **keyArgs)
        # DiscreteCartPole.__init__(self, *args, **keyArgs)
        self.discretizer = DiscreteCartPole(**keyArgs)

    def reset(self, *args, **keyArgs):
        observation, info = super().reset(*args, **keyArgs)
        options =  keyArgs.get('options')
        if options:
            self.discretizer = DiscreteCartPole(**options)

        _, values = self.discretizer.discretize(observation)
        self.enumerated_state = self.discretizer.enumerate_state(observation)
        self.state = np.array(values, dtype=np.float64)
        return np.array(values, dtype=np.float32), info
    
    def step(self, *args, **keyArgs):
        observation, reward, terminated, truncated, info = super().step(*args, **keyArgs)
        _, values = self.discretizer.discretize(observation)
        self.enumerated_state = self.discretizer.enumerate_state(observation)
        self.state = np.array(values, dtype=np.float64)
        return  np.array(values, dtype=np.float32), reward, terminated, truncated, info

# class CustomDiscreteCartPoleVectorEnv(CustomCartPoleVectorEnv, DiscreteCartPole):
class CustomDiscreteCartPoleVectorEnv(CustomCartPoleVectorEnv):
    def __init__(self, *args, **keyArgs):
        # super().__init__(*args, **keyArgs)
        super().__init__(*args, **keyArgs)
        # DiscreteCartPole.__init__(self, *args, **keyArgs)
        self.discretizer = DiscreteCartPole()

    def reset(self, *args, **keyArgs):
        observation, info = super().reset(*args, **keyArgs)
        _, values = self.discretizer.discretize(observation)
        self.enumerated_state = self.discretizer.enumerate_state(observation)
        self.state = np.array(values, dtype=np.float64)
        return np.array(values, dtype=np.float32), info
    
    def step(self, *args, **keyArgs):
        observation, reward, terminated, truncated, info = super().step(*args, **keyArgs)
        _, values = self.discretizer.discretize(observation)
        self.enumerated_state = self.discretizer.enumerate_state(observation)
        self.state = np.array(values, dtype=np.float64)
        return np.array(values, dtype=np.float32), reward, terminated, truncated, info


