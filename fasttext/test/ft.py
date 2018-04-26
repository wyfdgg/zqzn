# _*_coding:utf-8 _*_
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import fasttext

class FT:

    def __init__(self, classifier = None):
        self.classifier = classifier

    def train(self, filename_train, filename_model):
        classifier = fasttext.supervised(filename_train, filename_model, lr=0.2, dim=100, word_ngrams=2, loss='hs',
                                         bucket=4000000, label_prefix="__label__")
        print('train success')
        self.classifier = classifier
        #return classifier

    def loadModel(self, filename_model):
        classifier = fasttext.load_model(filename_model,
                                         label_prefix='__label__')
        self.classifier = classifier
        #return classifier

    def test(self, filename_test):
        result = self.classifier.test(filename_test)
        print('p = %f\tr = %f' % (result.precision, result.recall))
        return result

    def predict(self, texts, isPrint = False):
        result = self.classifier.predict(texts)
        if isPrint:
            print(result)
        return result

    def predict(self, filename_test):
        '''预测模型，并打印预测结果
            @filename_test 预测语料'''
        labels_right = []
        texts = []
        with open(filename_test) as fr:
            for line in fr:
                # line = line.decode("utf-8").rstrip()
                labels_right.append(line.split(" ")[0].replace("__label__", "").replace("\n", ""))
                texts.append(line[line.find(' ') + 1:])
            #     print labels
            #     print texts
        #     break
        labels_predict = [e[0] for e in self.classifier.predict(texts)]  # 预测输出结果为二维形式
        # print labels_predict

        text_labels = list(set(labels_right))
        text_predict_labels = list(set(labels_predict))  # 预测结果类别
        print(text_predict_labels)  # 预测结果类别
        print(text_labels)  # 测试数据类别

        error_texts = ['label_correct\tlabel_predict\t'] #存放预测错误的数据
        A = dict.fromkeys(text_labels, 0)  # 预测正确的各个类的数目
        B = dict.fromkeys(text_labels, 0)  # 测试数据集中各个类的数目
        C = dict.fromkeys(text_predict_labels, 0)  # 预测结果中各个类的数目
        for i in range(0, len(labels_right)):
            B[labels_right[i]] += 1
            C[labels_predict[i]] += 1
            if labels_right[i] == labels_predict[i]:
                A[labels_right[i]] += 1
            else: #预测错误的数据
                error_texts.append(labels_right[i] + '\t' + labels_predict[i] + '\t' + texts[i])
        print(A)
        print(B)
        print(C)
        # 计算准确率，召回率，F值
        for key in B:
            try:
                r = float(A[key]) / float(B[key])
                p = float(A[key]) / float(C[key])
                f = p * r * 2 / (p + r)
                print("%s:\t p:%f\t r:%f\t f:%f" % (key, p, r, f))
            except:
                print("error:", key, "right:", A.get(key, 0), "real:", B.get(key, 0), "predict:", C.get(key, 0))

        print('write error.txt ')
        with open('error.txt', 'w', encoding='utf-8') as fr:
            fr.write(''.join(error_texts))




if __name__ == "__main__":
    ft = FT()
    ft.train('train.txt', 'model')
    ft.test('test.txt')
    ft.predict('test.txt')








