import os
import sys
from dotenv import load_dotenv

load_dotenv()
project_path = os.getenv("URL")

os.chdir(project_path)
sys.path.append(os.getcwd())


from gpiozero import LED, Button
import threading
import sys
import cv2
import LCD as lcd_module
import torch
from models.ssd_predictions import SSDPredictions
from models.ssd import SSD

(w, h) = (640, 480)

camera = cv2.VideoCapture(0) 
camera.set(cv2.CAP_PROP_FRAME_WIDTH, w)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

if not camera.isOpened():
    print("Webカメラが見つかりません")
    sys.exit(1)

capturing = False
frame = None

led = LED(17)

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

def takingPicture():
    global capturing
    global frame
    lcd = lcd_module.LCD()
    lcd.write_string("Loading")
    capturing = True
    led.on()
    if frame is not None:
        cv2.imwrite("temp.jpg", frame)
        _, predict_bbox, pre_dict_label_index, _ = ssd.ssd_predict(frame, confidence_threshold=0.8)
        labels = ssd.detect_label(predict_bbox, pre_dict_label_index, voc_classes)
        if (len(labels) == 0):
            lcd.clear()
            lcd.write_string("No det.")
        elif (labels[0] == "tsubu"):
            lcd.clear()
            s = chr(0xc2)+chr(0xcc)+chr(0xf1)+chr(0xb8)+chr(0xf1)+chr(0xd0)
            lcd.write_string(s)
        elif (labels[0] == "kamukamu"):
            lcd.clear()
            s = chr(0xb6)+chr(0xd1)+chr(0xb6)+chr(0xd1)+chr(0xda)+chr(0xd3)+chr(0xdd)
            lcd.write_string(s)
        elif (len(labels) >= 2):
            lcd.clear()
            lcd.write_string("too many")
        else:
            lcd.clear()
            lcd.write_string("error")
    led.off()

def pressed(button):
    if button.pin.number == 27:
        t = threading.Thread(target=takingPicture)
        t.start()

def reset(button):
    global capturing
    if button.pin.number == 22:
        lcd = lcd_module.LCD()
        lcd.write_string("all set")
        capturing = False


btn1 = Button(27, pull_up=False, bounce_time=0.05)
btn1.when_pressed = pressed
btn2 = Button(22, pull_up=False, bounce_time=0.05)
btn2.when_pressed = reset

try:
    while True:
        if not capturing:
            ret, frame = camera.read() 
            if not ret:
                print("フレームを取得できません")
                break
            
            cv2.imshow("Now", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nプログラムを終了")

finally:
    lcd = lcd_module.LCD()
    lcd.clear()
    led.close()
    btn1.close()
    btn2.close()
    camera.release()
    cv2.destroyAllWindows()
