#找到每个设备每次开机的2个小时之内的数据，然后打上对应的第几次开机的flag
#找到室内温度第一次和设定温度的差值在[正负0.5或正负1度]的时刻
import pandas as pd
import time
import datetime
def temp_differ(diff):
    """
    :param diff: 温差：室内温度与设定温度
    :return:满足条件的Dataframe
    """
    frames = []
    id_tset_time = []
    df = pd.read_csv(r'D:\MyData\fanghui3\Desktop\data\t_aeaf_join.txt',delim_whitespace=True)
    list_id = df['appliance_id'].unique()
    # print(list_id)
    # print(list_id)
    list_id = list_id
    for id in list_id:
        differ = []   #保存找到室内与设定温度满足条件的时间间隔
        data = df.query('appliance_id == %s'%id)
        data = data.sort_values('a_dt')
        list_runstatus,list_adt = [],[]
        list_appid,list_tempset, list_runstatus, list_modeset, list_windspeedset, list_adt, list_tin, list_tout, list_humidity, list_flag = [],[], [], [], [], [], [], [], [], []
        appliance_id,tempset, runstatus, modeset, windspeedset, adt, tin, tout, humidity, flag,f_tin = [],[],[],[],[],[],[],[],[],[],[]
        list_flag = []
        start_tin = []
        index = []
        index_new = []
        all_index = []
        for i in data['appliance_id']:
            list_appid.append(i)
        for i in data['tempset']:
            list_tempset.append(i)
        for i in data['runstatus']:
            list_runstatus.append(i)
        for i in data['modeset']:
            list_modeset.append(i)
        for i in data['windspeedset']:
            list_windspeedset.append(i)
        for i in data['tin']:
            list_tin.append(i)
        for i in data['tout']:
            list_tout.append(i)
        for i in data['humidity']:
            list_humidity.append(i)


        for i in data['a_dt']:
            ltime = time.localtime(i / 1000)
            timeYMD = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
            list_adt.append(timeYMD)
        data['a_dt'] = list_adt

        for i in range(len(list_runstatus)):
            list_flag.append(0)
            start_tin.append(0)

        for i in range(len(list_runstatus)-1):
            if (list_runstatus[i]==0 and list_runstatus[i+1]==1):          #一次开机状态 并且需要每次开机时间大于半个小时
                index.append(i+1)                                          #保存的为开机状态的数组位置


        num = 0
        for i in range(len(index)-1):
            num=num+1
            for j in range(index[i],index[i+1]):
                list_flag[j] = num
                start_tin[j] = list_tin[index[i]]
            x = num+1
        print(x)
        print(index[-1],len(list_runstatus))
        for i in range(index[-1],len(list_runstatus)):

            list_flag[i] = x
            start_tin[i] = list_tin[index[-1]]
        data['flag'] = list_flag
        data['tin_f'] = start_tin

        for i in range(len(index)-1):
            t1 = pd.to_datetime(list_adt[index[i]], format="%Y-%m-%d %H:%M:%S")
            t2 = pd.to_datetime(list_adt[index[i+1]], format="%Y-%m-%d %H:%M:%S")
            time_differ = (t2-t1).total_seconds()                        #计算两次开机时间之间的间隔
            if(time_differ>1800):                                        #开机时间持续30分钟，则满足要求
                index_new.append(index[i])
        index_new.append(index[-1])

        id_list = []
        tset_list = []
        time_list = []

        #取每次开机两小时内的数据
        for i in range(len(index_new) - 1):
            n=0
            tset = list_tempset[index_new[i]]                  #每次开机的温度
            t = pd.to_datetime(list_adt[index_new[i]], format="%Y-%m-%d %H:%M:%S")     #开始时间
            # print(t)
            t_last = t + datetime.timedelta(hours=2)                                   #两小时限制时间
            for j in range(index_new[i],index_new[i+1]):            #两个开机时间之间
                list_adt[j] = pd.to_datetime(list_adt[j], format="%Y-%m-%d %H:%M:%S")
                if(list_adt[j]<t_last and n==0):
                    all_index.append(j)
                    if (abs(tset-list_tin[j])==diff ):
                        n+=1
                        if(n==1):                      #n控制的为第一次温度相等
                            # print((list_adt[j]-t).total_seconds())
                            # id_list.append(id)
                            # tset_list.append(tset)
                            differ.append(int((list_adt[j]-t).total_seconds()))
            # if(n==0):
            #     differ.append(-1)
            # print('___________________________')

        m = 0
        for i in range(index_new[-1],len(list_adt)):                #对于最后一个处理
            tset = list_tempset[index_new[-1]]               #开机温度
            t = pd.to_datetime(list_adt[index_new[-1]], format="%Y-%m-%d %H:%M:%S")  #开始时间
            t_last = t + datetime.timedelta(hours=2)
            list_adt[i] = pd.to_datetime(list_adt[i], format="%Y-%m-%d %H:%M:%S")
            if(list_adt[i]<t_last and m==0):
                all_index.append(i)
                if (abs(tset - list_tin[i]) == diff):
                    m += 1
                    if (m == 1):
                        # print((list_adt[i]-t).total_seconds())
                        # id_list.append(id)
                        # tset_list.append(tset)
                        differ.append(int((list_adt[i]-t).total_seconds()))
                        
        # if(m==0):
        #     differ.append(-1)

        print(all_index)

        test = pd.DataFrame()
        test['appliance_id'] = id_list
        test['tset'] = tset_list
        test['differ_time'] = differ
        test = test.astype('str')
        id_tset_time.append(test)

        for i in all_index:
            appliance_id.append(list_appid[i])
            tempset.append(list_tempset[i])
            runstatus.append(list_runstatus[i])
            modeset.append(list_modeset[i])
            windspeedset.append(list_windspeedset[i])
            adt.append(list_adt[i])
            tin.append(list_tin[i])
            tout.append(list_tout[i])
            humidity.append(list_humidity[i])
            flag.append(list_flag[i])
            f_tin.append(start_tin[i])
        data_new = pd.DataFrame()
        data_new['appliance_id'] = appliance_id
        data_new['tempset'] = tempset
        data_new['runstatus'] = runstatus
        data_new['modeset'] = modeset
        data_new['windspeedset'] = windspeedset
        data_new['adt'] = adt
        data_new['tin'] = tin
        data_new['tin_f'] = f_tin
        data_new['tout'] = tout
        data_new['humidity'] = humidity
        data_new['flag'] = flag
        data_new = data_new.astype('str')
        frames.append(data_new)
        # print(differ)
        print('**********************************')
    result = pd.concat(frames)
    # return result
    result.to_excel('high_frequency.xlsx',index=False)
    # result2 = pd.concat(id_tset_time)
    # result2.to_excel('%s.xlsx'%diff,index=False)

if __name__ == '__main__':
    temp_differ(0.5)




