import numpy as np
from reinforcement_learning_framework import ActorCriticAgent
from noc_simulator import NOCSimulator  # Assuming NOCSimulator is the simulator for network-on-chip environment

# Pseudocode to measure average latency and bandwidth
def measure_latency_and_bandwidth(interface_monitor_output):
    read_latency_sum, write_latency_sum, total_reads, total_writes = 0, 0, 0, 0
    bandwidth_sum, total_transactions = 0, 0
    last_read_timestamp, last_write_timestamp = -1, -1

    for entry in interface_monitor_output:
        txn_type = entry['TxnType']
        current_timestamp = entry['Timestamp']
        data_size = entry['DataSize']

        if txn_type == 'Read':
            if last_read_timestamp != -1:
                read_latency_sum += current_timestamp - last_read_timestamp
                total_reads += 1
            last_read_timestamp = current_timestamp
        elif txn_type == 'Write':
            if last_write_timestamp != -1:
                write_latency_sum += current_timestamp - last_write_timestamp
                total_writes += 1
            last_write_timestamp = current_timestamp
        bandwidth_sum += data_size
        total_transactions += 1

    average_read_latency = read_latency_sum / max(1, total_reads)
    average_write_latency = write_latency_sum / max(1, total_writes)
    average_bandwidth = bandwidth_sum / max(1, total_transactions)

    return average_read_latency, average_write_latency, average_bandwidth


# Reinforcement Learning Framework
class OptiNoCRL:
    def __init__(self, state_size, action_size):
        self.agent = ActorCriticAgent(state_size=state_size, action_size=action_size)

    def train(self, total_episodes, env):
        for episode in range(total_episodes):
            state = env.reset()
            done = False
            while not done:
                action = self.agent.act(state)
                next_state, reward, done = env.step(action)
                self.agent.learn(state, action, reward, next_state, done)
                state = next_state

        self.agent.save('optinoc_actor_critic_model.h5')


# Main function
def main():
    # Initialize the simulation environment
    env = NOCSimulator()

    # Measure latency and bandwidth
    interface_monitor_output = env.get_interface_monitor_output()
    average_read_latency, average_write_latency, average_bandwidth = measure_latency_and_bandwidth(interface_monitor_output)
    print(f"Average Read Latency: {average_read_latency}")
    print(f"Average Write Latency: {average_write_latency}")
    print(f"Average Bandwidth: {average_bandwidth}")

    # Initialize the RL agent and train
    rl_agent = OptiNoCRL(state_size=env.state_size, action_size=env.action_size)
    total_episodes = 1000  # Define the total number of training episodes
    rl_agent.train(total_episodes, env)


if __name__ == "__main__":
    main()
