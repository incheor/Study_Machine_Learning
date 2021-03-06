# -*- coding: utf-8 -*-
"""10. 파이토치를 이용한 CNN 핵심 모듈 구현.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JNAzGKRtrXX4JkPQUFds_cldLwURIlSb

# 개요

- CNN에서 합성곱과 풀링이 어떤 방식으로 처리되는지 이해
- 편향, 패딩은 고정하고 사용
- x, W, s, p 간의 공식 확인
- W를 직접 설계(수직, 수평, 빛의 방향 검토)
"""

import torch
torch.__version__

"""# 이미지 준비"""

import matplotlib.pyplot as plt
# Pillow
from PIL import Image

img = Image.open('/content/drive/MyDrive/딥러닝/dl/torch3.png')
img

import numpy as np

tmp = np.array(img)
tmp.shape

# (높이, 너비, 채널)

# 컬러 이미지를 grayscale로 처리해서 1채널 이미지로 만듬
# L = R * (299 / 1000) + G * (나머지 / 1000) + b * (114 / 1000)
img = img.convert('L')
img

tmp = np.array(img)
tmp.shape

# 1채널이라서 채널값 자체가 사라짐

img_Tensor = torch.Tensor(tmp)
img_Tensor.size()

