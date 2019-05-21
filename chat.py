import os
import pandas as pd
from sqlalchemy import  create_engine

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8mb4')
# engine = create_engine('mysql+pymysql://root:123456@10.133.229.100:3306/recommend?charset=utf8mb4')
def jd_chat_date(path):
    content = []
    total = []
    fobj = open(path, 'r', encoding='utf-8-sig')
    for eachline in fobj:
        content.append(eachline.strip())     #content是所有文本
    # print(len(content))                        #文本行数
    start_index = []
    end_index = []

    for i in range(len(content)):             #统计每一个文件里面产生了多少个对话
        if '以下为一通会话' in content[i]:
            start_index.append(i + 1)
        if '会话结束' in content[i]:
            end_index.append(i)


#cus客户 ser客服
    for i in range(len(start_index)):
        ser = ''
        start = start_index[i]
        end = end_index[i]
        try:
            for i in range(start, end):
                cus_name = content[i].split(' ')[0]          #获得用客户名称
                cur_time = content[i].split(' ')[1].split('-')[0]+'-'  #获得时间，用来确定文本中哪一行是识别客户和客服的行
                # print(cur_time)
                # print(cus_name)
                if cus_name and cur_time in content[i]:
                    cus = cus_name
                    break
        except IndexError:
            pass
        # 获得客户和客服的名字
        for i in range(start, end):
            if cur_time in content[i]:
                if content[i].split(' ')[0] != cus:
                    ser = content[i].split(' ')[0]
            else:
                pass
        for k in range(start, end):
            if cur_time in content[k]:
                current_person = content[k].split(' ')[0]
                current_time = ' '.join(content[k].split(' ')[1:])
                pass
            else:
                sub = []
                if current_person == cus:
                    sub.append(cus)
                    sub.append(ser)
                    sub.append('user')
                    sub.append(cus)
                    sub.append(content[k])
                    sub.append(current_time)
                else:
                    sub.append(cus)
                    sub.append(ser)
                    sub.append('rep')
                    sub.append(ser)
                    sub.append(content[k])
                    sub.append(current_time)
                total.append(sub)
    df = pd.DataFrame(total, columns=['tid', 'repid', 'type', 'from', 'content', 'chat_time'])
    df = df.astype('str')
    return df


def loop_file():
    filepath = r'D:\MyData\fanghui3\Desktop\京东数据\聊天记录'
    file = os.listdir(filepath)
    # print(file)
    for i in file:
        # df_list = []
        path = os.path.join(filepath,i)
        pathDir = os.listdir(path)
        for j in pathDir:
            df_list = []
            last_path = os.path.join(path,j)
            print(last_path)
            sub_df = jd_chat_date(last_path)
            sub_df['客服账号名称'] = i
            # df_list.append(sub_df)
            # total_df = pd.concat(df_list)
            # total_df = pd.concat(sub_df)
            pd.io.sql.to_sql(sub_df,'chat_data',con=engine,if_exists='append',index=False)
            print("%s已经成功写入数据库"%j)

        # total_df.to_excel('%s.xlsx'%i, encoding='utf-8-sig', index=False, header=True)


if __name__ == '__main__':
    loop_file()




