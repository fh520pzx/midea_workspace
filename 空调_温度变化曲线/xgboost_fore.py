from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ShuffleSplit
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

data = pd.read_excel('test.xlsx')

features = data.drop(['runstatus', 'windspeedset', 'adt', 'tin','tout', 'humidity', 'flag'],axis=1)
x = np.array(features)
y = np.array(data['tin'])
xgb_model = XGBRegressor(nthread=7)
cv_split = ShuffleSplit(n_splits=6,train_size=0.7,test_size=0.2)
grid_params = dict(
    max_depth = [10],
    learning_rate = [0.001],
    min_child_weight=[1],
    gamma = [0.1],
    n_estimators = [1000]
)
grid = GridSearchCV(xgb_model,grid_params,cv=cv_split,scoring='neg_mean_squared_error')
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
xgb_model.fit(x_train, y_train)
score = xgb_model.score(x_test, y_test)
print(score)

x_table = []
y_table = []
for i in range(0,3600):
    x_table.append(i)
    appliance_id =2199024235794
    tset = 20
    tin = 30
    modeset = 2
    x_t = [[appliance_id,tset,tin,modeset,i]]
    y1 = xgb_model.predict(x_t)[0]
    y_table.append(y1)
plt.figure(figsize=(15, 5))
plt.plot(x_table,y_table,linewidth=1)
plt.xticks(rotation=30)  # 横坐标刻度旋转角度
plt.show()
