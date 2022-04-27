import subprocess
import speech_recognition as sr
import time
import translate
import pandas as pd

r = sr.Recognizer()
# 音声ファイルを入力

if __name__ == '__main__':

    run = True
    while run:
        time.sleep(1)
        subprocess.run(" ./jsay.sh  おはよう", shell=True)
        with sr.Microphone() as source:  # マイクから音声入力
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            translation = r.recognize_google(audio, language='ja-JP')
            print(translation)  # 音声認識の結果
            # 味で果物を推奨する機能
            for key in translate.taste_d:
                if key in translation and '食べたい' in translation:
                    df = pd.read_csv('favorite.csv', encoding='shift_jis')
                    subprocess.run(" ./jsay.sh " + str(translate.taste_sample(translate.taste_d[key], df)) +
                                   "はどうですか", shell=True)
                    print(str(translate.taste_sample(translate.taste_d[key], df))+'はどうですか')

            if 'おはよう' in translation:
                subprocess.run(" ./jsay.sh おはよう", shell=True)
            elif '認識' in translation:
                subprocess.run(" python3 recognition.py", shell=True)
            elif '記録' in translation:
                subprocess.run(" python3 record.py", shell=True)

        except sr.UnknownValueError:
            subprocess.run(" ./jsay.sh バイバイ", shell=True)
            run = False
    print('会話終了')
