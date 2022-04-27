import time
import subprocess
import serial
import motionworks
import picture_capture
import image
import rf
import translate
import pandas as pd
# 1step=16ms

if __name__ == "__main__":
    con = serial.Serial('/dev/ttyAMA0', 115200)
    motionworks.motion2(con)
    time.sleep(0.5)
    src1 = picture_capture.capture(0)  # 背景写真
    subprocess.run(" ./jsay.sh 写真撮りまーす", shell=True)
    time.sleep(1)
    src2 = picture_capture.capture(1)  # 物体写真
    time.sleep(0.2)

    t1 = time.time()  # 写真撮影終了時間

    mask = image.create_mask(src1, src2, 60)  # マスク写真
    src3 = image.bg_difference(mask, src2)  # 背景黒の物体写真
    img = image.cv2topil(src3)  # PIL格式の背景黒物体写真

    t2 = time.time()  # 画像作成時間

    data = image.hsv_append(src2, mask, img)  # 特徴量書き出し
    a = rf.recognition(data)  # 識別結果

    t3 = time.time()  # 特徴量計算と認識の時間

    answer = translate.inverse_lookup(translate.fruit_name, a)
    df = pd.read_csv('favorite.csv', encoding='shift_jis')

    t4 = time.time()

    print("画像処理1経過時間:" + str(t2 - t1))
    print("画像処理2経過時間:" + str(t3 - t2))
    print("総経過時間:"+str(t4-t1))

    final = 'これはご主人様が'+translate.favorite_reverse[translate.fruit_favorite(answer,df)]\
            + answer + 'ですね'
    print(final)
    subprocess.run(" ./jsay.sh " + final, shell=True)
    con.close()

    # ランダムフォレストの訓練
    # rf.rf_train("data/fruit.csv")






