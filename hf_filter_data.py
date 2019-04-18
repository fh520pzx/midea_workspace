import pandas as pd
from sqlalchemy import create_engine
import datetime

engine = create_engine(r'mysql+pymysql://root:123456@10.133.229.100:3306/smart_ac')
sql = 'select * from hf_data order by time'

# engine = create_engine(r'mysql+pymysql://root:123456@localhost:3306/test')
# sql = 'select * from test order by time'

df = pd.read_sql_query(sql,engine)
df['家电id'].astype('str')
list_id = df['家电id'].unique()
print(list_id)
print('读取数据完成！')
for id in list_id:
    data = df.query('家电id == %s'%id)
    data['家电id'].astype('str')
    data['time'] = pd.to_datetime(data['time'],format="%Y-%m-%d %H:%M:%S")
    list = []
    for i in data['time']:
        list.append(i)
    for i in range(0,len(list)-1):
        j=i+1
        if(((list[j]-list[i]).seconds)<=3):
            list[i] = None
    data['time'] = list
    data.dropna(axis=0,how='any',inplace=True)

    pd.io.sql.to_sql(data,'hf_filter_data',con=engine,if_exists='append',index=False)
    print('id为%s的数据入库成功'%id)







