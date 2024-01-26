import json
import os

import numpy as np
import tensorflow as tf
from PIL import Image
from PIL.ImageDraw import ImageDraw

import operator

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

class CutImage():
    def __init__(self, input_path, parent_dir, moduleDir, img):
        self.input_path = input_path
        self.parent_dir = parent_dir
        self.moduleDir = moduleDir
        self.image = img
        self.image_np = np.array(self.image)
        
        self.image_width, self.image_height = self.image.size

    def loadModule(self):
        print('In cut-image class, loading module')
        path_to_checkpoint = self.moduleDir
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(path_to_checkpoint, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        return detection_graph
    def run_single_image(self, graph):
        print('into_run_for_single-image')
        with graph.as_default():
            with tf.Session() as sess:
                ops = tf.get_default_graph().get_operations()
                all_tensor_names = {output.name for op in ops for output in op.outputs}
                tensor_dict = {}
                for key in [
                    'num_detections',
                    'detection_boxes',
                    'detection_scores',
                    'detection_classes'
                ]:
                    tensor_name = key + ':0'

                    if tensor_name in all_tensor_names:
                        tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)

                image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

                # Run inference
                output_dict = sess.run(tensor_dict, feed_dict={image_tensor: np.expand_dims(self.image_np, 0)})

                # all outputs are float32 numpy arrays, so convert types as appropriate
                output_dict['num_detections'] = int(output_dict['num_detections'][0])
                output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
                output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
                output_dict['detection_scores'] = output_dict['detection_scores'][0]

                return output_dict
    def calc_Measures(self, output_dict):
        measures = []
        basename, ext = os.path.splitext(self.input_path)
        output_image = basename + '_bboxes' + ext
        overlay = Image.new('RGBA', self.image.size)
        image = self.image.convert("RGBA")
        image_draw = ImageDraw(overlay)
        for idx in range(output_dict['num_detections']):
            if output_dict['detection_scores'][idx] > 0.5:

                y1, x1, y2, x2 = output_dict['detection_boxes'][idx]

                y1 = y1 * self.image_height
                y2 = y2 * self.image_height
                x1 = x1 * self.image_width
                x2 = x2 * self.image_width

                measures.append({
                    'left': x1,
                    'top': y1,
                    'right': x2,
                    'bottom': y2
                })
                # color = 'f' + str(55555+color_index)
                if output_image is not None:
                    image_draw.rectangle([int(x1), int(y1), int(x2), int(y2)], fill='#00FFFF1B')
                    image_draw.rectangle([int(x1), int(y1), int(x2), int(y2)], outline='#008888', width=2)

            else:
                break

        if output_image is not None:
            result_image = Image.alpha_composite(image, overlay).convert('RGB')
            result_image.save('./Output/'+output_image)
        return measures

    def save_result(self, measures):
        parent_dir = self.parent_dir
        image = self.image.convert("RGBA")
        basename, ext = os.path.splitext(self.input_path)
        output_folder = basename + '_bboxes_results'

        print('into save result')
        output_path = os.path.join(parent_dir, output_folder)
        path = parent_dir+output_folder+'/'
        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        measures.sort(key=operator.itemgetter('top'))

        measures_lines = []
        measure_line = []
        former_height =  measures[0]['top']
        former_bottom = measures[0]['bottom']
        print('start_debug')
        for idx, measure in enumerate(measures):
            

           

            if idx == len(measures) -1:
                measure_line.append(measure)
                measure_line.sort(key=operator.itemgetter('left'))
                measures_lines.append(measure_line)
            elif measure['top'] - former_height <= (former_bottom-former_height)*0.5:
                measure_line.append(measure)
                
            else:
                measure_line.sort(key=operator.itemgetter('left'))
                measures_lines.append(measure_line)
                measure_line = []
                measure_line.append(measure)
            former_height = measure['top']
            former_bottom = measure['bottom']
            

        for l_index, line in enumerate(measures_lines):
            # For every bar
            # for index, measure in enumerate(line):
            #     image_cut = image
            #     rect = measure['left'], measure['top'], measure['right'], measure['bottom'] #left top right bottom
            #     image_cut = image_cut.crop(rect)
            #     image_cut.save(path+str(l_index)+str(index)+ext)

            # For every line
            image_cut = image
            

            rect = line[0]['left'], line[0]['top'], line[len(line)-1]['right'], line[len(line)-1]['bottom'] #left top right bottom
            image_cut = image_cut.crop(rect)
            image_cut.save(path+str(l_index)+ext)
        return measures_lines, output_folder
        
