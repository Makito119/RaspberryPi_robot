import cv2
import os
from matplotlib import pyplot as plt
import numpy as np
import statistics
from PIL import Image
import time
import matplotlib.pyplot as plt


def video_to_image(name):
    video_path = 'video/'+name+'.MP4'
    cap = cv2.VideoCapture(video_path)  # 動画を読み込む

    count = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 総フレーム数
    fps = cap.get(cv2.CAP_PROP_FPS)  # fps数
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # 幅
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 高さ
    print("width:{}, height:{}, count:{}, fps:{}".format(width, height, count, fps))

    os.mkdir('video_to_image/'+name)  # video_to_imageの下にフォルダを作成

    for num in range(1, int(count), int(fps)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, num)
        cv2.imwrite(
            'video_to_image/'+name+'/picture{:0=3}'.format(int((num-1)/int(fps)))+".jpg", cap.read()[1]
        )  # 毎秒１枚の画像を書き込み

        print("save picture{:0=3}".format(int((num-1)/int(fps)))+".jpg")
        # 画像をpicture000.jpgの名前で保存される
    cap.release()


# HSV特徴量の抽出
def hsv_data(img1, mask):
    img = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    h_sum, s_sum, v_sum = [], [], []
    he = mask.shape[0]  # 画像の縦画素数を取得
    we = mask.shape[1]  # 画像の横画素数を取得
    # print(img.shape)
    for j in range(he):
        for i in range(we):
            if mask[j, i] != 0:
                h_sum.append(img[j, i, 0])
                s_sum.append(img[j, i, 1])
                #v_sum.append(img[j, i, 2])

    # h_avg = round(sum(h_sum) / len(h_sum),3)  # 色相の平均値
    h_max = statistics.mode(h_sum)  # 色相の最頻値
    s_max = statistics.mode(s_sum)  # 彩度の最頻値
    #v_max = statistics.mode(v_sum)  # 明度の最頻値
    # print("H:{}, S:{}, V:{}".format(h_max, s_max, v_max))
    return h_max, s_max


def cv2topil(cv):
    a=cv2.cvtColor(cv, cv2.COLOR_BGR2RGB)
    PIL = Image.fromarray(a)
    return PIL

def plot_hist(bins, hist, color):
    centers = (bins[:-1] + bins[1:]) / 2
    widths = np.diff(bins)
    ax.bar(centers, hist, width=widths, color=color)

# マスク画像内のHSVのヒストグラム
def hsv_histogram(img1, mask):
    n_bins = 32  # ビンの数
    hist_range = [0, 256]
    img = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)  # HSV変換
    h, s, v = cv2.split(img)  # ３チャンネル分離
    hist_h = cv2.calcHist([h], [0], mask, [32], [0, 256])
    print(hist_h)
    hist=hist_h.squeeze(axis=-1)
    bins = np.linspace(*hist_range, n_bins + 1)
    fig, ax = plt.subplots()
    ax.set_xticks([0, 256])
    ax.set_xlim([0, 256])
    ax.set_xlabel("Pixel Value")
    plot_hist(bins, hist, color="k")
    plt.show()
    #hist_v = cv2.calcHist([v], [0], mask, [256], [0, 256])
    # plt.plot(hist_h, color='r', label="Hue")
    # #plt.plot(hist_s, color='g', label="Saturation")
    # #plt.plot(hist_v, color='b', label="Value")
    # plt.legend()
    # plt.show()  # plotで３チャンネル表を出す


# maskは物体のみの白黒画像、srcは物体背景画像
def bg_difference(mask, src):
    h = mask.shape[0]  # 画像の縦画素数を取得
    w = mask.shape[1]  # 画像の横画素数を取得
    dst = src
    for j in range(h):
        for i in range(w):
            if mask[j, i] == 255:  # 画素に白があったら
                dst[j, i, 0] = src[j, i, 0]   # 入力画像のR値を格納
                dst[j, i, 1] = src[j, i, 1]  # 入力画像のG値を格納
                dst[j, i, 2] = src[j, i, 2]  # 入力画像のB値を格納
            else:  # 画素が黒だったら、出力も黒
                dst[j, i, 0] = 0
                dst[j, i, 1] = 0
                dst[j, i, 2] = 0
    return dst


# 差分背景した白黒マスク画像(MOG2library)
def create_mask_mog(img1, img2, kernel):
    kernel = np.ones((kernel, kernel), np.uint8)  # カーネルの設定（膨張収縮の回数の設定）
    background = cv2.createBackgroundSubtractorMOG2()
    bg_mask = background.apply(img1)
    bg_mask = background.apply(img2)
    cv2.imshow('ou', bg_mask)

    d_mask = cv2.dilate(bg_mask, kernel)  # 膨張処理
    e_mask = cv2.erode(d_mask, kernel)  # 収縮処理
    return e_mask


# 差分背景した白黒マスク画像（閾値は６０に設定している）
def create_mask(img1, img2, kernel):
    kernel = np.ones((kernel, kernel), np.uint8)  # カーネルの設定（膨張収縮の回数の設定）
    th = 60
    # 3チャンネル分離
    r1, g1, b1 = cv2.split(img1)
    r2, g2, b2 = cv2.split(img2)
    # ３チャンネル別々で背景差分２値化
    ret, mask1 = cv2.threshold(cv2.absdiff(r1, r2), th, 255, cv2.THRESH_BINARY)
    ret, mask2 = cv2.threshold(cv2.absdiff(g1, g2), th, 255, cv2.THRESH_BINARY)
    ret, mask3 = cv2.threshold(cv2.absdiff(b1, b2), th, 255, cv2.THRESH_BINARY)

    dst = cv2.merge((mask3, mask2, mask1))  # ３チャンネル合成
    dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(dst, th, 255, cv2.THRESH_BINARY)
    cv2.imwrite("aaa.jpg",th)
    median = cv2.medianBlur(th, 7)
    d_mask = cv2.dilate(median, kernel)  # 膨張処理
    e_mask = cv2.erode(d_mask, kernel)  # 収縮処理
    return e_mask  # マスク画像を返す


