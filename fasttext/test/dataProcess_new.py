
labels = []
categroy = {}
data_result = []
count = 0
print('process 3.txt!')
#with open("../3.txt") as fr:
with open("3.txt") as fr:
    for line in fr:
        if "{" in line or "}" in line:
            continue
        else:
            data_result.append(line)
            count += 1
            label = line.split(' ')[0].replace('__label__', '').replace('\n', '')
            if categroy.__contains__(label):
                categroy[label] += 1
            else:
                categroy[label] = 1
            if labels.__contains__(label):
                continue
            else:
                labels.append(label)
print('write data.txt')
f = open('data.txt', 'w', encoding='utf-8')
f.write(''.join(data_result))
f.close()
print(categroy)  #训练数据类别及数目
print('data process success!')
print(count)

data_test = []
data_train = []
A = dict.fromkeys(labels, 0)
print('read data.txt')
with open("data.txt") as fr:
    for line in fr:
        label = line.split(' ')[0].replace('__label__', '').replace('\n', '')
        if categroy[label] < 1200000:  #过滤掉小于1万的数据
            continue
        A[label] += 1
        if A[label] <= 300000:  #从每个类中取1000条作为测试数据
            data_test.append(line)
        else:
            data_train.append(line)
print('write test.txt')
f = open('test.txt', 'w', encoding='utf-8')
f.write(''.join(data_test))
f.close()
print('write train.txt')
f = open('train.txt', 'w', encoding='utf-8')
f.write(''.join(data_train))
f.close()
print('OK')

