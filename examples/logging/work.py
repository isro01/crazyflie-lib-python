import pandas as pd 
import re

time =[]
range0=[]
data_line=[]
with open("test_range_data.log", "r") as f:
    # line = f.readline()
    # print(line)
    # res = re.split('{|: |, ', line)
    # print(res)


    # while line:
    #     # print(line)
        # line = f.readline()
    for line in f.readlines():
        # time.append(line.split("{")[0])
        # if "Closing" in str(line):
        #     exit
        res = re.split('{|: |, ', line)
        # print(res[2])
        # print("\n")
        # range0.append(res[2])
        data_line.append([res[0], res[2], res[4], res[6]])
        # data_line.append(res[4])
        # data_line.append(res[6])


print(data_line[0])
# data = [time, range0]
df = pd.DataFrame(data_line, columns=['timestamp','ranging.distance0','ranging.distance2', 'ranging.distance3'])

df.to_excel('test.xlsx', sheet_name='test')
