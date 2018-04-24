# _*_coding:utf-8 _*_
import sys, getopt

class Processor:
    labels = []
    categroy = {}
    data_result = []
    def formatData(self, filename):
        count = 0
        print('process %s' % filename)
        # with open("../3.txt") as fr:
        with open(filename) as fr:
            for line in fr:
                if "{" in line or "}" in line:
                    continue
                else:
                    self.data_result.append(line)
                    count += 1
                    label = line.split(' ')[0].replace('__label__', '').replace('\n', '')
                    if self.categroy.__contains__(label):
                        self.categroy[label] += 1
                    else:
                        self.categroy[label] = 1
                    if self.labels.__contains__(label):
                        continue
                    else:
                        self.labels.append(label)
        print('write data.txt')
        f = open('data.txt', 'w', encoding='utf-8')
        f.write(''.join(self.data_result))
        f.close()
        print(self.categroy)  # 训练数据类别及数目
        print('data process success!')
        print(count)

    def splitData(self, filename, minCount = 1200000, testCount = 300000):
        '''将数据集分成训练集和测试集
            @minCount 过滤掉数据量小于minCount的类别
            @testCount 测试集每一类的数据量'''
        data_test = []
        data_train = []
        A = dict.fromkeys(self.labels, 0)
        print('read %s' % filename)
        with open(filename) as fr:
            for line in fr:
                label = line.split(' ')[0].replace('__label__', '').replace('\n', '')
                if self.categroy[label] < minCount:  # 过滤掉小于1万的数据
                    continue
                A[label] += 1
                if A[label] <= testCount:  # 从每个类中取1000条作为测试数据
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
        print('write success')

    def GetData(self, filename_source, filename_result, *args):
        '''提取指定类别的数据
            @filename_source 源数据文件名称
            @args 要提取的类别'''
        result_data = []
        with open(filename_source) as fr:
            for line in fr:
                label = line.split(' ')[0].replace('__label__', '')
                if args.__contains__(label):
                    result_data.append(line)

        f = open(filename_result, 'w', encoding='utf-8')
        f.write(''.join(result_data))
        f.close()


if __name__ == "__main__":
    filename = "3.txt"
    minCount = 1200000
    testCount = 300000
    try:
        # 这里的 h 就表示该选项无参数，f:表示 f 选项后需要有参数
        opts, args = getopt.getopt(sys.argv[1:], "hf:m:t:", ["filename=", "minCount=", "testCount="])
    except getopt.GetoptError:
        print('Error: data.py -m <minCount> -t <testCount>')
        print('   or: data.py --minCount=<minCount> --testCount=<testCount>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print('data.py -m <minCount> -t <testCount>')
            print('or: data.py --minCount=<minCount> --testCount=<testCount>')
            sys.exit()
        elif opt in ("-f", "--filename"):
            filename = arg
            print(filename)
        elif opt in ("-m", "--minCount"):
            minCount = int(arg)
            print(minCount)
        elif opt in ("-t", "--testCount"):
            testCount = int(arg)
            print(testCount)
    p = Processor()
    p.formatData(filename)
    p.splitData('data.txt', minCount, testCount)
