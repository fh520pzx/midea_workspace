import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
for i in range(1,2):
    df = pd.read_excel('zone_%s.xlsx'%i)
    x_list = set(df['province'].tolist())
    y_list = range(16,31)
    b=[]
    for j in x_list:
        a=[]
        data=df.loc[df['province'] == j]
        list_tset = data['tset'].tolist()
        for k in y_list:
            if(k in list_tset):
                data1 = data.loc[data['tset']==k]
                a.append(round(np.array(data1['per'])[0],2))
            else:
                a.append(0)
        b.append(a)

    percent = np.array(b)
    percent=percent.transpose()
    fig, ax = plt.subplots(figsize = (30,20))
    im = ax.imshow(percent)
    ax.set_xticks(np.arange(len(x_list)))
    ax.set_yticks(np.arange(len(y_list)))
    ax.set_xticklabels(x_list,fontsize=25)
    ax.set_yticklabels(y_list,fontsize=25)
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
             rotation_mode="anchor")
    for m in range(len(y_list)):
        for n in range(len(x_list)):
            text = ax.text(n, m, percent[m, n],
                           ha="center", va="center", color="w",fontsize=25)
    ax.set_title('zone_%s'%i,fontsize=25)
    fig.tight_layout()
    plt.show()






