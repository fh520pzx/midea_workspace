import pandas as pd
import numpy as np
import favourite_temp
def day_temp(data,da,n):                                               #传入两个值，data是初始的dateframe，da代表根据几天进行预测,n代表根据多少小时预测
    table = []
    list_id = data['appliance_id'].unique()
    for id in list_id:
        new_data = data.query('appliance_id == %s' % id)
        list_days = new_data['day'].unique()  # 日期列表
        # print(list_days)      保存的是年月日
        total_temp = []
        for day in list_days:  # 每个日期对应的0时到23时的温度列表
            month = int(day.split('-')[1])
            days = int(day.split('-')[2])
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
                    temp.append(favourite_temp.favourite(month,days,j,n))
                    # temp.append(0)
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
    print("完成")
    return table

if __name__ == '__main__':
    # list_t = day_temp(df,3,3)
    # print(list_t)
    df = pd.read_excel('forecast_1_test.xlsx')
    df = df[['day', 'hour', 'temp_avg', 'appliance_id']]
    for i in range(5,12,2):
        total = 0
        list_t = day_temp(df, 3,i)                #以三天为例
        length = len(list_t)
        for j in list_t:
            if 0 in j[0:3] :                      #有0的数据，这儿的3与方法里面的3对应，可手动设置变量
                total = total + 1
        print(length)
        print(total)
        print("%s:缺失率为%f"%(i,total/length))
        data = pd.DataFrame(list_t, columns=['t1', 't2', 't3', 'day', 'hour', 'appliance_id'])         #以3天为例所以添加了表头t1-t3，可以不要
        data = data.astype(str)
        data.to_excel("forecast_2_%s.xlsx"%i, index=False)