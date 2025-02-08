from models.augmentations import Compose, ConvertFromInts, ToAbsoluteCoords, \
                                 PhotometricDistort, Expand, RandomSampleCrop, \
                                 RandomMirror, ToPercentCoords, Resize, SubtractMeans

class DataTransform:
    def __init__(self, input_size, color_mean):
        self.transform = {
            'train': Compose([
                ConvertFromInts(),    
                ToAbsoluteCoords(),   
                PhotometricDistort(), 
                Expand(color_mean),   
                RandomSampleCrop(),  
                RandomMirror(),     
                ToPercentCoords(), 
                Resize(input_size),
                SubtractMeans(color_mean)
            ]),
            'val': Compose([
                ConvertFromInts(),  
                Resize(input_size), 
                SubtractMeans(color_mean)
            ])
        }
        
    def __call__(self, img, phase, boxes, labels):
        return self.transform[phase](img, boxes, labels)