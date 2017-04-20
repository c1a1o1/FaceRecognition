# -*-coding:utf-8 -*-
__author__ = 'liubo-it'

import os
import sys
from DeepID.DeepId1.DeepId import train_valid_deepid, extract_feature
import numpy as np
from time import time
from sklearn.cross_validation import train_test_split
from PIL import Image
from scipy.misc import imread, imsave, imresize
from CriticalPointDetection.split_pic import get_landmarks, get_nose, get_left_eye, get_right_eye, cal_angel
import traceback
from skimage.transform import rotate
import pdb
from util.load_data import load_rgb_multi_person_all_data


def load_train_data(folder, shape=(156, 124, 3), need_pic_list=False, pic_num_threshold=1000, part_func=None,
                    person_num=None):
    label_int = True
    filter_list = []
    func_args_dic = {}
    data, label, all_pic_list = load_rgb_multi_person_all_data(
                        folder, shape, label_int, person_num, pic_num_threshold, filter_list, func_args_dic)
    if need_pic_list:
        return data, label, all_pic_list
    else:
        return data, label



class DeepId():
    def __init__(self):
        self.data_folder = '/data/liubo/face/vgg_face_dataset/'
        self.model_folder = '/data/liubo/face/vgg_face_dataset/model/'
        self.small_person_num_str = 'small_data'
        self.all_person_num_str = 'all_data'
        self.pic_shape = (78, 62, 3)
        self.person_num = 2622
        self.pic_num_threshold = 30
        self.deepid_model_file = os.path.join(self.model_folder, 'vgg_face.2622.78-62.rgb.deepid.model')
        self.deepid_weight_file = os.path.join(self.model_folder,'vgg_face.2622.78-62.rgb.deepid.weight')
        self.part_func = None
        print self.deepid_model_file
        print self.deepid_weight_file

    def train_vgg_face(self):
        # 所有数据进行训练
        data_folder = self.data_folder
        data, label = load_train_data('/data/liubo/face/vgg_face_dataset/all_data/pictures_box', shape=self.pic_shape,
                        pic_num_threshold=self.pic_num_threshold, part_func=self.part_func, person_num=self.person_num)

        # 1800人用于训练,800人用于验证
        X_train, X_test, y_train,  y_test = train_test_split(data, label, test_size=0.1)
        # pdb.set_trace()
        # X_train = np.transpose(X_train, (0, 3, 1, 2))
        # X_test = np.transpose(X_test, (0, 3, 1, 2))
        nb_classes = len(set(list(y_train)))
        # nb_classes = 2622

        print 'all shape : ',X_train.shape, y_train.shape, X_test.shape, y_test.shape
        weight_file = self.deepid_weight_file
        model_file = self.deepid_model_file
        print 'model_file : ', model_file, ' weight_file : ', weight_file
        error_valid_sample_file = os.path.join(data_folder,'error_valid_sample.txt')
        error_train_sample_file = os.path.join(data_folder,'error_train_sample.txt')
        train_valid_deepid(X_train, y_train, X_test, y_test, nb_classes, model_file, weight_file,
                       error_train_sample_file, error_valid_sample_file)



if __name__ == '__main__':
    deepid = DeepId()
    deepid.train_vgg_face()
