import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(r'mysql+pymysql://root:123456@10.133.229.100:3306/smart_ac')
sql  = 'select * from hf_filter_data'

# engine = create_engine(r'mysql+pymysql://root:123456@localhost:3306/test')
# sql = 'select * from hf_filter_data'

df = pd.read_sql_query(sql,engine)
list_time = []
for i in df['time']:
     list_time.append(i)
list_time1 = []
for i in list_time:
    i = str(i)
    i = i.split(':')[0]+':'+i.split(':')[1]
    list_time1.append(i)
df['time'] = list_time1
# df.to_excel(r'df.xlsx',index=False)
# ['类型','家电id','时间','开关机','温度','模式','风速','室内温度','室外温度','on_off_flag','']
# df = df.drop_duplicates()
list_columns = []
for i in df.columns.values:
    if i!= '家电id'and i != '时间' and i!= 'index':
        list_columns.append(i)
df.drop_duplicates(list_columns,keep='last',inplace=True)

# df.to_excel('df1.xlsx',index=False)
pd.io.sql.to_sql(df,'hf_filter_data2',con=engine,if_exists='append',index=False)




