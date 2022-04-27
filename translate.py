import MeCab
import pykakasi
import csv
from pathlib import Path

# 辞書を選ぶ
mecab = MeCab.Tagger('')
kakasi = pykakasi.kakasi()  # 日本語をローマ字に変換
# 'りんご': kakasi.convert('りんご')[0]['passport'] # 使い方


fruit_name = {'りんご': 'ringo', 'みかん': 'mikan', 'キウイ': 'kiui', 'かき': 'kaki', 'バナナ': 'banana'}
taste_d = {'甘い': 1, '酸っぱい': 2, '苦い': 3, '渋い': 4}
favorite_d = {'大好き': 1, '好き': 2, 'はい': 2, '普通': 3, 'いや': 4, 'いいえ': 4}
favorite_reverse = {1: '大好きな', 2: '好きな', 3: '好きでも嫌いでもない', 4: '嫌いな'}


# 品詞を切り取る
def cut_words(answer):
    ans = []
    for i in range(3):
        #answer[i] == unicodedata.normalize('NFC', answer[i])
        node = mecab.parseToNode(answer[i])  # 品詞を数字IDに変換
        print(mecab.parse(answer[i]))  #mecabで情報を見る
        # 単語、品詞、詳細情報をタブ区切りで表示
        #print(f'{node.surface}\t{node.posid}\t{node.feature}')
        while node:
            if i == 0:

                if 36 <= node.posid <= 67:
                    data1 = node.surface
                # 次の要素を取得
                node = node.next

            elif i == 1:
                if 10 <= node.posid <= 12:
                    # print(node.surface)
                    data2 = node.surface
                # 次の要素を取得
                node = node.next

            elif i == 2:
                if node.posid == 2 or 36 <= node.posid <= 67:
                    data3 = node.surface
                node = node.next
    ans.append(data1)
    ans.append(data2)
    ans.append(data3)
    return ans

def cut_word1(answer):
    node = mecab.parseToNode(answer)  # 品詞を数字IDに変換
    print(mecab.parse(answer))  # mecabで情報を見る
    # 単語、品詞、詳細情報をタブ区切りで表示
    # print(f'{node.surface}\t{node.posid}\t{node.feature}')
    while node:
        if 36 <= node.posid <= 67:
           data = node.surface
            # 次の要素を取得
        node = node.next
    return data

# 答えをリストに追加する(Q3,Q2の質問は数字に変換)
def word_data(cut_words):
    data = []
    data.append(cut_words[0])
    data.append(taste_d[cut_words[1]])
    data.append(favorite_d[cut_words[2]])
    return data


# (ひらがなの名前、taste,fav)をfavorite.csvに書き込む
def csv_write(ans):
    with open('favorite.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(ans)
    print(Path('favorite.csv').read_text())


# 果物に対する好き嫌いの割合(数字を返す)
def fruit_favorite(fruit_name, df):
    df1 = df[df['name'] == fruit_name]
    #print(df1)
    avg = round(df1['favorite'].mean())
    return avg


# 辞書の逆調べ
def inverse_lookup(d, x):
    for k,v in d.items():
        if x == v:
            return k


# tasteで出現する回数が一番多い果物を返す
def taste_sample(taste_num, df):
    df1 = df[df['taste'] == taste_num]
    #print(df1)
    max = df1['name'].mode()[0]
    #print(max)
    return max




