# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np

#去重保存到新的文件
# df = pd.read_excel(r'D:\MyData\fanghui3\Desktop\work4_4\第二轮语料标注及attr_word补充.xlsx','Sheet2')
# df_new = df.drop_duplicates()
# df_new.to_excel(r'D:\MyData\fanghui3\Desktop\work4_4\new.xlsx',index=False)

data1 = pd.read_excel(r'D:\MyData\fanghui3\Desktop\work4_4\recommend_re_map_new0401.xlsx')

data2 = pd.read_excel(r'D:\MyData\fanghui3\Desktop\work4_4\new.xlsx')

#形成4对1的字典
def creatdict(name):
    cat_id = np.array(name['Categoryid']).tolist()
    attr_n = np.array(name['attr_name']).tolist()
    value_n = np.array(name['value_name']).tolist()
    flag1 = np.array(name['flag']).tolist()
    flag = []
    for i in flag1:
        flag.append(str(i))
    attr_w = np.array(name['attr_word']).tolist()
    ls = []
    for i in range(len(attr_w)):
        ls.append(str(attr_w[i]).split('#'))               #分割attr_word中的单词
    list1 = list(zip(cat_id,attr_n,value_n,flag))
    dict1 = dict(zip(list1, ls))


    return dict1

def dictmerged(dica,dicb):                                 #两个字典合并去重
    dic={}
    for i in dicb:
        if dica.get(i):
            list = dica[i]
            li = dicb[i]
            for j in li:
                list.append(j)
            list1 = []
            for k in list:
                if k not in list1:
                    list1.append(k)
                else:
                    continue
            dic[i] = list1
        else:
            dic[i]=dicb[i]
    for i in dica:
        if dicb.get(i):
            pass
        else:
            dic[i] = dica[i]
    return dic

if __name__ == '__main__':
    list_old = creatdict(data1)      #初始表的字典
    list_extend = creatdict(data2)   #附加表的字典

    dict_new = dictmerged(list_old,list_extend)
    list_values = dict_new.values()
    # 每一个value值都是一个数组
    list1 = []
    for i in list_values:
        list1.append('#'.join(i))
    dict = dict(zip(dict_new.keys(),list1))   #合并后的字典

    # print(dict)
    list_last = []
    for i in dict.keys():
        value = dict[i]
        i = list(i)
        i.append(value)
        list_last.append(i)

    df = pd.DataFrame(list_last,columns=['Categoryid','attr_name','value_name','flag','attr_word'])

    data3 = pd.read_excel(r'D:\MyData\fanghui3\Desktop\work4_4\categorynamemap.xlsx')
    category= data3.set_index('category_id').to_dict()['category_name'] #建立的字典
    df['Category'] = df['Categoryid'].map(category)


    att = df['attr_word']
    att = ['' if x == 'nan' else x for x in att]    #将attr_word中的nan替换成空字符
    df['attr_word'] = att

    cols = list(df)                                 #将attr_word列放在第二列
    cols.insert(1, cols.pop(cols.index('Category')))
    df = df.loc[:, cols]


    df.to_excel(r'汇总.xlsx', index=False)


























