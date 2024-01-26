import os


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import cv2
import numpy as np

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw



tf.compat.v1.disable_eager_execution()
voc_file = "/Users/user/Documents/OneDrive/College Stuff/NYCU/Python for DS/Final_Project/Semantic_dep/vocabulary_semantic.txt"
# model = "/Users/user/Documents/OneDrive/College Stuff/NYCU/Python for DS/Final_Project/Self_trained_semantic_model/trained_semantic_model-12600.meta"
model = '/Users/user/Documents/OneDrive/College Stuff/NYCU/Python for DS/Final_Project/Semantic-Model/semantic_model.meta'

sess = tf.compat.v1.InteractiveSession()
# Read the dictionary
dict_file = open(voc_file,'r')
dict_list = dict_file.read().splitlines()
int2word = dict()
for word in dict_list:
  word_idx = len(int2word)
  int2word[word_idx] = word
dict_file.close()

# Restore weights
saver = tf.compat.v1.train.import_meta_graph(model)
saver.restore(sess,model[:-5])

graph = tf.compat.v1.get_default_graph()

input = graph.get_tensor_by_name("model_input:0")
seq_len = graph.get_tensor_by_name("seq_lengths:0")
rnn_keep_prob = graph.get_tensor_by_name("keep_prob:0")
height_tensor = graph.get_tensor_by_name("input_height:0")
width_reduction_tensor = graph.get_tensor_by_name("width_reduction:0")
logits = tf.compat.v1.get_collection("logits")[0]

# Constants that are saved inside the model itself
WIDTH_REDUCTION, HEIGHT = sess.run([width_reduction_tensor, height_tensor])

decoded, _ = tf.nn.ctc_greedy_decoder(logits, seq_len)

def normalize(image):
  return (255. - image)/255.


def resize(image, height):
  print('input HEIGHT in resize function',height)
  print('Original w & h', image.shape[1], image.shape[0])
  width = int(float(height * image.shape[1]) / image.shape[0])
  # height > org_height >> width 拉長
  # height < org_height >> width 縮水
  sample_img = cv2.resize(image, (width, height))
  
  return sample_img

def sparse_tensor_to_strs(sparse_tensor):
		indices= sparse_tensor[0][0]
		values = sparse_tensor[0][1]
		dense_shape = sparse_tensor[0][2]

		strs = [ [] for i in range(dense_shape[0]) ]
		
		string = []
		ptr = 0
		b = 0

		for idx in range(len(indices)):
			if indices[idx][0] != b:
				strs[b] = string
				string = []
				b = indices[idx][0]

			string.append(values[ptr])

			ptr = ptr + 1

		strs[b] = string

		return strs

class Predict:
	def __init__(self, measures_lines, inputs_path, input_image):
		self.measures_lines = measures_lines
		self.inputs_path = inputs_path
		self.input_image =input_image
	
	def predict(self, image_path):
		
		open_image = Image.open(image_path)

		image = open_image.convert('L') # 轉為灰階圖像
		
		image = np.array(image)
		image = resize(image, HEIGHT) # 轉為模型指定高度
		image = normalize(image) # 將 灰階值 轉到 0-1 之間
		image = np.asarray(image).reshape(1,image.shape[0],image.shape[1],1)

		seq_lengths = [ image.shape[2] / WIDTH_REDUCTION ]
		prediction = sess.run(decoded,
							feed_dict={
								input: image,
								seq_len: seq_lengths,
								rnn_keep_prob: 1.0,
							})
		str_predictions = sparse_tensor_to_strs(prediction)

		array_of_notes = []
		for w in str_predictions[0]:
			array_of_notes.append(int2word[w])
		notes=[]

		# 把符號切開 >> 低調音域跟節拍訊息
		for i in array_of_notes:
			if i[0:5]=="note-":
				if not i[6].isdigit():
					notes.append(i[5:7])
				else:
					notes.append(i[5])
		img = open_image.convert('L')
		size = (img.size[0], int(img.size[1]*1.3)) #image height * 1.5(for label usage)
		layer = Image.new('RGB', size, (255,255,255))
		layer.paste(img, box=None)
		open_image.close()
		img_arr = np.array(layer)
		height = int(img_arr.shape[0])
		width = int(img_arr.shape[1])
		# print(img_arr.shape[0])
		draw = ImageDraw.Draw(layer)
		# font = ImageFont.truetype(<font-file>, <font-size>)
		font = ImageFont.truetype("/Users/user/Documents/OneDrive/College Stuff/NYCU/Python for DS/Final_Project/Semantic_dep/Aaargh.ttf", 20)
		# draw.text((x, y),"Sample Text",(r,g,b))
		j = width / 9
		img.close()
		for i in notes:
			draw.text((j, height-40), i, (0,0,0), font=font)
			j+= (width / (len(notes) + 4))
		
		return layer, notes, array_of_notes

	def predict_lines(self):
		img = self.input_image
		result_img = img.copy()
		result_notes = []
		for l_index, line in enumerate(self.measures_lines):
			# For every bar
			# for index, measure in enumerate(line):
			# 	path = self.inputs_path+'/'+str(l_index)+str(index)+'.png'
			# 	result, notes = self.predict(path)
			# 	print(str(l_index)+str(index), notes)
			# 	print(result)
			# 	result_img.paste(result, (int(measure['left']), int(measure['top'])))

			# For every line
			path = './Output/output_bboxes_results/'+str(l_index)+'.png'
			result, notes, array_of_notes = self.predict(path)
			print(str(l_index), notes, array_of_notes)
			result_img.paste(result, (int(line[0]['left']), int(line[0]['top'])))

			result_notes.append(array_of_notes)

		
		return result_img, result_notes


