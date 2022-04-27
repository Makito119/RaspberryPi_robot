import subprocess
import speech_recognition as sr
import time
import serial
import motionworks
import picture_capture
import translate
r = sr.Recognizer()



# 質問を読み上げて、音声認識を行う
def question(num):
    if num == 1:
        subprocess.run(" ./jsay.sh 何を食べようとしていますか", shell=True)
        print("何を食べようとしていますか")
        ans = translate.cut_word1(recording())
        return ans
    elif num == 2:
        subprocess.run(" ./jsay.sh どんな味がしますか", shell=True)
        print("どんな味がしますか")
        translation = recording()
        return translation
    elif num == 3:
        subprocess.run(" ./jsay.sh 好きですか", shell=True)
        print("好きですか")
        translation = recording()
        return translation


# マイクから音声入力(音声翻訳を返す)
def recording():
    run = True
    while run:
        with sr.Microphone() as source:  # マイクから音声入力
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                translation = r.recognize_google(audio, language='ja-JP')
                print(translation)
                run = False
            except sr.UnknownValueError:
                subprocess.run(" ./jsay.sh もう一度お願いします", shell=True)
    return translation


if __name__ == "__main__":
    data = []
    con = serial.Serial('/dev/ttyAMA0', 115200)
    # 手を振る動作
    motionworks.motion1(con)
    time.sleep(1)
    # 質問１
    translation = question(1)
    data.append(translation)
    subprocess.run(" ./jsay.sh "+translation+"ですね。写真を撮るために、机の上に置いてください", shell=True)
    print(translation+"ですね。写真を撮るために、机の上に置いてください")

    # 写真を撮る動作
    motionworks.motion2(con)
    time.sleep(0.5)
    # 写真を撮る
    picture_capture.two_picture()
    subprocess.run(" ./jsay.sh 角度を変えて撮影します", shell=True)
    subprocess.run(" ./jsay.sh 写真撮りまーす", shell=True)
    picture_capture.capture(2)
    motionworks.puton(con)
    motionworks.putoff(con)
    time.sleep(0.5)
    subprocess.run(" ./jsay.sh どうぞお召し上がりください",shell=True)
    print("どうぞお召し上がりください")
    time.sleep(1)

    # 質問2
    translation = question(2)
    data.append(translation)
    # 質問3
    translation = question(3)
    data.append(translation)
    # データ記録
    ans = translate.cut_words(data)
    print(ans)
    subprocess.run(" ./jsay.sh " + str(ans[0]) + "," + str(ans[1]) + "," + str(ans[2]) + ",を記録します", shell=True)
    print(str(ans[0]) + "," + str(ans[1]) + "," + str(ans[2]) + ",を記録します")
    print(translate.word_data(ans))
    con.close()
    # 自動データベース保存
    # translate.csv_write(translate.word_data(ans))
    # favorite.csvに保存される
