'''
A Recurrent Neural Network (LSTM) implementation example using TensorFlow library.
This example is using the MNIST database of handwritten digits (http://yann.lecun.com/exdb/mnist/)
Long Short Term Memory paper: http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf

Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

from __future__ import print_function

import tensorflow as tf
from tensorflow.python.ops import rnn_cell, seq2seq, rnn
from tensorflow.python.ops.control_flow_ops import cond
from mgcdataset import MGCDataset
import matplotlib.pyplot as plt
import tensorflow.contrib.layers as tf_layers
import sys
import os
import math
import numpy as np

def plot_func(funcs):
    colors = ['red', 'cyan', 'green', 'orange']
    for i, points in enumerate(funcs):
        points = np.transpose(points)
        plt.scatter(points[0, :], points[1,:], c=colors[i])
    plt.show()

class FuncDataset:

    def __init__(self, func, len, bs, lower=0, upper=30):
        self.bs = bs
        self.current = 0
        self.X = np.linspace(lower, upper, num=len)
        values = [func(x) for x in self.X]
        self.Y = np.append(self.X, values, axis=0).reshape((2, len)).transpose()

    def next(self):
        return ([self.X], [self.Y])
        # return (self.X[self.current:self.current+batch_size], self.Y[:,self.current:self.current+batch_size])

def arb(x):
    # return math.sin(x)*x + np.random.random()
    # return math.tanh(x)
    return x*x*x*x

# plot_func([fsin.Y, fcos.Y])
# Parameters
learning_rate = 0.01
training_iters = 1000
batch_size = 1
display_step = 1
dataset_dump = "dataset.bin"
# Network Parameters
n_coeffs = 2 # MNIST data input (img shape: 28*28)
n_steps = 200 # timesteps
n_hidden = 64 # hidden layer num of features

# Required shape: 'n_steps' tensors list of shape (batch_size, n_input)
graph= tf.get_default_graph()
graph.seed=42

fsin = FuncDataset(math.sin, n_steps, 1)
fcos = FuncDataset(math.cos, n_steps, 1)
farb = FuncDataset(arb, n_steps, 1)
# # tf Graph input
x = tf.placeholder("float", [None, n_steps])
y = tf.placeholder("float", [None, n_steps, n_coeffs])

# Define weights
weights = {
    'out': tf.Variable(tf.random_normal([n_hidden, n_coeffs]))
}
biases = {
    'out': tf.Variable(tf.random_normal([n_coeffs]))
}


# Prepare data shape to match `rnn` function requirements
# Current data input shape: (batch_size, n_steps, n_input)

# Permuting batch_size and n_steps
xx = tf.transpose(x, [1, 0])
print(xx.get_shape())
# # Reshaping to (n_steps*batch_size, n_input)
xx = tf.reshape(xx, [-1, 1])
# print(xx.get_shape())
# # Split to get a list of 'n_steps' tensors of shape (batch_size, n_input)
xx = tf.split(0, n_steps, xx)
#
# print("XX", len(xx), xx[0].get_shape())
#
yy = tf.transpose(y, [1, 0, 2])
# Reshaping to (n_steps*batch_size, n_input)
yy = tf.reshape(yy, [-1, n_coeffs])
# Split to get a list of 'n_steps' tensors of shape (batch_size, n_input)
yy = tf.split(0, n_steps, yy)
# /
# gru_cell = rnn_cell.GRUCell(n_hidden)
#
# # Define a lstm cell with tensorflow
lstm_cell = rnn_cell.BasicLSTMCell(n_hidden)
# # gru_cell = rnn_cell.GRUCell(100)
# # Get lstm cell output
outputs, states = rnn.rnn(lstm_cell, xx, dtype=tf.float32)

# dec_inp = ([tf.zeros_like(x[0], dtype=np.float32, name="GO")]
#            + xx[:-1])

# outputs, states = seq2seq.rnn_decoder(xx, gru_cell.zero_state(batch_size, dtype="float32"), gru_cell)

# print("LO", len(outputs))
pred = [tf.matmul(o, weights["out"]) + biases["out"] for o in outputs]
# print(len(pred), pred[0].get_shape())
# print(len(yy), yy[0].get_shape())
# print(states[0].get_shape())

# Define loss and optimizer
cost = tf.sqrt(tf.reduce_mean(tf.square(tf.sub(pred, yy))))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
# print("Graph Initialized")

# Evaluate model
rmse = tf.sqrt(tf.reduce_mean(tf.square(tf.sub(pred, yy))))
# Initializing the variables
init = tf.initialize_all_variables()
# if os.path.exists(dataset_dump):
#     with open(dataset_dump, "rb") as f:
#         dataset = pickle.load(f)
# else:
#     dataset = MGCDataset("synthesized-mgc", "natural-mgc")
#     with open(dataset_dump, "wb") as f:
#         pickle.dump(dataset, f)
#
# print("Data loaded.")
# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    step = 1
    # Keep training until reach max iterations
    while step < training_iters:
        batch_x, batch_y = farb.next()
        # Reshape data to get 28 seq of 28 elements
        # batch_x = batch_x.reshape((batch_size, n_steps, n_input))
        # Run optimization op (backprop)
        # sess.run(optimizer, feed_dict={x: batch_x, y: batch_y})
        sess.run(optimizer, feed_dict={x: batch_x, y: batch_y})
        print(step)
        if step % display_step == 0:
            # Calculate batch accuracy
            mse = sess.run(rmse, feed_dict={x: batch_x, y: batch_y})
            # Calculate batch loss
            loss = sess.run(cost, feed_dict={x: batch_x, y: batch_y})
            print("Iter " + str(step*batch_size) + ", Minibatch Loss= " + \
                  "{:.6f}".format(loss) + ", Training RMSE= " + \
                  "{:.5f}".format(mse))
        step += 1
    print("Optimization Finished!")

    test_x, test_y = farb.next()
    # Calculate accuracy for 128 mnist test images
    test_rmse, test_out = sess.run([rmse, pred], feed_dict={x: test_x, y: test_y})
    print("Testing RMSE :", test_rmse)

    plot_func([farb.Y, np.array(test_out)])