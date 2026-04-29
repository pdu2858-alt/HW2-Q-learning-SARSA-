import numpy as np
import matplotlib.pyplot as plt
from cliff_walking import CliffWalkingEnv
from agents import QLearningAgent, SarsaAgent

def train_q_learning(episodes=500):
    env = CliffWalkingEnv()
    agent = QLearningAgent(env)
    rewards = []
    
    for ep in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.update(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            
        rewards.append(total_reward)
    return agent, rewards

def train_sarsa(episodes=500):
    env = CliffWalkingEnv()
    agent = SarsaAgent(env)
    rewards = []
    
    for ep in range(episodes):
        state = env.reset()
        action = agent.choose_action(state)
        total_reward = 0
        done = False
        
        while not done:
            next_state, reward, done = env.step(action)
            next_action = agent.choose_action(next_state)
            agent.update(state, action, reward, next_state, next_action, done)
            state = next_state
            action = next_action
            total_reward += reward
            
        rewards.append(total_reward)
    return agent, rewards

def smooth_rewards(rewards, window=10):
    smoothed = np.zeros_like(rewards, dtype=float)
    for i in range(len(rewards)):
        smoothed[i] = np.mean(rewards[max(0, i-window+1):i+1])
    return smoothed

def get_optimal_path(env, agent):
    path = np.full((env.height, env.width), ' ')
    state = env.reset()
    
    action_symbols = ['U', 'R', 'D', 'L']
    for r in range(env.height):
        for c in range(env.width):
            if (r, c) == env.goal_state:
                path[r, c] = 'G'
            elif (r, c) in env.cliff:
                path[r, c] = 'C'
            else:
                best_action = np.argmax(agent.Q[r, c, :])
                path[r, c] = action_symbols[best_action]
                
    state = env.reset()
    actual_path = [state]
    steps = 0
    while state != env.goal_state and steps < 100:
        r, c = state
        action = np.argmax(agent.Q[r, c, :])
        state, _, _ = env.step(action)
        actual_path.append(state)
        if state in env.cliff:
            break
        steps += 1
        
    return path, actual_path

def visualize_path(env, q_path, q_actual, sarsa_path, sarsa_actual):
    fig, axes = plt.subplots(2, 1, figsize=(12, 6))
    
    for i, (name, path, actual) in enumerate([("Q-learning (Off-policy)", q_path, q_actual), 
                                              ("SARSA (On-policy)", sarsa_path, sarsa_actual)]):
        ax = axes[i]
        ax.set_title(f"{name} Optimal Policy")
        ax.set_xlim(0, env.width)
        ax.set_ylim(0, env.height)
        ax.set_xticks(np.arange(env.width+1)-0.5, minor=True)
        ax.set_yticks(np.arange(env.height+1)-0.5, minor=True)
        ax.grid(which="minor", color="black", linestyle='-', linewidth=1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.invert_yaxis()
        
        for r in range(env.height):
            for c in range(env.width):
                if (r, c) == env.start_state:
                    ax.add_patch(plt.Rectangle((c-0.5, r-0.5), 1, 1, fill=True, color='green', alpha=0.3))
                    ax.text(c, r, 'S', ha='center', va='center', fontsize=12, fontweight='bold')
                elif (r, c) == env.goal_state:
                    ax.add_patch(plt.Rectangle((c-0.5, r-0.5), 1, 1, fill=True, color='blue', alpha=0.3))
                    ax.text(c, r, 'G', ha='center', va='center', fontsize=12, fontweight='bold')
                elif (r, c) in env.cliff:
                    ax.add_patch(plt.Rectangle((c-0.5, r-0.5), 1, 1, fill=True, color='gray', alpha=0.3))
                    ax.text(c, r, 'C', ha='center', va='center', fontsize=12)
                else:
                    arrow = path[r, c]
                    symbol = {'U': '↑', 'R': '→', 'D': '↓', 'L': '←'}.get(arrow, arrow)
                    ax.text(c, r, symbol, ha='center', va='center', fontsize=16)
        
        # Draw actual path
        for j in range(len(actual)-1):
            r1, c1 = actual[j]
            r2, c2 = actual[j+1]
            if (r2, c2) in env.cliff: continue
            ax.plot([c1, c2], [r1, r2], color='red', linewidth=3, alpha=0.5)

    plt.tight_layout()
    plt.savefig('path_visualization.png')
    plt.close()

if __name__ == "__main__":
    episodes = 500
    print("Training Q-learning...")
    np.random.seed(42)
    q_agent, q_rewards = train_q_learning(episodes)
    
    print("Training SARSA...")
    np.random.seed(42)
    sarsa_agent, sarsa_rewards = train_sarsa(episodes)
    
    print("Generating Reward Curve...")
    plt.figure(figsize=(10, 5))
    plt.plot(smooth_rewards(q_rewards, window=20), label='Q-learning', alpha=0.8)
    plt.plot(smooth_rewards(sarsa_rewards, window=20), label='SARSA', alpha=0.8)
    plt.xlabel('Episodes')
    plt.ylabel('Sum of rewards during episode (Smoothed over 20 eps)')
    plt.title('Performance on Cliff Walking')
    plt.legend()
    plt.ylim(-200, 0)
    plt.grid()
    plt.savefig('reward_curve.png')
    plt.close()
    
    print("Generating Path Visualization...")
    env = CliffWalkingEnv()
    q_path, q_actual = get_optimal_path(env, q_agent)
    sarsa_path, sarsa_actual = get_optimal_path(env, sarsa_agent)
    visualize_path(env, q_path, q_actual, sarsa_path, sarsa_actual)
    print("Done!")
