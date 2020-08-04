from IPython.display import SVG
import keras
from keras.utils.vis_utils import model_to_dot
from keras.models import load_model

loaded_model = keras.models.load_model('best_model_2.h5')
SVG(model_to_dot(loaded_model, show_shapes=True).create(prog='dot', format='svg'))