# -*- coding: utf-8 -*-
"""22.생산적_적대_신경망_GAN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1a1VyoOUY4h9sQubHO8w-OPczLDHFfTrS

# Generative Adversarial Networks(GAN)

- GAN(간)
- 생성모델, 딥러닝을 이용하여 가상의 데이터를 생성하는 신경망
- 예)
  - 얼굴생성, 스타일 합성 => 데이터생성
- 원리
  - 진짜같은 가짜를 만들기 위해서, 서로 상반된 **적대적인 경합**을 진행한다
- 요약
  - 생성자 (Generator)
    - 가짜 데이터를 만든다
    - 진짜같은, 가짜를 구분못할정도로 데이터를 생성하겠금 훈련
    - 판별자를 속이는것 목적
      
  - 판별자 (Discriminator)
    - 가짜와 진짜를 경합하여 가짜를 걸러내는것 목표
    - 이것을 잘 구분하도록 훈련한다
    - 더이상 가짜를 구분할수 없을때까지 훈련한다
  
- 훈련 종료
  - 균형
"""

from IPython.display import Image
Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/new_res/GAN-기본구성.png')

# 1. 실제 데이터, x
# 2. 랜덤/잡음의 백터 : 가짜 데이터를 만들 재료. z
# 3. 생성자 네트워크(모델) : z를 입력받아서, 가짜샘플 x*를 생성
# 4. 판별자 네트워크(모델) : x, x*을 입력받아서, 진짜/가짜를 구분
# 5. 분류의 오차값을 기준으로 반복적으로 과정진행 => 미세조정값을
#    생성자에게 전달 => 생성자가 최적화되게 진행
#    판별자는 전달은 하되 반영되지 않고(학습하지 않는다)->훈련진행
# 6. 균형을 이루면, 잘속이지도, 속지도 않는 상태 => 학습종료

"""# 생성자

- 입력
  - 잡음 백터(랜덤값)
  - ex) 평균0, 표준편차(혹은 분산) 1인 랜덤값
- 출력 / 목표
  - 진짜와 거의 구분이 않되는 가짜 데이터(샘플)

# 판별자

- 입력
  - x : 실제 샘플(훈련 데이터)
  - x* : 가짜 샘플(생성자가 만든)
- 출력 
  - 진짜인 확률
- 목표
  - 진짜와 가짜를 잘 구분해 내느것
"""

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/new_res/GAN-1.png', width=500)

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/new_res/GAN-2.png', width=500)

"""# 종류

- Auto Encoder
  - GAN의 기본 개념을 정립한 모델
  - 2개 모델이 경합하면서 서로 발전한다는 기초 아이디어 제공
- GAN
  - 하위 모델의 기본 모형
- **DCGAN**
  - GAN의 성능을 높이기 위해 
  - Deep 합성곱(Convolution)
  - 최신 GAN의 형식이 완성됨  
- WGAN
- ProGAN
  - 실제 사진과 비슷하게 생성
  - 풀 HD급
  - 전이학습으로 사용가능
- SGAN
  - 준지도 분야 가장 기대되는 모델
- CGAN
- CycleGAN
  - 스타일 트렌스퍼
  - 화풍을 가져와서 새로운 이미지에 화풍을 넣어서 생성
"""

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/new_res/GAN-3.png', width=500)
# CycleGAN

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/new_res/GAN-4.png', width=500)
# ProGAN

"""# DCGAN

- 데이터 MNIST
- 목표 : DCGAN을 통해서 손글씨 이미지를 생성한다(판별자가 가짜와 진짜를 구분하지 못할 정도까지 훈련시키셔)
"""

from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import Input, Dense, Reshape, Flatten, Dropout
from tensorflow.keras.layers import BatchNormalization, Activation, LeakyReLU, UpSampling2D, Conv2D
from tensorflow.keras.models import Sequential, Model
import numpy as np
import matplotlib.pyplot as plt

"""## 생성자 모델"""

# 가짜 데이터 생성 -> 7*7 -> 14*14 -> 28*28 -> 가짜이미지 생성
generator = Sequential()
# (?, 100) => (?, 7*7*128)=(?, 6272), 7*7 이미지의 1픽셀은 128 표현
generator.add( Dense(7*7*128, input_dim=100, activation=LeakyReLU(0.2) ))
# 데이터가 흐트러져있다 => 층이 깊어도 안정화되게 학습이 되도록
# 데이터를 조정하는 배치정규화 적용:평균0,  분산 1 =>조정
generator.add( BatchNormalization() )
# 세로7,가로7,1픽셀의정보128
generator.add( Reshape( (7,7,128) ) )
# 이미지를 세로가로 2배씩 확장 (14,14,128)
generator.add( UpSampling2D() )
# (14,14,128)->(14,14,64)
generator.add( Conv2D(64, kernel_size=5, padding='same')  )
generator.add( BatchNormalization() )
generator.add( Activation(LeakyReLU(0.2)) )
# (14,14,64) -> (28,28,64)
generator.add( UpSampling2D() )
generator.add( Conv2D(1, kernel_size=5, padding='same', activation='tanh') )
generator.summary()

"""## 판별자 모델"""

