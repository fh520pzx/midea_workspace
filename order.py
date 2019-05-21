import os
import pandas as pd
def search(path):
    order = []
    parents = os.listdir(path)
    for parent in parents:                              # 返回指定路径下所有文件和文件夹的名字，并存放于一个列表中
        child = os.path.join(path,parent)
        if os.path.isdir(child):                       # 将多个路径组合后返回
            search(child)
        elif os.path.isfile(child):                    # 如果是目录，则继续遍历子目录的文件
            if os.path.splitext(child)[1] == '.xlsx':   # 分割文件名和文件扩展名，并且扩展名为'xlsx'
                d = pd.read_excel(child,dtype=str)
                order.append(d)
    return order

def run(list):
    order_all = []
    for i in list:
        path = r'D:\MyData\fanghui3\Desktop\京东数据\订单\%s'%i
        df = search(path)
        df = pd.concat(df)
        df['客服账号名称']=i
        order_all.append(df)
    return order_all


if __name__ == '__main__':
    dirs = os.listdir(r'D:\MyData\fanghui3\Desktop\京东数据\订单')
    df = pd.concat(run(dirs))
    df.to_excel('汇总.xlsx',index=False)
