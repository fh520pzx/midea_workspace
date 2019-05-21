import requests
import json
import pandas as pd
import threading
import multiprocessing
def getintent(question):
    url='http://120.78.120.141:3000/classifier'
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "e5b5f72d-ec63-6c92-eae1-8006b6d05c5d"
        }
    req='{"sentence":"'+question+'","offline":"1"}'

    resp = requests.request("POST", url, data=req.encode(encoding='UTF-8'), headers=headers)
    intentlevel1=json.loads(resp.text)
    return intentlevel1
def run(a,b):
    data = pd.read_excel(r'D:\MyData\fanghui3\Desktop\12-31.xlsx')
    question = []
    sentence = []
    intent = []
    data = data['content']
    for i in data:
        question.append(i)
    for i in range(a,b):
        if i > len(data):
            break
        try:
            sent = getintent(question[i])['sentence']
            inte = getintent(question[i])['intent']
        except Exception as e:
            intent.append(e)
            sentence.append(sent)
            dataset = list(zip(sentence, intent))
            df = pd.DataFrame(data=dataset, columns=['content', 'intent'])
            df.to_excel("%d.xlsx" % a, index=False)
        else:
            intent.append(inte)
            sentence.append(sent)
            dataset = list(zip(sentence, intent))
            df = pd.DataFrame(data=dataset, columns=['content', 'intent'])
            df.to_excel("%d.xlsx"%a,index=False)
        print(i)

if __name__=='__main__':
    run(536,26031)