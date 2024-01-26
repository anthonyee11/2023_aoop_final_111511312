import tensorflow as tf
from tensorflow.python.platform import gfile
from google.protobuf import text_format

# Path to the .pbtxt file
pbtxt_path = 'output.pbtxt'

# Create a TensorFlow Graph
graph = tf.Graph()

with graph.as_default():
    graph_def = tf.GraphDef()

    # Load the .pbtxt file
    with gfile.FastGFile(pbtxt_path, 'r') as f:
        text_format.Merge(f.read(), graph_def)
        tf.import_graph_def(graph_def, name='')

# Start a TensorFlow session
with tf.Session(graph=graph) as sess:
    # Create a FileWriter to write the graph
    train_writer = tf.summary.FileWriter('logs/', sess.graph)

    # Close the FileWriter
    train_writer.close()
