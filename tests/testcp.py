import gymnasium as gym
import rlenvs

n=500

# env = gym.make("CartPole-v1", render_mode="human")
env = gym.make("custom/CartPole-v1", render_mode="human")
env.action_space.seed(82)

observation, info = env.reset(seed=82, masspole=1.45, length=1.0)

for _ in range(n):
    # action = env.action_space.sample()
    # action = 1
    action = int(input())
    print('action: ', action)
    observation,reward, terminated, truncated, info = env.step(action)
    print("info : ",info);
    
    if terminated or truncated:
        break
        # observation, info = env.reset()
        
env.close()