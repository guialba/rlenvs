import gymnasium as gym
import rlenvs

n=500

# env = gym.make("CartPole-v1", render_mode="human")
# env = gym.make("custom/CartPole-v1", render_mode="human")
env = gym.make("custom/DiscreteCartPole-v1", render_mode="human")

# observation, info = env.reset(seed=82, masspole=.45, length=1.0)
observation, info = env.reset(seed=82, options={'masspole':.45, 'length':1.0, "sizes":(1, 20, 20, 20)})
hist_s = [observation]
hist_a = []
for _ in range(n):
    # action = env.action_space.sample()
    # action = 1
    print("observation : ",observation);
    action = int(input())-1
    if not(action in [0,1]):
        break
    # print('action: ', action)
    observation,reward, terminated, truncated, info = env.step(action)
    # print("observation : ",observation);
    print(reward, terminated, truncated);
    
    hist_s.append(observation)
    hist_a.append(action)


    if terminated or truncated:
        break
        # observation, info = env.reset()
        
env.close()

print([{'s': s, "a": a} for s,a in zip(hist_s, hist_a)])