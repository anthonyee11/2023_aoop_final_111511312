import tensorflow as tf
from tensorflow.python.platform import gfile

# Path to the .pb file
model_filename ='faster-rcnn_inception-resnet-v2.pb'

# Convert .pb to .pbtxt
with gfile.FastGFile(model_filename,'rb') as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')
    tf.io.write_graph(graph_def, './', 'output.pbtxt', as_text=True)
