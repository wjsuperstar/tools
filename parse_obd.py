import re
import sys
import json
from collections import defaultdict

print("使用格式： python xx.py 文件名")
print("param:", sys.argv[1])

FileName = sys.argv[1]
ErrorDevidList = []
ErrorDict=defaultdict(list)

def get_all_dict(data):
    if isinstance(data,list):
        data = data[0]
    if isinstance(data,dict):
        for x in range(len(data)): 
            temp_key = list(data.keys())[x] 
            temp_value = data[temp_key]
            if not (isinstance(temp_value, list) or isinstance(temp_value, dict)):
                #print('{} : {}'.format(temp_key,temp_value))
                print('%-8s : %-32s' % (temp_key, temp_value), end=';')
            
            get_all_dict(temp_value) # 迭代输出结果

def parse_file():
    with open(FileName, encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:
                break
            #data = re.search('(?<=Boby:\[)(.*)(?=\],\sHttpRecv)', line).group(1)
            #data2 = re.search('(?<=HttpRecv:\[)(.*)', line).group(1)
            devid = re.search('DevID:(.*?),', line).group(1)
            #print('devid=', devid)
            data = re.search('Boby:\[(.*)\],\sHttpRecv:\[(.*)\]', line)
            js1 = json.loads(data.group(1))
            js2 = json.loads(data.group(2))
            ss1=js2['body'][0]['error']
            
            if ss1[0:4] == '[Wd]' or ss1[0:4] == '[Jd]' :
                #print('DevId=', devid, ss1, 'JD=', js1['body']['JD'], 'WD=', js1['body']['WD'])
                ErrorDevidList.append(devid)
            
            ErrorDict[devid].append(ss1+' '+js1['body']['JD']+' '+js1['body']['WD'])
            
            #get_all_dict(js1)
            #get_all_dict(js2)
            #print('\n')
            #break;
if __name__ == '__main__':
    parse_file()
    
    for key, value in ErrorDict.items():
        if key in ErrorDevidList:
            for i in value:
                print('devID:', key, ":", i)
    
        
    