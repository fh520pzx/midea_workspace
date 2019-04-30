import pandas as pd
import numpy as np
def day_temp(data,da):                                               #传入两个值，data是初始的dateframe，da代表根据几天进行预测
    table = []
    list_id = data['appliance_id'].unique()
    for id in list_id:
        new_data = data.query('appliance_id == %s' % id)
        list_days = new_data['day'].unique()  # 日期列表
        total_temp = []
        for day in list_days:  # 每个日期对应的0时到23时的温度列表
            list_hour = []
            list_temp = []
            temp = []
            data = new_data.loc[df['day'] == day]
            for i in data['hour']:
                list_hour.append(i)
            for j in data['temp_avg']:
                list_temp.append("{:.12g}".format(j))
            hour_temp = dict(zip(list_hour, list_temp))                      #小时对应温度的字典
            for j in range(24):
                if j not in list_hour:
                    temp.append(0)
                else:
                    temp.append(hour_temp.get(j))
            total_temp.append(temp)

        for i in range(24):                                                           #构建表
            for k in range(len(total_temp)-da+1):
                list_table = []
                for j in range(da):
                    list_table.append(total_temp[k+j][i])                   #依次存入温度
                list_table.append(list_days[k+j-1])                         #存入日期
                list_table.append(i)                                        #存入时间
                list_table.append(id)                                       #存入id
                table.append(list_table)
    return table

if __name__ == '__main__':
    df = pd.read_excel('test.xlsx')
    df = df[['day', 'hour', 'temp_avg', 'appliance_id']]
    list_t = day_temp(df,3)
    last_list = []
    for i in list_t:                                                        #删除包含0的数据
        if 0 not in i :
            last_list.append(i)
    df = pd.DataFrame(last_list,columns=['t1','t2','t3','day','hour','appliance_id'])
    df = df.astype(str)
    df.to_excel("forecast.xlsx",index=False)

