'''
A Recurrent Neural Network (LSTM) implementation example using TensorFlow library.
This example is using the MNIST database of handwritten digits (http://yann.lecun.com/exdb/mnist/)
Long Short Term Memory paper: http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf

Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

from __future__ import print_function

import tensorflow as tf
from tensorflow.python.ops import rnn_cell, seq2seq
from tensorflow.python.ops.control_flow_ops import cond
from mgcdataset import MGCDataset
import pickle
import os
import numpy as np



# Parameters
learning_rate = 0.001
training_iters = 5000
batch_size = 64
display_step = 1
dataset_dump = "dataset.bin"
# Network Parameters
n_coeffs = 35 # MNIST data input (img shape: 28*28)
n_steps = 1100 # timesteps
n_hidden = 128 # hidden layer num of features

# tf Graph input
x = tf.placeholder("float", [None, n_steps, n_coeffs])
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
# Required shape: 'n_steps' tensors list of shape (batch_size, n_input)

# Permuting batch_size and n_steps
xx = tf.transpose(x, [1, 0, 2])
# Reshaping to (n_steps*batch_size, n_input)
xx = tf.reshape(xx, [-1, n_coeffs])
# Split to get a list of 'n_steps' tensors of shape (batch_size, n_input)
xx = tf.split(0, n_steps, xx)


yy = tf.transpose(y, [1, 0, 2])
# Reshaping to (n_steps*batch_size, n_input)
yy = tf.reshape(yy, [-1, n_coeffs])
# Split to get a list of 'n_steps' tensors of shape (batch_size, n_input)
yy = tf.split(0, n_steps, yy)

gru_cell = rnn_cell.GRUCell(n_hidden)
dec_inp = ([tf.zeros_like(x[0], dtype=np.float32, name="GO")]
           + xx[:-1])

# is_first = tf.placeholder(tf.bool)
# state_before = tf.get_variable('state_before',
#                                initializer=tf.zeros([batch_size, n_hidden], dtype='float32'),
#                                trainable=False)
# before_state_bh = cond(is_first,
#                            lambda: gru_cell.zero_state(batch_size, dtype='float32'),
#                            lambda: state_before)
# Initial memory value for recurrence.
outputs, states = seq2seq.rnn_decoder(xx, gru_cell.zero_state(batch_size, dtype="float32"), gru_cell)

pred = [tf.matmul(o, weights["out"]) + biases["out"] for o in outputs]
print(pred[0].get_shape())
print(states[0].get_shape())

# Define loss and optimizer
cost = tf.sqrt(tf.reduce_mean(tf.square(tf.sub(pred, yy))))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
print("Graph Initialized")

# Evaluate model
rmse = tf.sqrt(tf.reduce_mean(tf.square(tf.sub(pred, yy))))
# Initializing the variables
init = tf.initialize_all_variables()
if os.path.exists(dataset_dump):
    with open(dataset_dump, "rb") as f:
        dataset = pickle.load(f)
else:
    dataset = MGCDataset("synthesized-mgc", "natural-mgc")
    with open(dataset_dump, "wb") as f:
        pickle.dump(dataset, f)

print("Data loaded.")
# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    step = 1
    # Keep training until reach max iterations
    while step * batch_size < training_iters:
        batch_x, batch_y = dataset.next_batch()
        # Reshape data to get 28 seq of 28 elements
        # batch_x = batch_x.reshape((batch_size, n_steps, n_input))
        # Run optimization op (backprop)
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

    test_x, test_y = dataset.get_test()
    # Calculate accuracy for 128 mnist test images
    print("Testing RMSE :",
        sess.run(rmse, feed_dict={x: test_x, y: test_y}))

