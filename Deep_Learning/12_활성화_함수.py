# -*- coding: utf-8 -*-
"""14.활성화 함수.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RfITnd5TtRArwOaDEENPk_tJu_DAPh5f

# 개요

- activation function
- 사용 이유
  - 인공신경망의 **정확도를 높이기 위해** 다양한 시도들이 도입
    - 신경망의 설계 관점(deep 하게?, 새로운 구조?)
    - 최적화(SGD, Adam, Momentum,,....) 이용
    - 활성화 함수 -> 데이터를 조정, 비선형을 구성 -> 깊이값을더 부여
  - 단점
    - 최적화, 활성화함수를 사용하면, 정보손실이 발생함
  - 장점
    - 특정층을 지나서 선형적인 분포를 가진 데이터를 비선형으로 흩트러 놓아 망을 더 추가하게 하는 역활 담당 = Deep 하게 하는 요인
    - 이상치, 결측치 등을 제거 하는 역활(학습중에 발생되는 데이터)
    - 특정 유형으로 데이터를 조정하는 역활
  - **정확도를 올리는 튜닝 포인트로 이해**

# sigmoid

- 초기 딥러닝에서 가장 많이 사용
- 입력 : 실수값 ( -∞ ~ +∞ )
- 출력 : 0 ~ 1 로 수렴 (음수가없다)
- 특징
  - 어떤 실수값이 와도 음수가 나올수 없다
  - 입력값이 커지거나, 작아지면 점점 0.0이나 1.0에 수렴하는 특징
    - 이 정도 근처에 오면 기울기가 0이된다
      - 가중치가 미반영되는 문제 -> 학습이 않됨 -> 신경(뉴련)이 죽었다 -> **죽은 뉴런 문제**
"""

from IPython.display import Image
Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/dl/activate_sigmod_1.png')

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/dl/activate_sigmod_2.png')

"""# tanh

- sigmod를 개선
  - 변동폭을 **2배로 개선**
  - y값을 0~1 => -1 ~ 1 로 확장
    - sigmod에 비해 2배 정도 수치를 커버링
      - **죽은 뉴런 문제는 미해결**
"""

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/dl/activate_tanh_1.png')

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/dl/activate_tanh_2.png')

"""# Relu

- 최근 가장 많이 사용됨
  - Relu를 개선한 하위 함수도 많다
  - 장점
    - 최적화 도구(SGD, Adam,..)가 가장 빠르게 최적의 가중치를 찾도록 도와주는 역활
    - 연산 비용 저렴
      - x가 양수면 그값 그대로, 음수면 0
  - 단점
    - 오차역전파(y->x) 진행시, 입력이 움수인 경우에서, 무응답 상태가 올수 있다
      - **죽은 뉴런 문제 발생**
"""

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/dl/activate_ReLu_1.png')

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/dl/activate_ReLu_2.png')

"""# Leaky Relu

- 음수대 값을 임계값을 부여하여, 조정(기울기를 부여)
  - 0에 아주 가깝게 기울기를 부여
  - 임계값 0.01
  - 죽은 뉴런은 아니다
  - 경우에 따라서 렐루보다 좋은 성능을 내기도 한다
"""

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/dl/activate_leaky_ReLu_1.png')

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/dl/activate_leaky_ReLu_2.png')

"""# PRelu

- 0.01로 고정된 Leaky Relu 개선
  - 자유도를 부여
  - 임계값을 Parameter로 입력받아서 적용
  - 유연성이 높아졌음
"""

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/dl/activate_PReLu_1.png')

"""# ELU

- 음수대 영역을 미분을 적용하여 처리
- 직선이 아닌 커브 형태(곡선)으로 커버
  - 연산 비용이 발생(비싸다)
"""

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/dl/activate_ELU_1.png')

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/dl/activate_ELU_2.png')

"""# Maxout

- Relu의 장점을 가져오고
- 죽은 뉴런의 문제도 해결
- 파라미터가 많아졌다 => 연산량 증가 => 학습 속도 저하 문제 발생
"""

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/dl/activate_maxout_1.png')

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/dl/activate_maxout_2.png')

"""# softmax

- 전체 총량에 대한 자기 지분 => 개별확률
- 결과의 총합은 1
- 다향분류에 적합
- 통상, 분류의 문제의 출력층에 주로 사용
"""

Image('/content/drive/MyDrive/k-디지털-품질재단/딥러닝/dl/activate_softmax.jpg')

"""# 기타 사용자정의

- 필요에 의해, 특수 목적을 달성하기위해서 생성
"""