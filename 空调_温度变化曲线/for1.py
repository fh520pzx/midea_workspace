import pandas as pd
import numpy as np
import sklearn as skl
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor


data = pd.read_excel('all.xlsx')
features = data.drop(['runstatus', 'windspeedset', 'adt', 'tin','tout', 'humidity', 'flag'],axis=1)
x = np.array(features)
y = np.array(data['tin'])
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2,random_state=1)
model = RandomForestRegressor(n_estimators=450, oob_score=True)
model.fit(x_train, y_train)
score = model.score(x_test, y_test)
print(score)

x_table = []
y_table = []
for i in range(0,6000):
    x_table.append(i)
    appliance_id =2199024235794
    tset = 20
    tin = 26
    modeset = 2
    x_t = [[appliance_id,tset,tin,modeset,i]]
    y1 = model.predict(x_t)[0]
    y_table.append(y1)

plt.figure(figsize=(15, 5))
plt.plot(x_table,y_table,linewidth=1)
plt.xticks(rotation=30)  # 横坐标刻度旋转角度
plt.show()












