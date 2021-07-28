import pandas as pd
import  matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import numpy as np
from minepy import MINE
register_matplotlib_converters()

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

data=pd.read_excel('data.xlsx')

data['avg_Score'] = np.round(data['score'].rolling(window=30,min_periods=1).mean(), 2)
data['avg_Price'] = np.round(data['price'].rolling(window=30,min_periods=1).mean(), 2)

mine = MINE(alpha=0.6, c=15)
mine.compute_score(data['avg_Score'], data['avg_Price'])
print(mine.mic())

mine = MINE(alpha=0.6, c=15)
mine.compute_score(data['score'], data['price'])
print(mine.mic())

plt.plot(data['date'],data['avg_Score'],linestyle='--',label='mood')
plt.xticks(rotation=45)
plt.legend(loc='upper left')
plt.twinx()
plt.plot(data['date'],data['avg_Price'],color='red',label='stock price')
plt.xticks(rotation=45)
plt.legend(loc='upper right')
plt.show()
