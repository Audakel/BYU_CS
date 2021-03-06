# neural-style

An implementation of neural style in TensorFlow.

This implementation is a lot simpler than a lot of the other ones out there,
thanks to TensorFlow.

TensorFlow doesn't support L-BFGS (which is what the original authors
used), so I use Adam. This may require a little bit more
hyperparameter tuning to get nice results.

## Requirements

* [TensorFlow](https://www.tensorflow.org/versions/master/get_started/os_setup.html#download-and-setup)
* [NumPy](https://github.com/numpy/numpy/blob/master/INSTALL.rst.txt)
* [SciPy](https://github.com/scipy/scipy/blob/master/INSTALL.rst.txt)
* [Pillow](http://pillow.readthedocs.io/en/3.3.x/installation.html#installation)
* [Pre-trained VGG network][net] (MD5 `8ee3263992981a1d26e73b3ca028a123`) - put it in the top level of this repository

