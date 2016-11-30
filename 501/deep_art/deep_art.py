import numpy as np
from scipy.misc import imread, imresize

import vgg16
from helper import *

sess = tf.Session()

opt_img = tf.Variable(tf.truncated_normal([1, 224, 224, 3],
                                          dtype=tf.float32,
                                          stddev=1e-1), name='opt_img').initialized_value()

tmp_img = tf.clip_by_value(opt_img, 0.0, 255.0)

vgg = vgg16.vgg16(tmp_img, 'vgg16_weights.npz', sess)

style_img = imread('style.png', mode='RGB')
style_img = imresize(style_img, (224, 224))
style_img = np.reshape(style_img, [1, 224, 224, 3])

content_img = imread('content.png', mode='RGB')
content_img = imresize(content_img, (224, 224))
content_img = np.reshape(content_img, [1, 224, 224, 3])

layers = ['conv1_1', 'conv1_2',
          'conv2_1', 'conv2_2',
          'conv3_1', 'conv3_2', 'conv3_3',
          'conv4_1', 'conv4_2', 'conv4_3',
          'conv5_1', 'conv5_2', 'conv5_3']
# ============================================
# ============================================


# ============================================
# ============================================

ops = [getattr(vgg, x) for x in layers]

alpha = 5e0
beta = 1e4

#
# --- construct your cost function here
# content loss
# For the images shown in Fig 2 we matched the content representation on layer 'conv4_2'
CONTENT_LAYER = ['conv4_2']
CONTENT_LAYER_WEIGHTS = [1.0]
L_content = content_loss(sess, vgg, content_img, CONTENT_LAYER, CONTENT_LAYER_WEIGHTS, ops)
# sess.run(ops, feed_dict={vgg.imgs: content_img})


# and the style representations on layers 'conv1_1', 'conv2_1', 'conv3_1', 'conv4_1' and 'conv5_1'
#   The ratio alpha/beta was  1x10-3
#   The factor w_l was always equal to one divided by the number of active layers (ie, 1/5)
init = tf.initialize_all_variables()

STYLE_LAYERS = ['conv1_1', 'conv2_1', 'conv3_1', 'conv4_1', 'conv5_1']
STYLE_LAYERS_WEIGHTS = [0.2, 0.2, 0.2, 0.2, 0.2]
L_style = style_loss(sess, vgg, style_img, STYLE_LAYERS, STYLE_LAYERS_WEIGHTS, [1], ops)

L_total = alpha * L_content
L_total += beta * L_style

# --- place your adam optimizer call here
#     (don't forget to optimize only the opt_img variable)

# optimization algorithm
LEARNING_RATE = 1e0
optimizer = tf.train.AdamOptimizer(LEARNING_RATE)

# def minimize_with_adam(sess, net, optimizer, init_img, loss):

# this clobbers all VGG variables, but we need it to initialize the
# adam stuff, so we reload all of the weights...
sess.run(tf.initialize_all_variables())
vgg.load_weights('vgg16_weights.npz', sess)
#
# # initialize with the content image


# --- place your optimization loop here
print('\nMINIMIZING LOSS USING ADAM OPTIMIZER')
train_op = optimizer.minimize(L_total)
init_op = tf.initialize_all_variables()
sess.run(init_op)
sess.run(ops, feed_dict={vgg.imgs: content_img})
# sess.run(vgg['input'].assign(content_img))
iterations = 0
MAX_ITERATION = 600
print_iterations = 50

while (iterations < MAX_ITERATION):
    sess.run(train_op)
    if iterations % print_iterations == 0:
        curr_loss = L_total.eval(session=sess)
        print("At iterate {}\tf=  {:.5E}".format(iterations, curr_loss))
    iterations += 1
