# -*- coding: utf-8 -*-
"""4. 딥러닝 개요.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P5rY3pRc96GoO94zf2WTvNCILb5rTCtp

# 개발 환경

- 로컬 PC
  - 레이저 컴퓨터
    - 게이밍 노트북
    - EGPU 활용
  - GPU가 있는 컴퓨터
    - NVIDA : CUDA 기술, google colab도 NVIDA 씀
    - AMD : ROCm 기술, 이제는 tensorflow, pyTorch에서도 지원
    - 애플 맥 : M1, M1Max, M1Pro, M2(CPU, GPU, 메모리 통합)
  - 없으면 그냥 CPU로 학습시키기 
- 클라우드
  - 기존 제품 활용
    - aws, azure, google
    - google colab은 12시간 제한(GPU or TPU)
      - GPU 학습이 CPU 학습보다 시간적 이득이 확실할 경우 사용하기
      - GPU 학습시 랜덤 시드값(파이썬, 시스템, 넘파이, 딥러닝 엔딘)이 변경되는 버그가 일부 있음
    - 정부 과제한다면 보통 azure(사업계획서에 작성)
  - 자체 구축
    - 딥러닝 워크스테이션 구축
    - 우분두 + 파이썬(직접 설치 or 아나콘다)
      - GUI 있는 우분투 + 팀뷰어
    - 스펙이 적절하면 가상으로 나눠서 사용

## TPU(Tensor Processing Unit)

- 구글에서 만든 연산 장치
- GPU보다 성능이 우수
- 구글 클라우드에서만 사용 가능(외부 판매 안 함)
- 주로 딥마인드에서 사용함(알파고도 TPU로 학습했음)

# 인공지능
"""

from IPython.display import Image
Image('/content/drive/MyDrive/딥러닝/dl/ai_ml_dl.png')

"""- 약 AI
  - 약한 AI
  - 시기 : 2025년
  - 핵심 : 하나만 잘 함
  - 예측
    - 완전 자율 주행(테슬라)
    - 로봇(테슬라봇)
- 강 AI
  - 강한 AI
  - 시기 : 2040년
  - 핵심 : 여러가지 일을 모두 잘 함
  - 예측
    - 영화에서 볼 수 있었던 AI
    - 인간의 지성 수준에 도달
- 초 AI
  - 시기 : 2060년
  - 핵심 : 인간의 시성 수준을 초월

# 이미지 인식 대회(ILSVRC)

- 한 장의 사진에서 한 장의 객체를 검출해서 그 정확도를 경연하는 대회
- 2017년에 종료되고 kaggle로 자료 이관됨
- history
  - AlexNet(2012)
    - 8 Layer
    - CNN을 처음으로 영상 인식에 사용했는데 이를 통해서 영상 인식 분야에 CNN을 사용해야 한다는 패러다임 전환(이전가지는 머신러닝으로 진행했음)
  - GoogleNet(2014 ~ 2016)
    - Inception v2~ v4
    - Firebase MLKit, MobileNet에서 활용
  - VGG((2014)
    - VGG-16, VGG-19
    - 전이학습의 대표 사례로 많이 사용
  - ResNet(2015)
    - 128 layer
    - 깊을수록 성능이 좋아진다는 패러다임의 한계를 전환한 신경망
    - 강화학습에서 활용
  - SeNet(2017)
    - 인식 오차율 2.3%로 인간의 수준(5%)을 뛰어 넘은 신경망
    - 대회가 종료 (더이상 의미 없음)
"""

Image('/content/drive/MyDrive/딥러닝/dl/ILSVRC_인식률.png')

Image('/content/drive/MyDrive/딥러닝/dl/ILSVRC_깊이.png')

Image('/content/drive/MyDrive/딥러닝/dl/googLeNet.png')

