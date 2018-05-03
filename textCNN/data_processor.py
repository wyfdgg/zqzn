import numpy as np
import re
import json

def load_data_and_labels(train_data_file):
    texts = []
    labels = []  #所有的label中文名称，没有去重
    #labels_count = 0  #类别数，已去重
    with open(train_data_file) as fr:
        for line in fr:
            text = line[line.find(' ') + 1:]  #文本，不带标签
            label = line.split(' ')[0].replace('__label__', '')
            #if not labels.__contains__(label):
            #    labels_count += 1
            labels.append(label)
            texts.append(text)
            #print(text + label)
    print('read train_data success')

    labels_count = len(set(labels))
    tmp_lbl = {}
    #{'label1': [1, 0, 0, 0], 'label2': [0, 1, 0, 0], 'label3': [0, 0, 1, 0], 'label4': [0, 0, 0, 1]}
    for l in labels:
        if not tmp_lbl.__contains__(l):
            tmp_lbl[l] = [0 for _ in range(0, labels_count)]
            tmp_lbl[l][len(tmp_lbl) - 1] = 1

    jsonObj = json.dumps(tmp_lbl)
    #写文件
    with open('label.json', 'w', encoding='utf-8') as fr:
        fr.write(jsonObj)

    #y = np.concatenate([tmp_lbl[l] for l in labels], 0)  #所有的label（用数组表示）
    y = np.array([tmp_lbl[l] for l in labels])
    return [texts, y]

