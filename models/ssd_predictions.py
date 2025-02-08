import numpy as np
import cv2  
import torch
from models.voc import DataTransform


class SSDPredictions:
    def __init__(self, eval_categories, net):
        self.eval_categories = eval_categories
        self.net = net
        color_mean = (104, 117, 123)  
        input_size = 300  
        self.transform = DataTransform(input_size, color_mean)
    
    def ssd_predict(self, image, confidence_threshold=0.5):
        height, width, channels = image.shape
        rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        phase = 'val'
        img_transformed, boxes, labels = self.transform(
            image,  
            phase,
            '',   
            '') 
        img = torch.from_numpy(
            img_transformed[:, :, (2, 1, 0)]).permute(2, 0, 1)
        self.net.eval()  
        x = img.unsqueeze(0)  
        detections = self.net(x)
        predict_bbox = []
        pre_dict_label_index = []
        scores = []
        detections = detections.cpu().detach().numpy()
        find_index = np.where(detections[:, :, :, 0] >= confidence_threshold)
        detections = detections[find_index]
        
        for i in range(len(find_index[1])):
            if (find_index[1][i]) > 0: 
                sc = detections[i][0]  
                bbox = detections[i][1:] * [width, height, width, height]
                lable_ind = find_index[1][i]-1
                scores.append(sc)
                predict_bbox.append(bbox)
                pre_dict_label_index.append(lable_ind)
        
        return rgb_img, predict_bbox, pre_dict_label_index, scores
  
    def detect_label(self, bbox, label_index, label_names):
        labels = [] 
        for i, bb in enumerate(bbox):
            label_name = label_names[label_index[i]]
            if label_name not in labels: 
                labels.append(label_name)
        return labels        
