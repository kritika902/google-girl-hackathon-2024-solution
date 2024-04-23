import numpy as np
from reinforcement_learning_framework import ActorCriticAgent
from noc_simulator import NOCSimulator  # Assuming NOCSimulator is the simulator for network-on-chip environment

def train_rl_agent(env, agent, total_episodes):
    for episode in range(total_episodes):
        state = env.reset()
        agent.reset()

        while True:
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            agent.learn(state, action, reward, next_state, done)
            state = next_state
            if done:
                break

def main():
    # Initialize the simulation environment
    env = NOCSimulator()

    # Initialize the RL agent with optimized memory usage
    agent = ActorCriticAgent(state_size=env.state_size, action_size=env.action_size, memory_efficient=True)

    # Train the RL agent
    total_episodes = 1000  
    train_rl_agent(env, agent, total_episodes)

    # Save the trained model
    agent.save('optinoc_actor_critic_model.h5')

if __name__ == "__main__":
    main()
