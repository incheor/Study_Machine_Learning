# -*- coding: utf-8 -*-
"""04.opencv_faster_rcnn_inference.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aX4mHGTfUQByaxE5BAXvNOyv_D3dfGMH

# OpenCV DNN 패키지를 이용하여 Faster R-CNN 기반의 Object Detection 실습

Tensorflow 에서 Pretrained 된 모델 파일을 OpenCV에서 로드하여 이미지와 영상에 대한 Object Detection 해보기

## Image Object Detection 해보기

### 이미지 다운로드
"""

!mkdir /content/data
!wget -O ./data/beatles01.jpg https://raw.githubusercontent.com/chulminkw/DLCV/master/data/image/beatles01.jpg

# Commented out IPython magic to ensure Python compatibility.
import cv2
import matplotlib.pyplot as plt
# %matplotlib inline

img = cv2.imread('./data/beatles01.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print('image shape:', img.shape)
plt.figure(figsize=(12, 12))
plt.imshow(img_rgb)

"""### OpenCV에서 Inference 모델 생성하기 위해 Tensorflow에서 Pretrained 된 Inference모델(Frozen graph)와 환경파일을 다운로드
- https://github.com/opencv/opencv/wiki/TensorFlow-Object-Detection-API 에 다운로드 URL 있음
- pretrained 모델은 http://download.tensorflow.org/models/object_detection/faster_rcnn_resnet50_coco_2018_01_28.tar.gz 에서 다운로드 후 압축 해제
- pretrained 모델을 위한 환경 파일은 https://github.com/opencv/opencv_extra/blob/master/testdata/dnn/faster_rcnn_resnet50_coco_2018_01_28.pbtxt 에서 다운로드 
- download된 모델 파일과 config 파일을 인자로 하여 inference 모델을 DNN에서 로딩함 
"""

# 경로 지정 및 다운로드
!mkdir ./pretrained
!wget -O ./pretrained/faster_rcnn_resnet50_coco_2018_01_28.tar.gz http://download.tensorflow.org/models/object_detection/faster_rcnn_resnet50_coco_2018_01_28.tar.gz
!wget -O ./pretrained/config_graph.pbtxt https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/faster_rcnn_resnet50_coco_2018_01_28.pbtxt

# 압축풀기
!tar -xvf ./pretrained/faster*.tar.gz -C ./pretrained

# 내용물 확인
!pwd
!ls -lia ./pretrained/faster_rcnn_resnet50_coco_2018_01_28

"""### dnn에서 readNetFromTensorflow()로 tensorflow inference 모델을 로딩"""

# 가중치 모델 파일, 환경 파일
cv_net = cv2.dnn.readNetFromTensorflow('./pretrained/faster_rcnn_resnet50_coco_2018_01_28/frozen_inference_graph.pb', 
                                       './pretrained/config_graph.pbtxt')

"""### coco 데이터 세트의 클래스(카테고리) id별 클래스명 지정(주의)

- coco 데이터 세트에는 id가 없는 클래스가 있음
"""

# OpenCV Yolo용
# 0 ~ 79
labels_to_names_seq = {0:'person',1:'bicycle',2:'car',3:'motorbike',4:'aeroplane',5:'bus',6:'train',7:'truck',8:'boat',9:'traffic light',10:'fire hydrant',
                        11:'stop sign',12:'parking meter',13:'bench',14:'bird',15:'cat',16:'dog',17:'horse',18:'sheep',19:'cow',20:'elephant',
                        21:'bear',22:'zebra',23:'giraffe',24:'backpack',25:'umbrella',26:'handbag',27:'tie',28:'suitcase',29:'frisbee',30:'skis',
                        31:'snowboard',32:'sports ball',33:'kite',34:'baseball bat',35:'baseball glove',36:'skateboard',37:'surfboard',38:'tennis racket',39:'bottle',40:'wine glass',
                        41:'cup',42:'fork',43:'knife',44:'spoon',45:'bowl',46:'banana',47:'apple',48:'sandwich',49:'orange',50:'broccoli',
                        51:'carrot',52:'hot dog',53:'pizza',54:'donut',55:'cake',56:'chair',57:'sofa',58:'pottedplant',59:'bed',60:'diningtable',
                        61:'toilet',62:'tvmonitor',63:'laptop',64:'mouse',65:'remote',66:'keyboard',67:'cell phone',68:'microwave',69:'oven',70:'toaster',
                        71:'sink',72:'refrigerator',73:'book',74:'clock',75:'vase',76:'scissors',77:'teddy bear',78:'hair drier',79:'toothbrush' }

# OpenCV Tensorflow Faster-RCNN용
# 0 ~ 90
labels_to_names_0 = {0:'person',1:'bicycle',2:'car',3:'motorcycle',4:'airplane',5:'bus',6:'train',7:'truck',8:'boat',9:'traffic light',
                    10:'fire hydrant',11:'street sign',12:'stop sign',13:'parking meter',14:'bench',15:'bird',16:'cat',17:'dog',18:'horse',19:'sheep',
                    20:'cow',21:'elephant',22:'bear',23:'zebra',24:'giraffe',25:'hat',26:'backpack',27:'umbrella',28:'shoe',29:'eye glasses',
                    30:'handbag',31:'tie',32:'suitcase',33:'frisbee',34:'skis',35:'snowboard',36:'sports ball',37:'kite',38:'baseball bat',39:'baseball glove',
                    40:'skateboard',41:'surfboard',42:'tennis racket',43:'bottle',44:'plate',45:'wine glass',46:'cup',47:'fork',48:'knife',49:'spoon',
                    50:'bowl',51:'banana',52:'apple',53:'sandwich',54:'orange',55:'broccoli',56:'carrot',57:'hot dog',58:'pizza',59:'donut',
                    60:'cake',61:'chair',62:'couch',63:'potted plant',64:'bed',65:'mirror',66:'dining table',67:'window',68:'desk',69:'toilet',
                    70:'door',71:'tv',72:'laptop',73:'mouse',74:'remote',75:'keyboard',76:'cell phone',77:'microwave',78:'oven',79:'toaster',
                    80:'sink',81:'refrigerator',82:'blender',83:'book',84:'clock',85:'vase',86:'scissors',87:'teddy bear',88:'hair drier',89:'toothbrush',
                    90:'hair brush'}

# OpenCV Tensorflow SSD용
# 1 ~ 91
labels_to_names = {1:'person',2:'bicycle',3:'car',4:'motorcycle',5:'airplane',6:'bus',7:'train',8:'truck',9:'boat',10:'traffic light',
                    11:'fire hydrant',12:'street sign',13:'stop sign',14:'parking meter',15:'bench',16:'bird',17:'cat',18:'dog',19:'horse',20:'sheep',
                    21:'cow',22:'elephant',23:'bear',24:'zebra',25:'giraffe',26:'hat',27:'backpack',28:'umbrella',29:'shoe',30:'eye glasses',
                    31:'handbag',32:'tie',33:'suitcase',34:'frisbee',35:'skis',36:'snowboard',37:'sports ball',38:'kite',39:'baseball bat',40:'baseball glove',
                    41:'skateboard',42:'surfboard',43:'tennis racket',44:'bottle',45:'plate',46:'wine glass',47:'cup',48:'fork',49:'knife',50:'spoon',
                    51:'bowl',52:'banana',53:'apple',54:'sandwich',55:'orange',56:'broccoli',57:'carrot',58:'hot dog',59:'pizza',60:'donut',
                    61:'cake',62:'chair',63:'couch',64:'potted plant',65:'bed',66:'mirror',67:'dining table',68:'window',69:'desk',70:'toilet',
                    71:'door',72:'tv',73:'laptop',74:'mouse',75:'remote',76:'keyboard',77:'cell phone',78:'microwave',79:'oven',80:'toaster',
                    81:'sink',82:'refrigerator',83:'blender',84:'book',85:'clock',86:'vase',87:'scissors',88:'teddy bear',89:'hair drier',90:'toothbrush',
                    91:'hair brush'}

"""### 이미지를 preprocessing 수행하여 Network에 입력하고 Object Detection 수행 후 결과를 이미지에 시각화

- 원본 이미지를 Faster RCNN기반 네트워크로 입력 시 사이즈가 변경됨
"""

img.shape

# scaling된 이미지를 기반으로 bounding box 위치가 예측되므로
# 이를 다시 원본 이미지로 변환하기 위해서는 원본 이미지 shape 정보가 필요함
# 그래서 shape 저장해놓음
rows = img.shape[0]
cols = img.shape[1]

# cv2의 rectangle()은 인자로 들어온 이미지 배열에 직접 사각형을 업데이트 하므로 그림 표현을 위한 별도의 이미지 배열 생성
draw_img = img.copy()

# 원본 이미지 배열 BGR을 RGB로 변환하여 배열 입력
# Tensorflow Faster RCNN은 마지막 classification layer가 Dense가 아니라서 size를 고정할 필요는 없음
cv_net.setInput(cv2.dnn.blobFromImage(img, swapRB = True, crop = False))

# Object Detection 수행하여 결과를 cvOut으로 반환
cv_out = cv_net.forward()

# cv_out : object Detection 수행한 결과는 4차원 배열임
# 앞 2개는 무시, 3번째는 찾은 오브젝트 수, 4번째는 찾은 오브젝트들의 요소임
# (요소들에 대한 설명은 아래 셀에서 확인)
print(cv_out.shape)

# bounding box의 테두리와 caption 글자색 지정
green_color = (0, 255, 0)
red_color = (0, 0, 255)

# detected 된 object들을 반복하면서 정보 추출
for detection in cv_out[0,0,:,:]:
    score = float(detection[2])
    class_id = int(detection[1])
    # detected된 object들의 score가 0.5 이상만 추출
    if score > 0.5:
        # detected된 object들은 scale된 기준으로 예측되었으므로 다시 원본 이미지 비율로 계산
        left = detection[3] * cols
        top = detection[4] * rows
        right = detection[5] * cols
        bottom = detection[6] * rows
        # labels_to_names_seq 딕셔너리로 class_id값을 클래스명으로 변경
        caption = "{}: {:.4f}".format(labels_to_names_0[class_id], score)
        print(caption)
        #cv2.rectangle()은 인자로 들어온 카피한 draw_img에 사각형을 그림, 위치 인자는 반드시 정수형이야함
        cv2.rectangle(draw_img, (int(left), int(top)), (int(right), int(bottom)), color = green_color, thickness = 2)
        cv2.putText(draw_img, caption, (int(left), int(top - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_color, 1)

img_rgb = cv2.cvtColor(draw_img, cv2.COLOR_BGR2RGB)

plt.figure(figsize = (12, 12))
plt.imshow(img_rgb)

# object Detection 수행한 결과는 4차원 배열임
cv_out
# 위의 4차원 배열의 4번째 요소
# 첫번째는 무시, 클래스 id, 클래스 id 확신 정도, 좌상단 좌표 2개, 우상단 좌표 2개 총 7개
# 이게 총 100개

"""### 단일 이미지의 object detection을 함수로 만들어보기"""

def get_detected_img(cv_net, img_array, score_threshold, use_copied_array = True, is_print = True):
    import time

    rows = img_array.shape[0]
    cols = img_array.shape[1]
    
    draw_img = None
    if use_copied_array:
        draw_img = img_array.copy()
    else:
        draw_img = img_array
    
    cv_net.setInput(cv2.dnn.blobFromImage(img_array, swapRB = True, crop = False))
    
    start = time.time()
    cv_out = cv_net.forward()
    
    green_color = (0, 255, 0)
    red_color = (0, 0, 255)

    for detection in cv_out[0,0,:,:]:
        score = float(detection[2])
        class_id = int(detection[1])
        # detected된 object들의 score가 함수 인자로 들어온 score_threshold 이상만 추출
        if score > score_threshold:
            left = detection[3] * cols
            top = detection[4] * rows
            right = detection[5] * cols
            bottom = detection[6] * rows
            caption = "{}: {:.4f}".format(labels_to_names_0[class_id], score)
            # print(class_id, caption)
            print(caption)
            cv2.rectangle(draw_img, (int(left), int(top)), (int(right), int(bottom)), color = green_color, thickness = 2)
            cv2.putText(draw_img, caption, (int(left), int(top - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_color, 1)
    if is_print:
        print('Detection 수행시간:',round(time.time() - start, 2),"초")

    return draw_img

# 함수 사용
img = cv2.imread('./data/beatles01.jpg')
print('image shape:', img.shape)
cv_net = cv2.dnn.readNetFromTensorflow('./pretrained/faster_rcnn_resnet50_coco_2018_01_28/frozen_inference_graph.pb', 
                                       './pretrained/config_graph.pbtxt')
draw_img = get_detected_img(cv_net, img, score_threshold = 0.5, use_copied_array = True, is_print = True)

img_rgb = cv2.cvtColor(draw_img, cv2.COLOR_BGR2RGB)

plt.figure(figsize = (12, 12))
plt.imshow(img_rgb)

# 다른 image 테스트
!wget -O ./data/baseball01.jpg https://raw.githubusercontent.com/chulminkw/DLCV/master/data/image/baseball01.jpg

img = cv2.imread('./data/baseball01.jpg')
print('image shape:', img.shape)
cv_net = cv2.dnn.readNetFromTensorflow('./pretrained/faster_rcnn_resnet50_coco_2018_01_28/frozen_inference_graph.pb', 
                                       './pretrained/config_graph.pbtxt')
draw_img = get_detected_img(cv_net, img, score_threshold = 0.5, use_copied_array = True, is_print = True)

img_rgb = cv2.cvtColor(draw_img, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(12, 12))
plt.imshow(img_rgb)

"""## Video Object Detection 해보기

### 비디오 다운로드
"""

!wget -O ./data/Jonh_Wick_small.mp4 https://github.com/chulminkw/DLCV/blob/master/data/video/John_Wick_small.mp4?raw=true

"""### VideoCapture와 VideoWriter 설정하기

- VideoCapture를 이용하여 Video를 frame별로 capture 할 수 있도록 설정함
  - VideoCapture의 속성을 이용하여 Video Frame의 크기 및 FPS 설정함
- VideoWriter를 위한 인코딩 코덱 설정 및 영상 write를 위한 설정함
"""

# Object Detection할 비디오
video_input_path = '/content/data/Jonh_Wick_small.mp4'
# Object Detection해서 바운딩박스를 그릴 비디오
video_output_path = './data/John_Wick_small_cv01.mp4'

# 비디오를 읽음
cap = cv2.VideoCapture(video_input_path)

# VideoWriter의 인코딩 코덱 설정
codec = cv2.VideoWriter_fourcc(*'XVID')

# 비디오 사이즈 : 너비, 높이
vid_size = (round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# fps설정
vid_fps = cap.get(cv2.CAP_PROP_FPS )

# 위에서 한 설정들 넣어서 VideoWriter
vid_writer = cv2.VideoWriter(video_output_path, codec, vid_fps, vid_size) 

# 프레임 확인
frame_cnt = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print('총 Frame 갯수:', frame_cnt)

"""### 프레임 별로 반복하면서 Object Detection 수행함(개별 frame별로 단일 이미지 Object Detection과 유사)"""

import time

green_color=(0, 255, 0)
red_color=(0, 0, 255)

while True:
    hasFrame, img_frame = cap.read()
    if not hasFrame:
        print('더 이상 처리할 frame이 없습니다.')
        break

    rows = img_frame.shape[0]
    cols = img_frame.shape[1]
    cv_net.setInput(cv2.dnn.blobFromImage(img_frame,  swapRB = True, crop = False))
    
    start= time.time()

    cv_out = cv_net.forward()
    frame_index = 0
    for detection in cv_out[0,0,:,:]:
        score = float(detection[2])
        class_id = int(detection[1])
        if score > 0.5:
            left = detection[3] * cols
            top = detection[4] * rows
            right = detection[5] * cols
            bottom = detection[6] * rows
            caption = "{}: {:.4f}".format(labels_to_names_0[class_id], score)
            cv2.rectangle(img_frame, (int(left), int(top)), (int(right), int(bottom)), color = green_color, thickness = 2)
            cv2.putText(img_frame, caption, (int(left), int(top - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, red_color, 1)
    print('Detection 수행 시간:', round(time.time()-start, 2),'초')
    vid_writer.write(img_frame)

vid_writer.release()
cap.release()

"""### video detection 전용 함수 만들어보기"""

def do_detected_video(cv_net, input_path, output_path, score_threshold, is_print):
    
    cap = cv2.VideoCapture(input_path)

    codec = cv2.VideoWriter_fourcc(*'XVID')

    vid_size = (round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    vid_fps = cap.get(cv2.CAP_PROP_FPS)

    vid_writer = cv2.VideoWriter(output_path, codec, vid_fps, vid_size) 

    frame_cnt = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('총 Frame 갯수:', frame_cnt)

    green_color = (0, 255, 0)
    red_color = (0, 0, 255)

    while True:
        hasFrame, img_frame = cap.read()
        if not hasFrame:
            print('더 이상 처리할 frame이 없습니다.')
            break
        
        # 위에서 만든 단일 이미지 Object Detect 함수
        img_frame = get_detected_img(cv_net, img_frame, score_threshold = score_threshold, use_copied_array = False, is_print = is_print)
        
        vid_writer.write(img_frame)

    vid_writer.release()
    cap.release()

# 함수 사용
do_detected_video(cv_net, '/content/data/Jonh_Wick_small.mp4', './data/John_Wick_small_02.mp4', 0.2, False)