import tensorflow as tf


def content_loss(sess, vgg, content_img, content_layers, content_layer_weights, ops):
    # vgg_layers = vgg_rawnet['layers'][0]
    # sess.run(getattr(vgg.parameters, 'preprocess').assign(content_img))
    sess.run(ops, feed_dict={vgg.imgs: content_img})

    # sess.run(vgg['input'].assign(content_img))
    content_loss = 0.
    for layer, weight in zip(content_layers, content_layer_weights):
        p = sess.run(getattr(vgg, layer))
        x = getattr(vgg, layer)
        p = tf.convert_to_tensor(p)
        content_loss += content_layer_loss(p, x) * weight
    content_loss /= float(len(content_layers))
    return content_loss


def style_loss(sess, vgg, style_imgs, style_layers, style_layer_weights, style_imgs_weights, ops):
    init = tf.initialize_all_variables()
    total_style_loss = 0.
    weights = style_imgs_weights
    for img, img_weight in zip(style_imgs, weights):
        # sess.run(vgg['input'].assign(img))
        sess.run(ops, feed_dict={vgg.imgs: style_imgs})

        style_loss = 0.
        for layer, weight in zip(style_layers, style_layer_weights):
            a = sess.run(getattr(vgg, layer))
            x = getattr(vgg, layer)
            a = tf.convert_to_tensor(a)
            style_loss += style_layer_loss(a, x) * weight
        style_loss /= float(len(style_layers))
        total_style_loss += (style_loss * img_weight)
    total_style_loss /= float(len(style_imgs))
    return total_style_loss


def content_layer_loss(p, x):
    _, h, w, d = p.get_shape()
    M = h.value * w.value
    N = d.value
    K = 1. / (2. * N ** 0.5 * M ** 0.5)
    loss = K * tf.reduce_sum(tf.pow((x - p), 2))
    return loss


def style_layer_loss(a, x):
    _, h, w, d = a.get_shape()
    M = h.value * w.value
    N = d.value
    A = gram_matrix(a, M, N)
    G = gram_matrix(x, M, N)
    loss = (1. / (4 * N ** 2 * M ** 2)) * tf.reduce_sum(tf.pow((G - A), 2))
    return loss


def gram_matrix(x, area, depth):
    F = tf.reshape(x, (area, depth))
    G = tf.matmul(tf.transpose(F), F)
    return G
