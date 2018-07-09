import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.io import loadmat
import  pickle
from scipy.misc import toimage
from PIL import Image, ImageFilter
from scipy.misc import toimage
from keras.models import model_from_yaml

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

# load YAML and create model
yaml_file = open('/home/anshul/Desktop/handwritten to text/EMNIST-master/model1.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
loaded_model = model_from_yaml(loaded_model_yaml)
# load weights into new model
loaded_model.load_weights("/home/anshul/Desktop/handwritten to text/EMNIST-master/model1.h5")
print("Loaded model from disk")
mapping = pickle.load(open('%s/mapping.p' % '/home/anshul/Desktop/handwritten to text/EMNIST-master/bin', 'rb'))