# 가짜와 진짜를 구분 -> CNN 진영, 28 -> 14 -> 7 -> 수렴
discriminator = Sequential()
# (?, 28,28,1) -> (?, 14,14,64)
discriminator.add(Conv2D(64, kernel_size=5, strides=2, padding='same', input_shape=(28,28,1)))
discriminator.add(Activation(LeakyReLU(0.2)))
discriminator.add(Dropout(0.3))
# (?, 14,14,64) -> (?, 7,7,128)
discriminator.add(Conv2D(128, kernel_size=5, strides=2, padding='same'))
discriminator.add(Activation(LeakyReLU(0.2)))
discriminator.add(Dropout(0.3))
# (?, 7,7,128) -> (?, 7*7*128)
discriminator.add(Flatten())
# (?, 7*7*128) -> (?, 1)
discriminator.add(Dense(1,activation='sigmoid'))

discriminator.compile(loss='binary_crossentropy', optimizer='adam')

# 판별자는 미세조정을 통한 최적화를 하지는 않는다. 
# 그 수치는 생성자에게 전달
discriminator.trainable = False

discriminator.summary()

"""## GAN 모델"""

# 생성자와 판별자 (100,) -> (28,28,1) -> (1,)
g_input  = Input( shape=(100,) )                 # 생성자 입력
d_ouptut = discriminator( generator( g_input ) ) # 연결하여 판별자 출력
gan      = Model( g_input, d_ouptut )            # GAN 모델 완성
gan.compile(loss='binary_crossentropy', optimizer='adam')
gan.summary()

"""## 훈련

- 학습 진행간 특정 주기 단위로 가짜 데이터를 저장
- 가짜데이터를 뿌리면서 최종적으로 진짜 처럼 변화되는 결과물을 확인
"""

def dcgan_train_simul( epoch, batch_size, save_inter ):
  # 1. 데이터 로드 -> 진짜 가짜만 가리면 되므로, 실제 데이터만 필요
  (X_train, _),(_,_)= mnist.load_data()
  # (60000, 28, 28)
  print( X_train.shape )  
  X_train = X_train.reshape( -1,28,28,1 ).astype('float32')
  # 생성자를 통해서 나오느 데이터는 -1 ~ 1
  # 원본데이터는 0~255 -> 0~1 -> -1 ~ 1
  X_train = (X_train - 127.5) / 127.5 # -1 ~ 1
  # 판별자가 데이터를 판독하기 위해서 값의 범위를 조정했다
  
  # 2. 정답을 비교하여 학습시 사용할 비교백터 준비
  true  = np.ones( (batch_size,1) ) # 모든 구성원 값이 1
  false = np.zeros((batch_size,1) ) # 모든 구성원 값이 0

  # 세대 학습
  for i in range( epoch ): # 2000번 반복 
    # 3. 생성자
    # 3-1 잡음백터 생성
    noise = np.random.normal( 0, 1, (batch_size, 100) ) # (32, 100)
    # 3-2 백터를 넣어서 이미지 생성(생성자의 예측)
    # (32, 28, 28, 1)
    gen_images = generator.predict( noise )
    # 3-3 판별자에게 훈련을 시킨다 => 이 데이터는 모두 가짜다 
    # d_loss_fake : 가짜데이터가 가짜라고 학습시켰을대 오차값
    d_loss_fake = discriminator.train_on_batch( gen_images, false )

    # 4. 판별자 
    # 4-1. 진짜 데이터를 batch_size 만큼 추출
    #      0 ~ 6000 개 사이에 난수로 무작위로 32개가 추출(인덱스)
    rand_idx    = np.random.randint( 0, X_train.shape[0], batch_size)
    real_images = X_train[ rand_idx ]
    # 이 이미지는 모드 진짜야 => 학습
    d_loss_real = discriminator.train_on_batch( real_images, true )
    # 오차평균
    d_loss = np.add(d_loss_fake, d_loss_real) * 0.5

    # 5. GAN 학습 및 백터를 진짜로 예측하는 오차율
    #    시간이 많이 지나서 이 오차율이 0에 수렴하면
    #    생성자가 거의 진짜를 만들고 있다 -> 판단
    g_loss = gan.train_on_batch( noise, true )

    print( 'epoch:%d' % i, 'd_loss:%.4f' % d_loss, 
           'g_loss:%.4f' % g_loss  )
    
    # 7. 저장
    if i % save_inter == 0 :
      # 한번 저장할때 16개씩 생성
      noise  = np.random.normal( 0, 1, (16, 100) )
      # 생성자가 이미지를 만든다
      g_imgs = generator.predict( noise )
      # 현재 이미지 값은 tanh => -1*0.5 ~ 1*0.5 
      # => -0.5+0.5 ~ 0.5+0.5 => 0~1
      g_imgs = g_imgs*0.5 + 0.5
      fig, axs = plt.subplots(4,4)
      cnt = 0
      for i in range(4):
        for j in range(4):
          axs[i,j].imshow( g_imgs[ cnt, : , : , 0 ], cmap='gray' )
          cnt += 1
      fig.savefig( 'gan_%d.png' % i)
    pass
  pass

import tensorflow as tf
with tf.device('/device:gpu:0'):
  dcgan_train_simul( 2000, 32, 100 )