"""# 분야

- 성과를 낸 분야
  - 객체 탐지
  - 음성 인식
  - 자연어 처리
- 관심이 커지는 분야
  - 생성 : 영상, 음성, 텍스트
  - 시뮬레이션
  - 강화 학습

# 엔진

- 개발 생산성 향상 목적
- 엔진을 사용하지 않고 C++, Numpy로도 가능함

## Tensorflow

- Google에서 제작, 개발자가 가장 많음
- PC, 모바일, 서버, 웹 모두 지원
- 1.x 버전과 2.x 버전(현재 최신)이 있음
- Define And Run(정의하고 실행함)
- C++로 실질적인 연산 처리해서 빠름, 하지만 디버깅이 어려움
- 코드는 파이썬으로 작성하지만 cython을 거쳐서 C++로 최종 처리함
- 개발 방식
  - 1.x를 2.x에 호환되게 처리
  - 2.x로 순수하게 처리
  - Keras로 작성(케라스의 백엔드가 TF가 되는구조)

## PyTorch

- Meta(구 FaceBook)에서 제작, 점유율 2위
- PC, 모바일 지원
- 파이썬 스타일임
- 연구기관에서 주로 사용
- Define By Run(정의하면 즉시 실행)
- 파이썬과 루아(Lua)로 만들어짐

## Keras(인터페이스)

- 텐서플로우 커밋 2017 행사에서 공식적으로 통합됨
- 점유율 3위(텐서플로우에 병합되어서 사용됨)
- 엔진은 백엔드로 두고 그 상위에서 공통 API를 통해서 팁러닝이 가능하게 만들어진 구조
- 문과생을 위한 엔진

## 기타 엔진

- Theano
- CNTK
- MXNET
- coffee
- Chainer

# 인공신경망

## CNN

### 개념

- 컨볼류젼(합성곱) 뉴럴 네트워크
- 주 분야는 영상 인식
- '이 이미지는 xxx이미지임' 라고 분류 처리
- 종류
  - 이미지 한 장에서 한 개의 객체 검출
  - 이미지 한 장에서 여러개의 객체 검출
    - RNN, fast RNN, faster RNN
    - YOLO
  - 이미지 한 장에서 사물의 shape 형태로 검출
    - mediapipe
  - base
    - opencv

## RNN

### 개념

- 순환(재귀적) 뉴럴 네트워크
- 기존 일반적 신경망 + 시퀀스(시간, 순서)
- 난이도가 높은 편
- 종류
  - 자연어 처리
    - 문서 분류
    - 매화문 생성
    - 챗봇
    - 기계 번역
    - 문서 요약
    - 이미지 캡션
    - 토픽 추출
  - 시계열 분야
    - 스마트 팩토리(이상 탐지)
    - 주식/금융/코인/부동산 분석(퀀트가 목표)
    - 통계 : ARIMA, AR, MA, ARMA
    - 머신러닝 : 회귀
    - 딥러닝 : RNN - LSTM, RNN - GRU
    - 상용 라이브러리 : Meta의 Prophet

### 구성

- 입력 대비 출력
  - one to many : 이미지를 보고 텍스트 생성
  - many to one : 감정 분석, 스팸메일 분류
  - many to many : 기계 번역, 챗봇

## GAN

- 적대적 생성 모델
- GAN, DCGAN, DEGAN
- 원리
  - 원본 데이터와 최대한 동일하게 데이터를 생성할 수 있도록 모델을 학습시킴
  - 가짜 데이터를 판독해주는 모델이 진짜 모델이라고 인식하면(가짜 판별을 못하면) 종료
- 예시
  - 가짜 데이터를 잘 만드는 모델을 활용하면 가짜 데이터를 생성하는 모델이 됨
  - 가짜 데이터를 잘 판독해 내는 모델을 활용하면 가짜 데이터 판독기가 됨

# 퍼셉트론

## 개념

- 개요
  - 1957년 제안
  - 기계학습의 기초 개념
- 단순 퍼셉트론
  - 특징
    - 입력층, 출력층이 존재함
    - 입력은 다양하게 x1, x2 등 존재함
    - 출력은 y임
    - 여러개의 입력에서 출력 y에 수렴하고 싶음
    - 어떤 입력이 출력에 얼마큼 영향을 미치는가?

- 예시
  - 입사 기념으로  M2 맥북 에어를 구매할려고 함
    - 구매할 것인가? => 구매 / 비구매 (y)
    - 구매에 미치는 영향 => (x)
      - x1 : 현재 사용하는 노트북이 너무 느림
      - x2 : 새 기분으로 일하고 싶음(원하는 것인가? 필요한 것인가?)
      - x3 : 딥러닝좀 돌릴려고 하는데 좋은 성능  PC가 필요함
      - x4 : 기존 노트북이 너무 무거움
      - x10 : 돈이 있었나? 카드는 되나?...
    - y로 수렴하기 위해서 다수결을 적용한다면
      - 다수의  x가 OK 라면 구매할것인가?
        - 다수의 이유가 살 필요가 있어서 살려고하는데 돈이 부족함, x10에서 만족을 못하는 상황이 발생
    - 왜 이런 상황이 발생했는가?
      - 입력 요인별로 가중치가 다르다, 중요도가 다르다
      - 가중치 W(Weight)
    - 식 
      - x1 * W1 + x2 * W2 + .....x10 * W10 = 합계
      - 합계 > C(임계값)을 넘어서면 구매함
    - 다양한 입력 요인이 보다 올바르게 판단(예측)할 수 있다는 것을 증명했음

- 딥러닝 본질
  - 보다 정확한 예측을 위해서 다양한 입력요인들에게 적절한 W를 계산하는 과정 => 딥러닝 학습의 본질 => W, b
"""

Image('/content/drive/MyDrive/딥러닝/dl/퍼셉트론.png')

Image('/content/drive/MyDrive/딥러닝/dl/학습의본질.png')

# 여러개의 입력은 행렬(배열)을 통해서 표현

