import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine(r'mysql+pymysql://root:123456@10.133.229.100:3306/smart_ac')
sql = 'select * from hf_data'

df = pd.read_sql_query(sql,engine)
list_id = df['家电id'].unique()

for id in list_id:
    data = df.query('家电id == %s' % id)
    data = data[data['on_off_flag'].isin([1])]
    data = data[data['开关机'].isin(['1'])]
    temp = data['温度']
    list_temp = []
    for i in temp:
        list_temp.append(i)
    tim = data['time']
    list_time = []
    for i in tim:
        list_time.append(i)
    plt.figure(figsize=(12,6))
    plt.plot(list_time,list_temp)
    plt.xticks(rotation=70)  # 横坐标刻度旋转角度
    plt.xlabel('%s'%id)
    plt.ylabel('temperature')
    plt.show()
