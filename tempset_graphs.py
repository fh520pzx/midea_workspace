import pandas as pd
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv(r'D:\MyData\fanghui3\Desktop\liyu_data.txt',delim_whitespace=True)
list_id = df['applianceID'].unique()

for i in range(10):
    id = list_id[i]
    data = df.query('applianceID == %s'%id)
    data = data.sort_values('dt')
    list_dt = []
    for i in data['dt']:
        ltime = time.localtime(i / 1000)
        timeYMD = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
        list_dt.append(str(timeYMD))
    data['dt'] = list_dt
    data['dt'] = pd.to_datetime(data['dt'])
    plt.figure(figsize=(15, 5))
    plt.plot(data['dt'],data['tempset'],linewidth=1)
    plt.xticks(rotation=-30)  # 横坐标刻度旋转角度
    plt.title(id)
    plt.show()




