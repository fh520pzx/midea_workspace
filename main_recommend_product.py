import pandas as pd
from sqlalchemy import create_engine
import datetime

engine = create_engine('mysql+pymysql://root:123456@10.133.229.100:3306/product_info')
sql = 'select * from main_recommend_dialog'
df = pd.read_sql_query(sql,engine)

df = df[['category_id','item_code','recommend_dialog','product_url']]

df.dropna(axis=0, how='any', inplace=True)

a = df.drop_duplicates(subset='category_id',keep='first')
b = df.drop_duplicates(subset='category_id',keep='last')

df = a.append(b)
df = df.drop_duplicates(keep='first')
df.insert(0,'level','1')
start_time = datetime.datetime.now()
end_time =datetime.datetime.now() + datetime.timedelta(days=30)
df.insert(5,'start_time',start_time)
df.insert(6,'end_time',end_time)
df.insert(7,'attributes','无')

pd.io.sql.to_sql(df,'main_recommend_product',con=engine,if_exists='append',index=False)






