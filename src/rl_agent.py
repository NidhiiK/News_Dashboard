import numpy as np

class QLAgent:
    def __init__(self, num_states, num_actions, learning_rate=0.1, discount=0.9):
        self.q_table = np.zeros((num_states, num_actions))  # States: topics, Actions: promote/demote
        self.lr = learning_rate
        self.discount = discount

    def choose_action(self, state, epsilon=0.1):
        if np.random.random() < epsilon:
            return np.random.randint(self.q_table.shape[1])  # Explore
        return np.argmax(self.q_table[state])  # Exploit

    def update(self, state, action, reward, next_state):
        current_q = self.q_table[state, action]
        next_max_q = np.max(self.q_table[next_state])
        self.q_table[state, action] = current_q + self.lr * (reward + self.discount * next_max_q - current_q)

if __name__ == "__main__":
    agent = QLAgent(3, 2)  # 3 topics, 2 actions (promote/demote)
    print("Initial Q-table:", agent.q_table)