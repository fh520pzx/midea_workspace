#计算24小时内的各个温度的运行时间（小时-月份-天数）
#暂时没用
import pandas as pd

df = pd.read_csv(r'D:\MyData\fanghui3\Desktop\27487790780775.txt',delim_whitespace=True)
# df = pd.read_csv(r'D:\MyData\fanghui3\Desktop\test2.txt',delim_whitespace=True)
dtime = df['sampling_time'].astype('str')
sam_time = []
day_flag = []
hour_flag = []
month_flag = []
for i in dtime:
    ti = i[0:4] + '-' + i[4:6] + '-' + i[6:8] + ' ' + i[8:10] + ':' + i[10:12] + ':' + i[12:14]
    day = i[6:8]
    hour = i[8:10]
    month = i[4:6]
    sam_time.append(ti)
    day_flag.append(day)
    hour_flag.append(hour)
    month_flag.append(month)
df['sampling_time'] = sam_time
df['sampling_time'] = pd.to_datetime(df['sampling_time'], format="%Y-%m-%d %H:%M:%S")  # 将时间串转换成标准时间格式
df['day_flag'] = day_flag
df['hour_flag'] = hour_flag
df['month_flag'] = month_flag
df = df.sort_values('sampling_time')
data = df[['sampling_time','tset','day_flag','month_flag']].groupby(df['hour_flag'])            #以小时进行分类
list_name = []
hour_day = []
month_day1 = []
month_day2 = []
hour_month_day_time = []
hour_month_day_tset = []
for name,group in data:
    list_name.append(int(name))
    a1,a2,b,c = [],[],[],[]
    for i in group['sampling_time']:
        a1.append(i)
    for i in group['tset']:
        a2.append(i)
    for i in group['day_flag']:
        b.append(i)
    for i in group['month_flag']:
        c.append(i)
    data1 = pd.DataFrame()
    data1['sampling_time'] = a1
    data1['tset'] = a2
    data1['day_flag'] = b
    data1['month_flag'] = c
    data2 = data1[['sampling_time','tset','day_flag']].groupby(data1['month_flag'])                #以月进行分类
    list_name1 = []
    month_time = []
    month_tset = []
    month_day_time = []
    month_day_tset = []
    for name1,group in data2:
        list_name1.append(int(name1))
        d1,d2,e = [],[],[]
        for i in group['sampling_time']:
            d1.append(i)
        for i in group['tset']:
            d2.append(i)
        for i in group['day_flag']:
            e.append(i)
        data3 = pd.DataFrame()
        data3['sampling_time'] = d1
        data3['tset'] = d2
        data3['day_flag'] = e
        data4 = data3[['sampling_time','tset']].groupby(data3['day_flag'])                  #按天进行分类
        list_name2 = []
        day_time = []
        day_tset = []
        list_month_time = []
        list_month_tset = []
        for name2,group in data4:
            list_name2.append(int(name2))
            f1,f2= [],[]
            for i in group['sampling_time']:
                f1.append(i)
            for i in group['tset']:
                f2.append(i)
            day_time.append(f1)
            day_tset.append(f2)
        dict_1 = dict(zip(list_name2,day_time))
        dict_2 = dict(zip(list_name2,day_tset))
        for i in range(1, 32):
            if i not in dict_1.keys():
                dict_1[i] = []
            if i not in dict_2.keys():
                dict_2[i] = []
        for i in sorted(dict_1):
            list_month_time.append(dict_1[i])
        for i in sorted(dict_2):
            list_month_tset.append(dict_2[i])
        month_time.append(list_month_time)
        month_tset.append(list_month_tset)
    dict2 = dict(zip(list_name1,month_time))
    dict3 = dict(zip(list_name1,month_tset))
    for i in range(1,13):
        if i not in dict2.keys():
            dict2[i] = []
        if i not in dict3.keys():
            dict3[i] = []
    for i in sorted(dict2):
        month_day_time.append(dict2[i])
    for i in sorted(dict3):
        month_day_tset.append(dict3[i])
    month_day1.append(month_day_time)
    month_day2.append(month_day_tset)
dict4 = dict(zip(list_name,month_day1))
dict5 = dict(zip(list_name,month_day2))
for i in range(24):
    if i not in dict4.keys():
        dict4[i] = []
    if i not in dict5.keys():
        dict5[i] = []
for i in sorted(dict4):
    hour_month_day_time.append(dict4[i])
for i in sorted(dict5):
    hour_month_day_tset.append(dict5[i])
# print(len(hour_month_day_tset))
# print(hour_month_day_tset)

time = []
temp = []
for i in range(24):
    time1 = []
    temp1 = []
    if(len(hour_month_day_tset[i])!=0):              #说明当前小时是有数据的
        time_differ = []
        tempset = []
        for j in range(len(hour_month_day_tset[i])):
            if(hour_month_day_tset[i][j]!=[]):
                for k in range(len(hour_month_day_tset[i][j])):
                    if(hour_month_day_tset[i][j][k]!=[]):
                        # time_differ = []
                        # tempset = []
                        hmd_ti = hour_month_day_time[i][j][k]
                        hmd_ts = hour_month_day_tset[i][j][k]
                        for m in range(len(hmd_ti) - 1):
                            tempset.append(hmd_ts[m])
                            time_differ.append((hmd_ti[m + 1] - hmd_ti[m]).seconds)
        for x in tempset:
            temp1.append(x)
        for y in time_differ:
            time1.append(y)
    time.append(time1)
    temp.append(temp1)
# print(time)
# print(temp)

for i in range(24):
    tset_time = {}
    for j, k in zip(temp[i], time[i]):
        if j not in tset_time.keys():
            tset_time[j] = k
        else:
            tset_time[j] = tset_time[j] + k
    print(i,tset_time)

















