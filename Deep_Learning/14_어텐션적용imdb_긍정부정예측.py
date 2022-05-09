# -*- coding: utf-8 -*-
"""17.어텐션적용imdb_긍정부정예측.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k1nHyWfWJs2g8eiOJAG6xoHwLXFACS2t
"""

!pip  list

!pip install attention

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.layers import Activation, Conv1D, MaxPool1D, Dropout
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.datasets import imdb
from tensorflow.keras.callbacks import EarlyStopping
from attention import Attention

import numpy as np
import matplotlib.pyplot as plt

(X_train, y_train), (X_test, y_test) = imdb.load_data(
                                          num_words=5000)

X_train = sequence.pad_sequences( X_train, maxlen=500 )
X_test  = sequence.pad_sequences( X_test,  maxlen=500 )

model = Sequential()
model.add( Embedding(5000, 500) )
model.add( Dropout(0.5) )

model.add( Conv1D(64, 5, padding='valid', activation='relu', strides=1) )
# 4 -> 설정값, 커널의 크기
model.add( MaxPool1D(4) )

model.add( LSTM(  50, return_sequences=True ) )
# 어텐션에 사용하기 위해 출력에 sequences를 포함
model.add( Attention() ) # 어텐션 적용
model.add( Dropout(0.5) )
model.add( Dense( 1 ) )
model.add( Activation( 'sigmoid' ) )

model.compile( loss='binary_crossentropy', 
               optimizer='adam', metrics=['accuracy'] )
early_stopping  = EarlyStopping(patience=3)
his = model.fit(X_train, y_train, 
                batch_size=40, epochs=100, 
                validation_split=0.25, 
                callbacks=[early_stopping])
print( '\n정확도 %.4f' % ( model.evaluate(X_test, y_test)[1] ) )







