#根据两个变量（某一时间点：年月日，天数n），得到从该时间起的前n天的时间范围内的，各个温度持续的时间点
import pandas as pd
import datetime
def ts_time(ymd,day_num):
    dict_last = {}
    time_list = []
    time_last = pd.to_datetime(ymd,format="%Y-%m-%d")
    time_first = time_last-datetime.timedelta(days=day_num)
    while (time_first <= time_last):
        time_list.append(time_first)
        time_first = time_first + datetime.timedelta(days=1)
    df = pd.read_csv(r'D:\MyData\fanghui3\Desktop\27487790780775.txt',delim_whitespace=True)
    # df = pd.read_csv(r'D:\MyData\fanghui3\Desktop\test2.txt',delim_whitespace=True)
    dtime = df['sampling_time'].astype('str')
    sam_time = []
    hour_flag = []
    year_month_day_flag = []
    for i in dtime:
        ti = i[0:4] + '-' + i[4:6] + '-' + i[6:8] + ' ' + i[8:10] + ':' + i[10:12] + ':' + i[12:14]
        hour = i[8:10]
        year_month_day = i[0:4] + '-' + i[4:6] + '-' + i[6:8]
        sam_time.append(ti)
        hour_flag.append(hour)
        year_month_day_flag.append(year_month_day)
    df['sampling_time'] = sam_time
    df['sampling_time'] = pd.to_datetime(df['sampling_time'], format="%Y-%m-%d %H:%M:%S")  # 将时间串转换成标准时间格式
    # for i in df['sampling_time']:
    #     print(i-datetime.timedelta(days=3))
    df['hour_flag'] = hour_flag
    df['year_month_day_flag'] = year_month_day_flag
    # df['year_month_day_flag'] = pd.to_datetime(df['year_month_day_flag'], format="%Y-%m-%d")  # 将时间串转换成标准时间格式
    df = df.sort_values('sampling_time')
    data = df[['sampling_time','tset','year_month_day_flag']].groupby(df['hour_flag'])            #以小时进行分类
    list_name = []
    list_time = []

    for name,group in data:
        list_name.append(int(name))
        tempset = []
        samplingtime = []
        a,b,c = [],[],[]
        for i in group['sampling_time']:
            a.append(i)
        for i in group['tset']:
            b.append(i)
        for i in group['year_month_day_flag']:
            c.append(i)
        data1 = pd.DataFrame()
        data1['sampling_time'] = a
        data1['tset'] = b
        data1['year_month_day_flag'] = c
        data2 = data1[['sampling_time','tset']].groupby(data1['year_month_day_flag'])                #以具体时间（年月日进行分类）
        list_name1 = []
        time = []
        tset = []
        for name1,group in data2:
            list_name1.append(name1)
            d,e = [],[]
            for i in group['sampling_time']:
                d.append(i)
            for i in group['tset']:
                e.append(i)
            time.append(d)
            tset.append(e)
        dict1 = dict(zip(list_name1,time))
        dict2 = dict(zip(list_name1,tset))
        for i in dict1.keys():
            i_new = pd.to_datetime(i, format="%Y-%m-%d")
            if i_new in time_list:
                samplingtime.append(dict1.get(i))
        for i in dict2.keys():
            i_new = pd.to_datetime(i, format="%Y-%m-%d")
            if i_new in time_list:
                tempset.append(dict2.get(i))

        all_tset = []
        all_timediff = []
        for i in range(len(samplingtime)):
            one_samplingtime = samplingtime[i]
            one_tempset = tempset[i]
            time_differ = []
            all_temp = []
            for i in range(len(one_tempset) - 1):
                all_temp.append(one_tempset[i])
                time_differ.append((one_samplingtime[i + 1] - one_samplingtime[i]).seconds)
            for i in all_temp:
                all_tset.append(i)
            for i in time_differ:
                all_timediff.append(i)
        tset_time = {}
        for i, j in zip(all_tset, all_timediff):
            if i not in tset_time.keys():
                tset_time[i] = j
            else:
                tset_time[i] = tset_time[i] + j
        dict_last[int(name)] = tset_time
    # print(dict_last)
    return dict_last
if __name__ == '__main__':
    # print(ts_time('2018-6-10',7))
    date = '2018-6-10'
    days = 7
    for key, value in ts_time(date,days).items():
        print(key,value)
    print(ts_time(date,days).get(25))