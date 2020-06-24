import gym
import matplotlib.pyplot as plt
from memory_replay import ReplayMemory, Transition
import random
import tensorflow as tf
import numpy as np
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('--s', type=int, default=1, help='Random seed')
parser.add_argument('--e', action="store_true", default=False, help='Run in eval mode')
parser.add_argument('--ep',type=int,default=455,help='Number of Training Episodes')
parser.add_argument('--avg_over', type=int, default=100, help='Number of previous episodes of training to find the average reward.')
args = parser.parse_args()

np.random.seed(args.seed)
random.seed(args.seed)


class DQN(object):
    
    def __init__(self, env):

        self.env = env
        self.sess = tf.Session()

        
        self.batch_len = 32
        self.gamma = 0.99
        self.alpha = 0.0005
        self.memory_cap = 10000
        
        self.epsilon_start = 0.99
        self.eps= self.epsilon_start
        
        self.clone_stps = 500
        self.inp_size = env.observation_space.shape[0]
        
        self.replay_memory = ReplayMemory(100000)
        
        self.min_replay_size = 10000
        self.memory = np.zeros((self.memory_cap, self.inp_size * 2 + 2))
        self.actions = env.action_space.n

        
        self.observation_input = tf.placeholder(tf.float32, [None, self.inp_size])
        self.observation_input_target = tf.placeholder(tf.float32, [None, self.inp_size])
        self.q_target = tf.placeholder(tf.float32, [None, self.actions], name='Q_target')  
        self.train_network = self.build_model(self.observation_input)
        self.target_network = self.build_model(self.observation_input_target,'target')

        t_params = tf.get_collection('target_params')
        e_params = tf.get_collection('train_params')
        self.replace_target_op = [tf.assign(t, e) for t, e in zip(t_params, e_params)]

        
        self.loss = tf.reduce_mean(tf.losses.huber_loss(self.q_target, self.train_network))
        self.reducer = tf.train.AdamOptimizer(self.alpha).minimize(self.loss)


        self.num_episodes = 0
        self.num_steps = 0
        self.cost_his = []

        self.saver = tf.train.Saver(tf.trainable_variables())
        self.sess.run(tf.global_variables_initializer())

    def build_model(self, observation_input, scope='train'):
        
        with tf.variable_scope(scope):
            namespace, layer1_nodes, layer2_nodes, weights, biases = [scope+'_params', tf.GraphKeys.GLOBAL_VARIABLES], 50, 40, \
            tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)  

            
            w1 = tf.get_variable('w1', [self.inp_size, layer1_nodes], initializer=weights, collections=namespace)
            b1 = tf.get_variable('b1', [1, layer1_nodes], initializer=biases, collections=namespace)
            l1 = tf.nn.relu(tf.matmul(observation_input, w1) + b1)

            
            w2 = tf.get_variable('w2', [layer1_nodes, layer1_nodes], initializer=weights, collections=namespace)
            b2 = tf.get_variable('b2', [1, layer1_nodes], initializer=biases, collections=namespace)
            l2 = tf.nn.relu(tf.matmul(l1, w2) + b2)

            
            w3 = tf.get_variable('w3', [layer1_nodes, self.actions], initializer=weights, collections=namespace)
            b3 = tf.get_variable('b3', [1, self.actions], initializer=biases, collections=namespace)
        return tf.matmul(l2, w3) + b3


    def select_action(self, obs, evaluation_mode=False):
        
        if np.random.uniform() > self.epsilon_start or evaluation_mode:
            
            actions_value = self.sess.run(self.train_network, feed_dict={self.observation_input: obs[np.newaxis, :]})
            action = np.argmax(actions_value)
        else:
            action = np.random.randint(0, self.actions)


        return action

    def update(self):
        
        if self.num_steps % self.clone_stps == 0:
            self.sess.run(self.replace_target_op)

        if self.num_steps > self.memory_cap:
            sample_index = np.random.choice(self.memory_cap, size=self.batch_len)
        else:
            sample_index = np.random.choice(self.num_steps, size=self.batch_len)
        batch_data = self.memory[sample_index, :]

        target_q, train_q = self.sess.run(
            [self.target_network, self.train_network],
            feed_dict={
                self.observation_input_target: batch_data[:, -self.inp_size:],  
                self.observation_input: batch_data[:, :self.inp_size],  
            })

        target_network = train_q.copy()

        i_train = batch_data[:, self.inp_size].astype(int)
        reward = batch_data[:, self.inp_size + 1]

        target_network[np.arange(self.batch_len, dtype=np.int32), i_train] = reward + self.gamma * np.max(target_q, axis=1)

        _,cost = self.sess.run([self.reducer, self.loss],
                      feed_dict={self.observation_input: batch_data[:, :self.inp_size],
                                 self.q_target: target_network})
        self.cost_his.append(cost)

    def train(self):
        
        done = False
        obs = env.reset()
        total_reward = 0.0
        while not done:
            action = self.select_action(obs, evaluation_mode=False)
            next_obs, reward, done, info = env.step(action)

            self.memory[self.num_steps % self.memory_cap, :] = np.hstack((obs, [action, reward], next_obs))

            if(self.num_steps>5000):
                self.update()

            total_reward += reward

            obs = next_obs
            self.num_steps += 1
        print("Training Episode #", self.num_episodes, " with reward: ", total_reward, " and eps = ", self.epsilon_start)
        self.epsilon_start -= .002
        self.num_episodes += 1
        return total_reward

    def eval_avg100(self, save_snapshot=False):
        total_reward = 0.0
        reward_list = []
        for i in range(100):
            ep_steps = 0
            done = False
            obs = env.reset()
            rew = 0
            while not done: 
                action = self.select_action(obs, evaluation_mode=True)
                obs, reward, done, info = env.step(action)
                total_reward += reward
                rew +=reward
            reward_list.append(rew)
            print('Episode',i,'reward:',rew)
        print ("Evaluation episode: ", total_reward/100)
        plt.plot(np.arange(len(reward_list)),reward_list, label='Actual Reward')
        plt.plot(np.arange(len(reward_list)),np.ones((len(reward_list),))*total_reward/100,label='Average Reward')
        plt.ylabel('Reward')
        plt.title('Evaluating the trained model')
        plt.xlabel('Episodes')
        plt.legend()
        plt.show()
        if save_snapshot:
            print ("Saving state with Saver")
            self.saver.save(self.sess, 'models/dqn-model', dqn.num_episodes)

    def eval(self, save_snapshot=False):
        
        total_reward = 0.0
        ep_steps = 0
        done = False
        obs = env.reset()
        while not done:
            env.render()
            action = self.select_action(obs, evaluation_mode=True)
            obs, reward, done, info = env.step(action)
            total_reward += reward
        print ("Evaluation episode: ", total_reward)
        if save_snapshot:
            print ("Saving state with Saver")
            self.saver.save(self.sess, 'models/dqn-model', dqn.num_episodes)



def eval(dqn):
    
    ckpt_file = os.path.join(os.path.dirname(__file__), 'models/checkpoint')
    with open(ckpt_file, 'r') as f:
        first_line = f.readline()
        model_name = first_line.split()[-1].strip("\"")
    dqn.saver.restore(dqn.sess, os.path.join(os.path.dirname(__file__), 'models/'+model_name))
    dqn.eval_avg100(save_snapshot=False)

    

def train(dqn):
    episode_history = []
    for i in range(1,args.episodes):
        curr = dqn.train()
        env.render()
        episode_history.append(curr)
    plot_cost(episode_history)
    print("Saving state with Saver")
    dqn.saver.save(dqn.sess, 'models/dqn-model', dqn.num_episodes)

def plot_cost(episode_list):
    print(np.average(episode_list[:-args.avg_over]))
    plt.plot(np.arange(len(episode_list)), episode_list)
    plt.ylabel('Cost')
    plt.title('Training reward with alpha=0.0005, gamma = 0.99')
    plt.xlabel('Training steps')
    plt.show()


if __name__ == '__main__':
    
    env = gym.make('LunarLander-v2')
    env.seed(args.seed)

    dqn = DQN(env)
    if args.eval:
        eval(dqn)
    else:
        train(dqn)