# nameは物体の名前,物体の名前がtxtの名前で、データをtxtに書き込む
def file_write(name, kaisu, src1, src2, img, mask):
    file = open('data/'+name+'.txt', 'a')
    file.write(name+',')  # 第一特徴量:物体の名前
    file.write(str(circularity1(mask))+',')  # 第二特徴量:円形度
    file.write(str(hsv_data(src2, mask)[0])+',')  # 第三特徴量：色相の最頻値
    file.write(str(hsv_data(src2, mask)[1])+',')  # 第四特徴量：彩度の最頻値
    for i in range(31):
        file.write(str(image_mode(img)[i])+',')  # 第5～37特徴量:色相ヒストグラム8分割の割合
    file.write(str(image_mode(img)[31])+'\n')
    print('名前：{},円形度：{},色相最頻値:{},彩度最頻値:{},色相ヒストグラム:{}'
          .format(name, circularity1(mask), hsv_data(src2, mask)[0],hsv_data(src2,mask)[1],image_mode(img)))
    file.close()


def hsv_append(src2,src3,img):
    temp=[]
    temp.append('name')
    t1=time.time()
    temp.append(circularity1(src3))
    temp.append(hsv_data(src2, src3)[0])
    temp.append(hsv_data(src2, src3)[1])
    t2=time.time()
    print('append:'+str(t2-t1))
    for i in range(32):
        temp.append(image_mode(img)[i])  # 第7～13特徴量:色相ヒストグラム8分割の割合
    print(temp)
    temp = [temp]
    return temp

# 画像のhsvの値をファイルに読み込む,背景差分した画像をname_bgに保存する(写真の名前:n_m,果物の名前:name)
def hsv_write(n, m, name):
    src1 = cv2.imread("photograph/" + name + "/" + str(n) + "_0.jpg")  # 写真を読み込む
    for a in range(1, m+1):
        src2 = cv2.imread("photograph/" + name + "/" + str(n) + "_" + str(a) + ".jpg")
        mask=create_mask(src1, src2, 60)
        mask1 = bg_difference(mask,src2)
        #cv2.imwrite('photograph/'+name+'_bg/bg'+str(n)+'_'+str(a)+'.jpg', mask1)
        #img = 'photograph/'+name+'_bg/bg'+str(n)+'_'+str(a)+'.jpg'
        img = cv2topil(mask1)
        #print('photograph/'+name+'_bg/bg'+str(n)+'_'+str(a)+'を保存した')
        file_write(name, n, src1, src2, img, mask)  # 特徴量をデータに書き込む


# 写真サイズに合わせたウィンドウ
def window_show(name, output):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, 960, 540)
    cv2.imshow(name, output)


# 写真の最頻値の計算と色ヒストグラム8分割の計算,imgは背景黒の物体のみ画像
def image_mode(img):
    #image = Image.open(img)
    result = img.convert('HSV')
    h, s, v = result.split()
    main_colors = h.getcolors(640*480)  # カラー獲得
    for i in range(len(main_colors)-1):
        if main_colors[i][1] == 0:
            main_colors.pop(main_colors[i][1])  # 黒画素を削除
    color_counts = sorted(main_colors, reverse=True)  # 順番で並べる(一列目は画素数、二列目は色相)
    sum = np.sum(color_counts,axis=0)  # 画素と色相の和　
    #print(sum)
    hue = [0]*32
    # 色ヒストグラムの色相の割合(0-255)32分割
    for i, h in color_counts:
        for a in range(0, 256, 8):
            if a < h <= a+8:
                hue[int(a/8)] += i
    for c in range(32):
        hue[c]=round((hue[c]/sum[0])*100, 2)  # hue[8]は色相の割合100%単位
    return hue


# 円形度の計算
def circularity(src1, src2):
    bg = create_mask(src1, src2, 60)
    contours, ss = cv2.findContours(bg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # マスク画像の輪郭
    for i, cnt in enumerate(contours):
        cnt = cnt.squeeze(axis=1)  # 形状を変更する。(NumPoints, 1, 2) -> (NumPoints, 2)

    area = cv2.contourArea(cnt)  # 面積を求める
    perimeter = cv2.arcLength(cnt, True)  # 周囲長を求める
    en = round(4.0 * np.pi * area / (perimeter * perimeter), 3)  # 円形度を求める
    # print('周囲長：{},面積：{},円形度：{}'.format(perimeter, area, en))
    return en


def circularity1(mask):
    contours, ss = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # マスク画像の輪郭
    for i, cnt in enumerate(contours):
        cnt = cnt.squeeze(axis=1)  # 形状を変更する。(NumPoints, 1, 2) -> (NumPoints, 2)

    area = cv2.contourArea(cnt)  # 面積を求める
    perimeter = cv2.arcLength(cnt, True)  # 周囲長を求める
    en = round(4.0 * np.pi * area / (perimeter * perimeter)*100, 1)  # 円形度を求める
    # print('周囲長：{},面積：{},円形度：{}'.format(perimeter, area, en))
    return en







