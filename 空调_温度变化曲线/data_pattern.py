import pandas as pd
import time
df = pd.read_excel('high_frequency.xlsx')
list_flag = df['flag'].unique()

list_id = df['appliance_id'].unique()
last = []
for id in list_id:
    all = []
    data1 = df.query('appliance_id == %s' % id)
    list_flag = data1['flag'].unique()
    for flag in list_flag:
        data = data1.query('flag == %s' % flag)
        list_appid, list_tempset, list_modeset, list_adt, list_tin,list_tinf = [], [], [], [], [],[]
        for i in data['appliance_id']:
            list_appid.append(i)
        for i in data['tempset']:
            list_tempset.append(i)
        for i in data['modeset']:
            list_modeset.append(i)
        for i in data['tin']:
            list_tin.append(i)
        for i in data['tin_f']:
            list_tinf.append(i)

        for i in data['adt']:
            list_adt.append(i)

        differ_time = []
        for i in range(len(list_tempset)):
            if (i==0):
                differ_time.append(0)
            else:
                t1 = pd.to_datetime(list_adt[i-1], format="%Y-%m-%d %H:%M:%S")
                t2 = pd.to_datetime(list_adt[i], format="%Y-%m-%d %H:%M:%S")
                differ_time.append((t2-t1).seconds)
        s = 0
        x=[]
        for i in range(len(differ_time)):
            s = s + differ_time[i]
            x.append(s)
        data['time'] = x
        data = data.astype('str')
        all.append(data)
    result = pd.concat(all)
    last.append(result)
result2 = pd.concat(last)
result2.to_excel('all.xlsx',index = False)




