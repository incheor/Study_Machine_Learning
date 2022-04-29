# -*- coding: utf-8 -*-
"""5. 텐서플로우 기초학습.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oh-NIgPLMWtWqKVCTSIsZnzYNk7FS_u4

# 기본구성

- 텐서플로우 1.x, 2.x 버전 구성
"""

! pip list

!pip install tensorflow==1.15

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x

import tensorflow as tf
tf.__version__

"""# Define And Run

- 2개의  파트로 설계하여 개발, 운영함
  - 설계
    - 데이터가 흘러들어가는 플로우를 구성
    - 신경망 구성
    - 네트워크 구성
    - 파이썬으로 구성
    - 실제 연산 작업은 수행하지 않음
  - 학습
    - 실제 데이터를 주입
    - C++이 데이터를 가지고 학습 행위 진행
    - 세션을 획득하고 학습이 진행됨
    - 절차
      - 세션 오픈
      - 데이터 주입
      - 학습 진행(C++), GPU 활용
      - 결과를 돌려받음
      - 세션 닫음
  - 텐서 보드를 활용해서 플로우 및 기타 내용을 확인할 수는 있음

# 텐서플로우 기본 요소

## 텐서(Tensor)

- 연산의 기본 단위이자 데이터의 기본 단위(본질은 행렬)
- 넘파이를 기반으로 구현되어 있음
- ndarray와 tensor 사이에는 거의 유사한 함수들이 존재
- 데이터는 무조건 수치로 표현되어야 함
"""

from IPython.display import Image
Image('/content/drive/MyDrive/딥러닝/dl/텐서용어.png')

Image('/content/drive/MyDrive/딥러닝/dl/tensor_style.jpeg')

"""## 상수(Constant)

- 초기값을 부여할 때 사용
"""

# 1. 플로우 구성
myText = tf.constant(10)
myText
# 현재 데이터 10은 세팅되어있지 않음

# 2. 실행
# 2 - 1. 세션 오픈
sess = tf.Session()

# 2 - 2. 데이터 주입, 실행
result = sess.run(myText)

# 2 - 3. 세션 닫기
sess.close()

# 확인
result

"""## 연산"""

# 1. 플로우 구성
a = tf.constant(1234)
b = tf.constant(4000)

a, b

# 계산식
# add_oper는 a와 b의 + 의 결과임(결과를 가지고만 있음)
add_oper = a + b
add_oper

# 2. 데이터 주입 후 실행
with tf.Session() as sess :
  print(sess.run(add_oper))

"""## 변수(Variable)"""

# 1. 플로우 구성
# name을 주는 이유
# 해당 텐서의 정체성을 정확하게 묘사하고 텐서 보드에서 플로우를 볼 때 좋음
a = tf.constant(1234, name = 'a')
b = tf.constant(4000, name = 'b')
c = tf.constant(4000, name = 'c')

a, b, c

# 변수 : 보통 가중치나 편향값
v = tf.Variable(0, name = 'v')
v

# 연산
x_opr = a + b - c
x_opr

# 데이터 플로우 그래프 : 데이터들의 관계를 그래프로 나타낸 것
assign_opr = tf.assign(v, x_opr)
assign_opr

# 2. 데이터 주입 후 실행
with tf.Session() as sess :
  print(sess.run(assign_opr))
  print(sess.run(v))

"""## 플레이스 홀더(PlaceHolder)

### 개념

- 데이터를 주입할 때 대상이 되는 요소
- 신경망을 구축하고 학습을 전개할 때 데이터를 삽입하는데 그 데이터의 형태는 플레이스 홀더를 기준으로 설계함
- 형태(shape)이 중요함
- 종류
  - 고정 크기 플레이스 홀더
  - 가변 크기 플레이스 홀더

### 고정 크기 플레이스 홀더
"""

# 1. 데이터 플로우 그래프 구성
# 데이터는 정수 + 값이 3개로 구성된 1차원 벡터로 주입하도록 설정
a = tf.placeholder(tf.int32, shape = (3))
a

# 상수
b = tf.constant(2)
b

# 연산
# a는 벡터, b는 스칼라 -> a의 각 요소에 b를 더함
x_opr = a + b
x_opr

# 2. 데이터 주입 및 실행
# 데이터 주입은 feed_dict를 채움, 값은 딕셔너리
# 키는 placeholder를 지칭하는 변수명(여기서는 a)
# 값은 placeholder에서 설정한데로 해야함(여기서는 정수, 값은 3개, 1차원 벡터)
with tf.Session() as sess :
  print(sess.run(x_opr, feed_dict = {a : [1, 2, 3]}))

"""### 가변 크기 플레이스 홀더

- 실제 학습시 형태 : 데이터의 개수가 몇 개인지 모를 때, 가변적일 때
"""

a = tf.placeholder(tf.int32, shape=(None))
b = tf.constant(2)
x_opr = a + b 
with tf.Session() as sess:
  print(sess.run(x_opr, feed_dict={a : [1,2,3]}))
  print(sess.run(x_opr, feed_dict={a : [1,2,3,4,5,6,7,8]}))
  print(sess.run(x_opr, feed_dict={a : [1]}))

