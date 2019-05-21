import pandas as pd
from sqlalchemy import create_engine
import datetime


engine = create_engine('mysql+pymysql://root:123456@10.133.229.100:3306/product_info')

engine2 = create_engine('mysql+pymysql://root:123456@10.133.229.100:3306/product_info?charset=utf8mb4')

sql1 = 'select table_name from information_schema.tables where table_schema= "product_info" and table_name like "va_category%%"'
df = pd.read_sql_query(sql1,engine)

sql2 = 'select * from va_midea_goods_list'
df2 = pd .read_sql_query(sql2,engine)
df2 = df2[['midea_erp_code','item_url']]        #list表的信息
midea_code= df2.set_index('midea_erp_code').to_dict()['item_url'] #建立字典 920



list = []
for i in df.table_name:
    sql = 'select * from %s'%i
    data = pd .read_sql_query(sql,engine)
    data = data[['CategoryId','ItemCode','SellingPoint']]
    list.append(data)
df1 = pd.concat(list)                           #category表的信息

df1['product_url'] = df1['ItemCode'].map(midea_code)

df1.insert(0,'level','1')
start_time = datetime.datetime.now()
end_time =datetime.datetime.now() + datetime.timedelta(days=30)
df1.insert(5,'start_time',start_time)
df1.insert(6,'end_time',end_time)
df1.insert(7,'user','无')

df1.rename(columns={'CategoryId':'category_id', 'ItemCode':'item_code','SellingPoint':'recommend_dialog'}, inplace = True)

# df1.to_excel('test.xlsx',index=False)    #url 896

# list = midea_code.keys()     #920
#
# df_test = df1['item_code'].tolist()   #896
#
# for i in list:
#     if i not in df_test:
#         print(i)

pd.io.sql.to_sql(df1,'main_recommend_dialog',con=engine2,if_exists='append',index=False)
















