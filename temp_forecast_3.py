import pandas as pd
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv(r'D:\MyData\fanghui3\Desktop\liyu_data.txt',delim_whitespace=True)
list_id = df['applianceID'].unique()
list_id = list_id[0:10]                         #取十个设备


def picture(x,y1,y2,n):                             #画折线图
    fig = plt.figure(figsize=(15, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))  # 设置时间标签显示格式
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.set_title("%s-%s" % (id, n+1))
    ax.plot(x, y1,linewidth=1,color='red', label='tempset')
    ax.plot(x, y2, linewidth=1, color='blue', label='tin')
    plt.xticks(rotation=45)  # 旋转45度显示
    plt.legend()  # 显示图例
    plt.show()

def sameFactor(List):         #判断一个数组里面的元素是否完全相同
    if len(set(List))!=1:
        return 1
    else:
        return 0


for id in list_id:
    data = df.query('applianceID == %s'%id)
    data = data.sort_values('dt')
    list_dt = []
    for i in data['dt']:
        ltime = time.localtime(i / 1000)
        timeYMD = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
        list_dt.append(str(timeYMD))
    data['dt'] = list_dt
    list_status = []
    list_time = []
    list_tset = []
    list_tin = []
    number = []
    for i in data['runstatus']:
        list_status.append(i)
    for i in data['dt']:
        list_time.append(i)
    for i in data['tempset']:
        list_tset.append(i)
    for i in data['tin']:
        list_tin.append(i)

    #统计从第一段时间
    for j in range(len(list_status)-1):
        if (list_status[j] == 0 and list_status[j + 1] == 1):             #找到运行状态从0变成1的时刻
            number.append(j)                                              #保存的是出现的位置

    for i in range(len(number)-1):                          #i代表的是第几次开机
        num = i
        x = []
        x_new = []
        y_ts = []
        y_tin = []
        for j in range(number[i],number[i+1]):        #j代表的是出现的位置
            x.append(list_time[j])
            y_ts.append(list_tset[j])
            y_tin.append(list_tin[j])

        for k in x:
            start_date = datetime.datetime.strptime(k, "%Y-%m-%d %H:%M:%S")
            x_new.append(start_date)
        if (sameFactor(y_ts)==1):
            picture(x_new,y_ts,y_tin,num)


    #统计最后一段时间段的情况
    x1 = []
    x1_new = []
    y1_ts = []
    y1_tin = []
    for j in range(number[len(number)-1],len(list_status)):
        x1.append(list_time[j])
        y1_ts.append(list_tset[j])
        y1_tin.append(list_tin[j])
    for i in x1:
        start_date = datetime.datetime.strptime(i,"%Y-%m-%d %H:%M:%S")
        x1_new.append(start_date)
    if (sameFactor(y1_ts) == 1):
        picture(x1_new,y1_ts,y1_tin,num+1)










