import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
import matplotlib.pyplot as plt


kpi = 0
keep_probability = [0.1, 0.25, 0.5, 0.75, 1.0]
# Toggle btwn dropout and dropConnect
dc = False
_lambda = 0.0001
# ==================================================================
#

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def dropout(h):
    if not dc:
        d = np.random.binomial([np.ones((h.get_shape()[1]))], keep_probability[kpi])[0] #* (1.0/(keep_probability[kpi]))
        return tf.mul(h, d)
    return h

def dropconnect(w):
    if dc:
        d = np.random.binomial([np.ones((w.get_shape()))], keep_probability[kpi])[0]
        # return tf.mul(w, d)
        return w * d
    return w

def sum_weights(w1,w2,w3,b1,b2,b3):
    sw = [w1,w2,w3,b1,b2,b3]
    t = 0
    for x in sw:
        t += tf.reduce_sum(tf.abs(x))
    return t

#
# ==================================================================
#

# Declare computation graph

y_ = tf.placeholder(tf.float32, shape=[None, 10], name="y_")
x = tf.placeholder(tf.float32, [None, 784], name="x")

W1 = weight_variable([784, 500])
# W1 = dropconnect(W1)
b1 = bias_variable([500])
h1 = tf.nn.relu(tf.matmul(x, dropconnect(W1)) + b1)

# Drop
h1 = dropout(h1)

W2 = weight_variable([500, 500])
# W2 = dropconnect(W2)
b2 = bias_variable([500])
h2 = tf.nn.relu(tf.matmul(h1, dropconnect(W2)) + b2)

# Drop
h2 = dropout(h2)

W3 = weight_variable([500, 1000])
# W3 = dropconnect(W3)
b3 = bias_variable([1000])
h3 = tf.nn.relu(tf.matmul(h2, dropconnect(W3)) + b3)

# Drop
h3 = dropout(h3)

W4 = weight_variable([1000, 10])
b4 = bias_variable([10])
y_hat = tf.nn.softmax(tf.matmul(h3, W4) + b4)

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_hat), reduction_indices=[1]))
xent_summary = tf.scalar_summary('xent', cross_entropy)

correct_prediction = tf.equal(tf.argmax(y_hat, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
acc_summary = tf.scalar_summary('accuracy', accuracy)

train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy + _lambda * sum_weights(W1,W2,W3, b1,b2,b3))

#
# ==================================================================
#

# sess.run(tf.initialize_all_variables())

#
# ==================================================================
#

# NOTE: we're using a single, fixed batch of the first 1000 images
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

images = mnist.train.images[0:1000, :]
labels = mnist.train.labels[0:1000, :]

ga_train = []
ga_trial = []


# for k in keep_probability:

sess = tf.Session()
sess.run(tf.initialize_all_variables())
for i in range(100):
    _, acc = sess.run([train_step, accuracy], feed_dict={x: images, y_: labels})

    if (i == 90):
        ga_train.append(acc)
    if (i % 25 == 0):
        print("step %d, training accuracy %g" % (i, acc))

final_acc = sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels})
ga_trial.append(final_acc)
print("drop {} test accuracy {} kpi {}".format(keep_probability[kpi], final_acc, kpi))

