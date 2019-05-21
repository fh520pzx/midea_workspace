#已知具体时间（月日时）,得到以该时间为期待，num小时为跨度的，运行时间最长的温度
import pandas as pd
import favourite_temp_3
def temp_totaltime(month_hour_time, month_hour_tset, month, day, hours, num):
    """
    :param month_day_hour_time: 月份_天_小时_空调运行时间字典
    :param month_day_hour_tset: 月份_天_小时_空调温度设定字典
    :param month: 月份
    :param day: 第几天
    :param hours: 小时
    :param num: 以几个小时为周期
    :return: 返回规定时间内运行时间最长的温度
    """
    list_time = []
    list_tset = []
    hour_time = month_hour_time[month - 1][day - 1]
    hour_tset = month_hour_tset[month - 1][day - 1]
    if(hour_time!=[]):                                        #如果某月某天是有数据的，则得到该天某个小时的一段时间内的持续时间最长的温度
        if (hours + num <= 23):
            for i in range(num):
                for j in hour_time[hours + i]:
                    list_time.append(j)
                for k in hour_tset[hours + i]:
                    list_tset.append(k)
        else:
            for i in range(num):
                for j in hour_time[hours - i]:
                    list_time.append(j)
                for k in hour_tset[hours - i]:
                    list_tset.append(k)
        time_differ = []
        tempset = []
        for i in range(len(list_time)-1):
            tempset.append(list_tset[i])
            time_differ.append((list_time[i+1]-list_time[i]).seconds)
        tset_time = {}
        for i,j in zip(tempset,time_differ):
            if i not in tset_time.keys():
                tset_time[i] = j
            else:
                tset_time[i] = tset_time[i] + j
        key_name = max(tset_time, key=tset_time.get,default=0)             #获得字典中值最大的相对应的键，获得温度持续时间最长的温度
        # return key_name
    else:                                                       #如果某月某天没有数据。就使用前几天的这个时刻的持续时间最长的温度
        time = '2018'+'-'+str(month)+'-'+str(day)
        hour_tset_time = favourite_temp_3.ts_time(time,7)
        if (hour_tset_time.get(hours)!=None):
            last_ts_ti = hour_tset_time.get(hours)
            key_name = max(last_ts_ti, key=last_ts_ti.get, default=0)
        else:
            key_name = 0
    return key_name


def favourite(months,days,hours,n):
    df = pd.read_csv(r'D:\MyData\fanghui3\Desktop\27487790780775.txt',delim_whitespace=True)
    # df = pd.read_csv(r'D:\MyData\fanghui3\Desktop\test1.txt', delim_whitespace=True)
    dtime = df['sampling_time'].astype('str')
    sam_time = []
    hour_flag = []
    month_flag = []
    day_flag = []
    for i in dtime:
        ti = i[0:4] + '-' + i[4:6] + '-' + i[6:8] + ' ' + i[8:10] + ':' + i[10:12] + ':' + i[12:14]
        month = i[4:6]
        day = i[6:8]
        hour = i[8:10]
        sam_time.append(ti)
        hour_flag.append(hour)
        month_flag.append(month)
        day_flag.append(day)
    df['sampling_time'] = sam_time
    df['sampling_time'] = pd.to_datetime(df['sampling_time'], format="%Y-%m-%d %H:%M:%S")  # 将时间串转换成标准时间格式
    df['hour_flag'] = hour_flag
    df['month_flag'] = month_flag
    df['day_flag'] = day_flag

    list_id = df['appliance_id'].unique()
    for id in list_id:
        data = df.query('appliance_id == %s' % id)
        data = data.sort_values('sampling_time')
        list_hour = []
        list_day = []
        month_sampling = []  # 保存1-12月每天空调运行时刻
        month_tset = []  # 保存1-12月每天空调的温度设置情况
        list_name1 = []
        month_day_hour_time = []
        month_day_hour_tset = []
        data1 = data[['sampling_time', 'tset', 'hour_flag', 'day_flag']].groupby(data['month_flag'])  # 通过月份进行分类
        for name1, group in data1:
            list_name1.append(int(name1))
            a, b, c, d = [], [], [], []
            for i in group['sampling_time']:
                a.append(i)
            for i in group['tset']:
                b.append(i)
            for i in group['hour_flag']:
                c.append(i)
            for i in group['day_flag']:
                d.append(i)
            da = pd.DataFrame()
            da['sampling_time'] = a
            da['tset'] = b
            da['hour_flag'] = c
            da['day_flag'] = d
            list_name2 = []
            day_sampling = []
            day_tset = []
            day_hour_time = []
            day_hour_tset = []
            da1 = da[['sampling_time', 'tset', 'hour_flag']].groupby(da['day_flag'])  # 通过天进行分类
            for name2, group in da1:
                list_name2.append(int(name2))
                e, f, g = [], [], []
                for i in group['sampling_time']:
                    e.append(i)
                for i in group['tset']:
                    f.append(i)
                for i in group['hour_flag']:
                    g.append(i)
                da2 = pd.DataFrame()
                da2['sampling_time'] = e
                da2['tset'] = f
                da2['hour_flag'] = g
                da3 = da2[['sampling_time', 'tset']].groupby(da2['hour_flag'])  # 通过小时进行分类
                list_name3 = []
                hour_ti = []
                hour_ts = []
                for name3, group in da3:
                    list_name3.append(int(name3))
                    s, t = [], []
                    for i in group['sampling_time']:
                        s.append(i)
                    hour_ti.append(s)
                    for i in group['tset']:
                        t.append(i)
                    hour_ts.append(t)
                dict1 = dict(zip(list_name3, hour_ti))
                dict2 = dict(zip(list_name3, hour_ts))
                hour_sampling = []  # 保存从0-23时刻的时间
                hour_tset = []  # 保存从0-23时刻的温度设置
                for i in range(24):
                    if i not in dict1.keys():
                        dict1[i] = []
                    if i not in dict2.keys():
                        dict2[i] = []
                for i in sorted(dict1):
                    hour_sampling.append(dict1[i])
                for j in sorted(dict2):
                    hour_tset.append(dict2[j])
                day_sampling.append(hour_sampling)
                day_tset.append(hour_tset)
            dict_day_sampling = dict(zip(list_name2, day_sampling))
            dict_day_tset = dict(zip(list_name2, day_tset))
            for i in range(1, 32):
                if i not in dict_day_sampling.keys():
                    dict_day_sampling[i] = []
                if i not in dict_day_tset.keys():
                    dict_day_tset[i] = []
            for i in sorted(dict_day_sampling):
                day_hour_time.append(dict_day_sampling[i])
            for i in sorted(dict_day_tset):
                day_hour_tset.append(dict_day_tset[i])
            month_sampling.append(day_hour_time)
            month_tset.append(day_hour_tset)
        dict_month_time = dict(zip(list_name1, month_sampling))
        dict_month_tset = dict(zip(list_name1, month_tset))
        for i in range(1, 13):
            if i not in dict_month_time.keys():
                dict_month_time[i] = []
            if i not in dict_month_tset.keys():
                dict_month_tset[i] = []
        for i in sorted(dict_month_time):
            month_day_hour_time.append(dict_month_time[i])
        for i in sorted(dict_month_tset):
            month_day_hour_tset.append(dict_month_tset[i])
        temp = temp_totaltime(month_day_hour_time, month_day_hour_tset, months, days, hours, n)
        return temp









