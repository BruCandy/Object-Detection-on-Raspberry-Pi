from models.ssd_predictions import SSDPredictions
from models.ssd import SSD
import torch
import cv2



voc_classes = ["kamukamu","tsubu"]

ssd_cfg = {
    'classes_num': 21, 
    'input_size': 300,
    'dbox_num': [4, 6, 6, 6, 4, 4], 
    'feature_maps': [38, 19, 10, 5, 3, 1], 
    'steps': [8, 16, 32, 64, 100, 300], 
    'min_sizes': [30, 60, 111, 162, 213, 264],  
    'max_sizes': [60, 111, 162, 213, 264, 315], 
    'aspect_ratios': [[2], [2, 3], [2, 3], [2, 3], [2], [2]],
}

net = SSD(phase="test", cfg=ssd_cfg)
net_weights = torch.load(
    'models/gumi_weights_train.pth',
    map_location={'cuda:0': 'cpu'},
    weights_only=True)

net.load_state_dict(net_weights)

ssd = SSDPredictions(eval_categories=voc_classes, net=net)
image_file_path = "data/つぶぐみ.jpg"
image = cv2.imread(image_file_path)
rgb_img, predict_bbox, pre_dict_label_index, scores = ssd.ssd_predict(image, confidence_threshold=0.8)
labels = ssd.detect_label(predict_bbox, pre_dict_label_index, voc_classes)
print(labels[0])