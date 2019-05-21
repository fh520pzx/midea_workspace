import pandas as pd
from sqlalchemy import create_engine
import favourite_temp
#初始化数据库连接，使用pymysql模块

# engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test')
# # engine = create_engine('mysql+pymysql://root:123456@10.133.229.100:3306/recommend')
# # #查询语句
# # sql = 'select * from mapping'
# #
# # #read_sql_query的两个参数，sql语句，数据库连接
# # df = pd.read_sql_query(sql,engine)
# # print(df)
# df = pd.read_excel(r'D:\MyData\fanghui3\Desktop\京东数据\test.xlsx')
# # pd.io.sql.to_sql(sub_df,'chat_data',con=engine,if_exists='append',index=False)
# pd.io.sql.to_sql(df,'test_smart_acr',con=engine,if_exists='append',index=False)
# import datetime
# def ts_time(time,day_num):
#     time_list = []
#     time_last = pd.to_datetime(time,format="%Y-%m-%d")
#     time_first = time_last-datetime.timedelta(days=(day_num-1))
#     while (time_first <= time_last):
#         time_list.append(time_first)
#         time_first = time_first + datetime.timedelta(days=1)
#     return time_list
# if __name__ == '__main__':
#     print(ts_time('2018-4-5',3))
# time = '2019-4-5'
# time_list = []
# time_last = pd.to_datetime(time,format="%Y-%m-%d")
# time_first = time_last-datetime.timedelta(days=2)
# while (time_first <= time_last):
#     time_list.append(time_first)
#     time_first = time_first + datetime.timedelta(days=1)
# print(time_list)
df = pd.read_csv(r'D:\MyData\fanghui3\Desktop\test2.txt', delim_whitespace=True)
print(len(df))