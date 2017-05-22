'''
A linear regression learning algorithm example using TensorFlow library.

Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

import tensorflow as tf
import argparse
from dataset import Dataset, Utterance
import tensorflow.contrib.layers as tf_layers


ap = argparse.ArgumentParser()
ap.add_argument("-l", type=int)
ap.add_argument("-s", type=int)
ap.add_argument("-e", type=int)
ap.add_argument("--include_gold", action="store_true")
args = ap.parse_args()
no_classes = 4
d = Dataset(length=args.s, dataset_path="dataset.dump")
d.load_data(size=no_classes, include_gold=args.include_gold)
# Parameters
learning_rate = 0.01
training_epochs = args.e
display_step = 2
input_size = d.data_X.shape[1]
batch_size = 8
print(d.data_X.shape)
# batch x frames x order x engines
X = tf.placeholder("float", [None, input_size])
Y = tf.placeholder(tf.int64, [None])

# Set model weights
l1_size = args.l
# W1 = tf.Variable(initial_value=tf.random_uniform([input_size, l1_size], 0, 1), name="weights1", trainable=True)
# b1 = tf.Variable(initial_value=tf.random_uniform([l1_size], 0, 1), name="bias1", trainable=True)
# W2 = tf.Variable(initial_value=tf.random_uniform([100, no_classes], 0, 1), name="weights2", trainable=True)
# b2 = tf.Variable(initial_value=tf.random_uniform([no_classes], 0, 1), name="bias2", trainable=True)


l1 = tf.sigmoid(tf_layers.linear(X, l1_size))
logits = tf_layers.linear(l1, no_classes)
# softmax = tf.nn.softmax(logits)
pred = tf.argmax(logits, axis=1)
# Mean squared error
cost = tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(labels=tf.one_hot(Y, no_classes), logits=logits))

# Gradient descent
optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

# Initializing the variables
init = tf.global_variables_initializer()

# Launch the graph
with tf.Session() as sess:
    sess.run(init)

    # Fit all training data
    # train_X, train_Y = d.get_data()
    for epoch in range(training_epochs):
        for x, y in d.next_batch():
            sess.run([optimizer, cost], feed_dict={X: x, Y: y})
            if d.batch_end():
                break
        # Display logs per epoch step
        if (epoch+1) % display_step == 0:
            predictions, c = sess.run([pred, cost], feed_dict={X: x, Y:y})
            print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(c), "pred=", predictions)

        valid_X, valid_Y = d.get_valid()
        train_X, train_Y = d.get_train()
        predictions, c = sess.run([pred, cost], feed_dict={X: valid_X, Y: valid_Y})
        print("Cost: {}, predictions: {}".format(c, predictions))
        diff = abs((valid_Y - predictions) != 0)
        print("Valid: ", 1 - ((sum(diff)) / len(diff)))
        predictions, c = sess.run([pred, cost], feed_dict={X: train_X, Y: train_Y})
        print("Cost: {}, predictions: {}".format(c, predictions))
        diff = abs((train_Y - predictions) != 0)
        print("Train: ", 1 - ((sum(diff)) / len(diff)))
    print("Optimization Finished!")
    #
    # # Graphic display
    # plt.plot(train_X, train_Y, 'ro', label='Original data')
    # plt.plot(train_X, sess.run(W) * train_X + sess.run(b), label='Fitted line')
    # plt.legend()
    # plt.show()
