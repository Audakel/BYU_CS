"""Functions for downloading and reading MNIST data."""
from __future__ import print_function
import os
import urllib
import numpy
from PIL import Image
import subprocess
from sklearn import model_selection


SOURCE_URL = 'http://www.openu.ac.il/home/hassner/data/lfwa/'


def maybe_download(filename, work_directory):
    """Download the data from website, unless it's already here."""
    if not os.path.exists(work_directory):
        os.mkdir(work_directory)
    filepath = os.path.join(work_directory, filename)

    if not os.path.exists(filepath):
        print('Downloading images...')
        filepath, _ = urllib.urlretrieve(SOURCE_URL + filename, filepath)
        statinfo = os.stat(filepath)
        print('Succesfully downloaded', filename, statinfo.st_size, 'bytes.')
    return filepath


def extract_images_and_labels(filename):
    """
    After running this code,
    the data will in the data tensor,
    and the labels will be in the labels tensor:
    """
    if not os.path.exists("lfw2"):
        print('Extracting', filename)
        bashCommand = "tar -xvzf data/lfwa.tar.gz"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    if not os.path.exists("list.txt"):
        bashCommand2 = "find lfw2/ -name *.jpg > list.txt"
        process = subprocess.Popen(bashCommand2.split(), stdout=subprocess.PIPE)
        print('Making list.txt', process.communicate())

    """
    assumes list.txt is a list of filenames, formatted as
    /lfw2//Aaron_Eckhart/Aaron_Eckhart_0001.jpg
    ./lfw2//Aaron_Guiel/Aaron_Guiel_0001.jpg  ...
    """
    files = open('./list.txt').readlines()

    image = numpy.zeros((len(files), 250, 250))
    labels = numpy.zeros((len(files), 1))

    # a little hash map mapping subjects to IDs
    ids = {}
    scnt = 0

    # load in all of our images
    ind = 0
    for fn in files:
        subject = fn.split('/')[2]
        subject = subject[:-10]
        if not ids.has_key(subject):
            ids[subject] = scnt
            scnt += 1
        label = ids[subject]

        image[ind, :, :] = numpy.array(Image.open(fn.rstrip()))
        labels[ind] = label
        ind += 1

    # data is (13233, 250, 250)
    # labels is (13233, 1)
    # Reshape image to flatten
    image = image.reshape(image.shape[0], image.shape[1] * image.shape[2])
    return image, labels


def read_data_sets(train_dir, fake_data=False, one_hot=False):
    ALL_IMAGES = 'lfwa.tar.gz'
    local_file = maybe_download(ALL_IMAGES, train_dir)
    X, y = extract_images_and_labels(local_file)
   
    # X_train, X_test, y_train, y_test
    return model_selection.train_test_split(X, y, test_size=0.2, random_state=42)