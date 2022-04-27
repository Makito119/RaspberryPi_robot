import cv2
import os
import subprocess
import time


def two_picture():
    capture(0)
    subprocess.run(" ./jsay.sh 写真撮りまーす", shell=True)
    time.sleep(1)
    capture(1)
    time.sleep(0.5)


def capture(num):
    current_dir = os.path.dirname(os.path.abspath(__file__)) + '/'

    cam = cv2.VideoCapture(0)
    if cam == None:
        return False

    print(cam)

    # カメラから映像を読み込む
    _, img = cam.read()

    # 保存先を設定
    image_file = current_dir + 'capture_test'+str(num)+'.jpg'

    # 画像ファイルとして書き出す
    cv2.imwrite(image_file, img)

    # 事後処理
    cam.release()
    cv2.destroyAllWindows()
    return img



