서론
시계열 분석(Time series analysis)이란,
독립변수(Independent variable)를 이용하여 종속변수(Dependent variable)를 예측하는 일반적인 기계학습 방법론에 대하여 시간을 독립변수로 사용한다는 특징이 있다. 독립변수로 시간을 사용하는 특성때문에 분석에 있어서 일반적인 방법론들과는 다른 몇가지 고려가 필요하다.

본 포스트에서는 시계열 분석(혹은 예측)에 있어서 가장 널리 사용되는 모델중 하나인 ARIMA에 대해 알아보고 Python을 통해 구현해본다.
본 포스트에서는

ARIMA의 간단한 개념
ARIMA 모델의 파라미터 선정 방법
실제 데이터와 ARIMA 모델을 이용한 미래 예측
등 과 관련된 내용을 다룬다.

ARIMA(Autoregressive Integrated Moving Average)
ARIMA는 Autoregressive Integrated Moving Average의 약자로, Autoregressive는 자기회귀모형을 의미하고, Moving Average는 이동평균모형을 의미한다.

즉, ARIMA는 자기회귀와 이동평균을 둘 다 고려하는 모형인데, ARMA와 ARIMA의 차이점은 ARIMA의 경우 시계열의 비정상성(Non-stationary)을 설명하기 위해 관측치간의 차분(Diffrance)을 사용한다는 차이점이 있다.
ARMA와 ARIMA 외에도 ARIMAX 등의 방법도 있는데, 이는 본 포스트에서 살펴보지 않는다.

AR: 자기회귀(Autoregression). 이전 관측값의 오차항이 이후 관측값에 영향을 주는 모형이다. 아래 식은 제일 기본적인 AR(1) 식으로, theta는 자기상관계수, epsilon은 white noise이다. Time lag은 1이 될수도 있고 그 이상이 될 수도 있다.
eq_ar1
I: Intgrated. 누적을 의미하는 것으로, 차분을 이용하는 시계열모형들에 붙이는 표현이라고 생각하면 편하다.
MA: 이동평균(Moving Average). 관측값이 이전의 연속적인 오차항의 영향을 받는다는 모형이다. 아래 식은 가장 기본적인 MA(1) 모형을 나타낸 식으로, beta는 이동평균계수, epsilon은 t시점의 오차항이다. 
eq_ma1
현실에 존재하는 시계열자료는 불안정(Non-stationary)한 경우가 많다. 그런데 AR(p), MA(q) 모형이나, 이 둘을 합한 ARMA(p, q)모형으로는 이러한 불안정성을 설명할 수가 없다.
따라서 모형 그 자체에 이러한 비정상성을 제거하는 과정을 포함한것이 ARIMA모형이며 ARIMA(p, d, q)로 표현한다.
eq_arima

eq_arima_mu
eq_arima_ar
eq_arima_ma
eq_arima_d0
eq_arima_d1
eq_arima_d2
위와 같은 특징에 따라 ARMIA(p, d, q)는 AR, MA, ARMA를 모두 표현할 수 있다.

AR(p) = ARIMA(p, 0, 0)
MA(q) = ARIMA(0, 0, q)
ARMA(p, q) = ARIMA(p, 0, q)
이 외에도 ARIMA와 관련한 많은 내용이 있으나, 본 포스트에서는 생략하고 이후 포스트 진행에 필요한 부분들이 있으면 간략하게 설명하겠다. 참고할만한 서적으로는 ARIMA를 포함하여 통계적 시계열분석의 Standard라고 할 수 있는 Box, George; Jenkins, Gwilym (1970). Time Series Analysis: Forecasting and Control.(아마존 링크)를 참조하시면 좋을 듯 하다.

데이터
본 포스트에서 ARIMA를 이용한 예측에 사용할 데이터는 Blockchain Luxembourg S.A에서 Export한 최근 60일간의 비트코인 시세와 관련된 자료이다.
CSV파일로 Export했으며, Column name만 수동으로 추가하여주었다.
---
Date	Price
2017-10-12	5325.130683333333
2017-10-13	5563.806566666666
2017-10-14	5739.438733333333
…	…
미화(USD)기준 가격 변동임에도, 며칠전 일련의 사태(비트코인 플래티넘 등)로 폭등했던 흔적이 남아있다.
rawdata_plot

import pandas as pd

series = pd.read_csv('market-price.csv', header=0, index_col=0, squeeze=True)
series.plot()
---
