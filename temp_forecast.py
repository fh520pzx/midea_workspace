import pandas as pd
import numpy as np
import datetime
import time
df = pd.read_csv(r'D:\MyData\fanghui3\Desktop\27487790780775.txt',delim_whitespace=True)
# df = pd.read_csv(r'D:\MyData\fanghui3\Desktop\112.txt',delim_whitespace=True)
df = df.sort_values('sampling_time')

dtime = df['sampling_time'].astype('str')
sam_time = []
time_flag = []
for i in dtime:
    ti = i[0:4]+'-'+i[4:6]+'-'+i[6:8]+' '+i[8:10]+':'+i[10:12]+':'+i[12:14]
    j = i[0:4]+'-'+i[4:6]+'-'+i[6:8]+' '+i[8:10]
    sam_time.append(ti)
    time_flag.append(j)
df['sampling_time'] = sam_time
df['sampling_time'] = pd.to_datetime(df['sampling_time'],format="%Y-%m-%d %H:%M:%S")             #将时间串转换成标准时间格式
df['time_flag'] = time_flag                                                                      #设置一个用来分组的时间标记，设置到小时
list_id = df['appliance_id'].unique()                                                            #以设备id作为分组依据


for id in list_id:
    data = df.query('appliance_id == %s' % id)
    list_time = data['time_flag'].unique()
    list_day = []
    list_hour = []
    for i in list_time:                                                                          #获得每天每小时的数组
        list_day.append(i.split(' ')[0])
        list_hour.append(i.split(' ')[1])


    data1 = data['tset'].groupby(data['time_flag'])                                              #以时间标记为依据进行分组得到tset
    data2 = data[['sampling_time','tset']].groupby(data['time_flag'])                            #以时间标记为依据进行分组得到'sampling_time','tset'

    avg_temp = []
    shijian = []
    wendu = []
    for name,group in data2:
        total_tem = 0
        a= []
        b = []
        for i in group['sampling_time']:
            a.append(i)
        shijian.append(a)
        for j in group['tset']:
            b.append(j)
        wendu.append(b)

    for i in range(len(shijian)):                                  #计算平均温度
        total_tem = 0.0
        hours = 0
        for t in range(len(shijian[i])):
            k = t + 1
            if (k > len(shijian[i]) - 1 and (i + 1) <= len(shijian) - 1):
                hour = ((shijian[i + 1][0] - shijian[i][t]).seconds) / 3600
            elif (k > len(shijian[i]) - 1 and (i + 1) > len(shijian) - 1):
                temp = (shijian[i][t] + datetime.timedelta(hours=+1)).strftime("%Y-%m-%d %H") + ":00:00"
                hour1 = datetime.datetime.strptime(temp, "%Y-%m-%d %H:%M:%S")
                hour = ((hour1 - shijian[i][t]).seconds) / 3600
            else:
                hour = ((shijian[i][k] - shijian[i][t]).seconds) / 3600
            total_tem += hour * wendu[i][t]
            hours += hour
            try:
                avg_t = total_tem / hours
            except ZeroDivisionError:
                pass
        avg_temp.append(avg_t)

    min = data1.min()
    max = data1.max()
    std = data1.std()
    avg = data1.mean()
    da = pd.DataFrame({'max':max,'min':min,'max-min':max-min,'std':std,'avg':avg,'appliance_id':id,'day':list_day,'hour':list_hour,'temp_avg':avg_temp})
    da.reset_index(inplace=True)
    da['appliance_id'].astype('str')
    da.drop(columns='time_flag',inplace=True)
    da.to_excel('test.xlsx',index=False)




