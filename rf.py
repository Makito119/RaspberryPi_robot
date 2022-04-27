import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import StandardScaler
import pickle
#from sklearn.decomposition import PCA 主成分分析


# データベースモデルを作成(train_model.sav)
def rf_train(fruit):
    headernames = ['Class', '円形度', '色相最頻値', '彩度最頻値', '色相1',
                   '色相2', '色相3', '色相4', '色相5', '色相6', '色相7', '色相8'
        ,'9','10','11','12','13','14','15','16','17','18','19','20'
        , '21','22','23','24','25','26','27','28','29','30','31','32']  # データセットに列名を割り当てる
    dataset = pd.read_csv(fruit, names=headernames)  # データセットを読み取る
    dataset.head()  # 先頭から数えて5つの行だけが表示される
    print(dataset)
    x_train = dataset.iloc[:, 1:].values  # 何列目をX座標
    print(x_train.shape)
    y_train = dataset.iloc[:, 0].values   # 何列目をy座標
    forest = RandomForestClassifier(n_estimators=300, criterion='gini', max_depth=None, random_state=0)  # ランダムフォレストの実行
    forest.fit(x_train, y_train)
    # モデルを作成する段階でのモデルの識別精度
    result2 = forest.score(x_train, y_train)
    print('TrainAccuracy: {}'.format(result2))
    # モデルを保存する
    filename = 'temp.sav'
    pickle.dump(forest, open(filename, 'wb'))


# 未編集
def rf_whole(fruit):
    headernames = ['Class', '円形度', '色相最頻値', '明度最頻値',
                   '色相1', '色相2', '色相3', '色相4', '色相5', '色相6', '色相7', '色相8'
        , '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'
        , '21', '22', '23', '24', '25', '26', '27',
                   '28', '29', '30', '31', '32']  # データセットに列名を割り当てる

    dataset = pd.read_csv(fruit, names=headernames)  # データセットを読み取る
    dataset.head()  # 先頭から数えて5つの行だけが表示される
    print(dataset)
    x = dataset.iloc[:, [1, 35]].values  # 何列目をX座標
    y = dataset.iloc[:, 0].values  # 何列目をy座標
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)  # 訓練データとテストデータの割合
    forest = RandomForestClassifier(n_estimators=500, criterion='gini', max_depth=None, random_state=0)  # ランダムフォレストの実行
    forest.fit(x_train, y_train)
    # モデルを作成する段階でのモデルの識別精度
    result2 = forest.score(x_train, y_train)
    print('TrainAccuracy: {}'.format(result2))
    y_predict = forest.predict(x_test)  # 予測値算出
    result = confusion_matrix(y_test, y_predict)
    print("Confusion Matrix:", result)
    # precision(適合率)：
    result1 = classification_report(y_test, y_predict)
    print("Classification Report:\n", format(result1))
    result2 = accuracy_score(y_test, y_predict)  # 作成したモデルに学習に使用していない評価用のデータセットを入力し精度を確認
    print("Accuracy:", result2)
    print('Data:\n', dataset['Class'].value_counts())



def rf_test(test):
    headernames = ['Class', '円形度', '色相最頻値', '彩度最頻値',
                   '色相1', '色相2', '色相3', '色相4', '色相5', '色相6', '色相7', '色相8'
        , '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'
        , '21', '22', '23', '24', '25', '26', '27',
                   '28', '29', '30', '31', '32'
                   ]  # データセットに列名を割り当てる
    dataset = pd.read_csv(test, names=headernames)  # データセットを読み取る
    print(dataset)
    x_test = dataset.iloc[:, 1:].values  # 何列目をX座標
    y_test = dataset.iloc[:, 0].values  # 何列目をy座標
    forest = pickle.load(open('temp.sav', 'rb'))

    # std = StandardScaler()
    # x_test=std.fit_transform(x_test)
    # pca = PCA(n_components=2, whiten=False)
    # x_test=pca.fit_transform(x_test)
    y_predict = forest.predict(x_test)  # 予測値算出
    print(y_predict)
    result = confusion_matrix(y_test, y_predict)
    print("Confusion Matrix:", result)
    # precision(適合率)：
    result1 = classification_report(y_test, y_predict,digits=4)
    print("Classification Report:\n", result1)
    result2 = accuracy_score(y_test, y_predict)  # 作成したモデルに学習に使用していない評価用のデータセットを入力し精度を確認
    print("Accuracy:", result2)
    print('Data:\n', dataset['Class'].value_counts())
    # Feature Importance
    fti = forest.feature_importances_

    print('Feature Importances:')
    for i, feat in enumerate(headernames[1:36]):
        print('\t{0:20s} : {1:>.6f}'.format(feat, fti[i]))


def recognition(data):
    headernames = ['Class', '円形度', '色相最頻値', '彩度最頻値', '色相1',
                   '色相2', '色相3', '色相4', '色相5', '色相6', '色相7', '色相8'
        , '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'
        , '21', '22', '23', '24', '25', '26', '27',
                   '28', '29', '30', '31', '32']  # データセットに列名を割り当てる
    datas = np.array(data)
    print(datas)
    dataset = pd.DataFrame(datas, columns=headernames)
    print(dataset)
    x_test = dataset.iloc[:, 1:].values  # 何列目をX座標
    y_test = dataset.iloc[:, 0].values  # 何列目をy座標
    forest = pickle.load(open('temp.sav', 'rb'))
    y_predict = forest.predict(x_test)  # 予測値算出
    print(y_predict)
    return y_predict


if __name__ == "__main__":
    rf_test('data/aaa_test.csv')
