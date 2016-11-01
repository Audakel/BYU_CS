from tensorflow.python.ops import rnn_cell, seq2seq
import tensorflow as tf
import numpy as np
from textloader import TextLoader

#
# -------------------------------------------
#
# Global variables

batch_size = 50
sequence_length = 50
data_loader = TextLoader(".", batch_size, sequence_length)
grad_clip = 5
vocab_size = data_loader.vocab_size  # dimension of one-hot encodings
state_dim = 128

num_layers = 2

tf.reset_default_graph()

#
# ==================================================================
# ==================================================================
# ==================================================================
#

# define placeholders for our inputs.
# in_ph is assumed to be [batch_size,sequence_length]
# targ_ph is assumed to be [batch_size,sequence_length]

in_ph = tf.placeholder(tf.int32, [batch_size, sequence_length], name='inputs')
targ_ph = tf.placeholder(tf.int32, [batch_size, sequence_length], name='targets')
in_onehot = tf.one_hot(in_ph, vocab_size, name="input_onehot")

inputs = tf.split(1, sequence_length, in_onehot)
inputs = [tf.squeeze(input_, [1]) for input_ in inputs]
targets = tf.split(1, sequence_length, targ_ph)

# at this point, inputs is a list of length sequence_length
# each element of inputs is [batch_size,vocab_size]

# targets is a list of length sequence_length
# each element of targets is a 1D vector of length batch_size



# ------------------
# YOUR COMPUTATION GRAPH HERE
with tf.variable_scope("COMPUTATION", reuse=None):
    # create a BasicLSTMCell
    cell = rnn_cell.BasicLSTMCell(state_dim)  # True )

    #   use it to create a MultiRNNCell
    cell = rnn_cell.MultiRNNCell([cell] * num_layers)

    #   use it to create an initial_state
    #     note that initial_state will be a *list* of tensors!
    initial_state = cell.zero_state(batch_size, tf.float32)

    softmax_w = tf.get_variable("softmax_w", [state_dim, vocab_size])
    softmax_b = tf.get_variable("softmax_b", [vocab_size])

    # call seq2seq.rnn_decoder
    outputs, last_state = seq2seq.rnn_decoder(inputs, initial_state, cell)
    output = tf.reshape(tf.concat(1, outputs), [-1, state_dim])

    # transform the list of state outputs to a list of logits.
    logits = tf.matmul(output, softmax_w) + softmax_b
    # use a linear transformation.
    probs = tf.nn.softmax(logits)
    # call seq2seq.sequence_loss
    loss = seq2seq.sequence_loss([logits],
                                    [tf.reshape(targets, [-1])],
                                    [tf.ones([batch_size * sequence_length])],
                                    vocab_size)
    cost = tf.reduce_sum(loss) / batch_size / sequence_length
    final_state = last_state
    lr = tf.Variable(0.0, trainable=False)
    tvars = tf.trainable_variables()
    grads, _ = tf.clip_by_global_norm(tf.gradients(cost, tvars), grad_clip)

    # create a training op using the Adam optimizer
    optimizer = tf.train.AdamOptimizer(lr)
    train_op = optimizer.apply_gradients(zip(grads, tvars))

# ------------------
# YOUR SAMPLER GRAPH HERE
s_in_ph = tf.placeholder(tf.int32, [1], name='s_in_ph')
s_inputs = [tf.one_hot(s_in_ph, vocab_size, name="s_inputs")]

# place your sampler graph here it will look a lot like your
# computation graph, except with a "batch_size" of 1.

with tf.variable_scope("COMPUTATION", reuse=True):
    # ======
    # s_in_ph = tf.placeholder(tf.int32, [1, 1], name='s_in_ph')
    # s_inputs = tf.one_hot(s_in_ph, vocab_size, name="s_inputs")

    # s_inputs_ = tf.split(1, 1, s_inputs)
    # s_inputs_ = [tf.squeeze(input_, [1]) for input_ in s_inputs_]
#    ======

    #   use it to create a MultiRNNCell
    # scope.reuse_variables()
    s_cell = rnn_cell.BasicLSTMCell(state_dim)  # True )

    #   use it to create a MultiRNNCell
    s_cell = rnn_cell.MultiRNNCell([s_cell] * num_layers)

    s_initial_state = s_cell.zero_state(1, tf.float32)

    s_outputs, s_final_state = seq2seq.rnn_decoder(s_inputs, s_initial_state, s_cell)
    # s_final_state = tf.reshape(tf.concat(1, s_outputs), [-1, state_dim])

    # print ("Shape", s_outputs.get_shape())
    # print ("softmax_w ", softmax_w.get_shape())
    logits = tf.matmul(s_outputs[0], softmax_w) + softmax_b
    s_probs = tf.nn.softmax(logits)


#
# ==================================================================
# ==================================================================
# ==================================================================
#

def sample(num=200, prime='ab'):
    # prime the pump

    # generate an initial state. this will be a list of states, one for
    # each layer in the multicell.
    s_state = sess.run(s_initial_state)

    # for each character, feed it into the sampler graph and
    # update the state.
    for char in prime[:-1]:
        x = np.ravel(data_loader.vocab[char]).astype('int32')
        feed = {s_in_ph: x}
        for i, s in enumerate(s_initial_state):
            feed[s] = s_state[i]
        s_state = sess.run(s_final_state, feed_dict=feed)

    # now we have a primed state vector; we need to start sampling.
    ret = prime
    char = prime[-1]
    for n in range(num):
        x = np.ravel(data_loader.vocab[char]).astype('int32')

        # plug the most recent character in...
        feed = {s_in_ph: x}
        for i, s in enumerate(s_initial_state):
            feed[s] = s_state[i]
        ops = [s_probs]
        ops.extend(list(s_final_state))

        retval = sess.run(ops, feed_dict=feed)

        s_probs_ = retval[0]
        s_state = retval[1:]

        # ...and get a vector of probabilities out!

        # now sample (or pick the argmax)
        # sample = np.argmax( s_probsv[0] )
        sample = np.random.choice(vocab_size, p=s_probs_[0])

        pred = data_loader.chars[sample]
        ret += pred
        char = pred

    return ret


#
# ==================================================================
# ==================================================================
# ==================================================================
#

sess = tf.Session()
sess.run(tf.initialize_all_variables())
summary_writer = tf.train.SummaryWriter("./tf_logs", graph=sess.graph)

lts = []

print "FOUND %d BATCHES" % data_loader.num_batches

for j in range(1000):

    state = sess.run(initial_state)
    data_loader.reset_batch_pointer()

    for i in range(data_loader.num_batches):

        x, y = data_loader.next_batch()

        # we have to feed in the individual states of the MultiRNN cell
        feed = {in_ph: x, targ_ph: y}
        for k, s in enumerate(initial_state):
            feed[s] = state[k]

        ops = [train_op, loss]
        ops.extend(list(final_state))

        # retval will have at least 3 entries:
        # 0 is None (triggered by the optim op)
        # 1 is the loss
        # 2+ are the new final states of the MultiRNN cell
        retval = sess.run(ops, feed_dict=feed)

        lt = retval[1]
        state = retval[2:]

        if i % 1000 == 0:
            print "%d %d\t%.4f" % ( j, i, lt )
            lts.append(lt)

    print sample(num=60, prime="And ")
# print sample( num=60, prime="ababab" )
#    print sample( num=60, prime="foo ba" )
#    print sample( num=60, prime="abcdab" )

summary_writer.close()

#
# ==================================================================
# ==================================================================
# ==================================================================
#

# import matplotlib
# import matplotlib.pyplot as plt
# plt.plot( lts )
# plt.show()
