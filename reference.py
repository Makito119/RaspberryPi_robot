
# 録音する仕方

# import pyaudio
# import wave
# import time
# import subprocess
# import motionworks
# import serial
# import picture_capture
#
# CHUNK = 2 ** 11  # チャンク（データ点数）
# CHANNELS = 1  # チャンネル1(モノラル)
# rec_time = 3  # 録音時間[s]
# RATE = 44100  # サンプリング周波数
# INDEX_NUM = 1  # 録音デバイスのインデックス番号（デフォルト1）
# file_path = "output.wav"  # 音声を保存するファイル名
# fmt = pyaudio.paInt16  # 音声のフォーマット
# audio = pyaudio.PyAudio()
# frames = []  # データリスト
#
#
# def record():
#     stream = audio.open(format=fmt, channels=CHANNELS, rate=RATE, input=True,
#                         input_device_index=INDEX_NUM,
#                         frames_per_buffer=CHUNK)
#     print("recording start...")
#
#     # 録音処理
#     for i in range(0, int(RATE / CHUNK * rec_time)):
#         data = stream.read(CHUNK)
#         frames.append(data)
#
#     # print("recording  end...")
#     #
#     # # 録音終了処理
#     # stream.stop_stream()
#     # stream.close()
#
# def record_end():
#     print("recording  end...")
#
#     # 録音終了処理
#     stream.stop_stream()
#     stream.close()
#
# def save_record():
#     audio.terminate()
#     # 録音データをファイルに保存
#     wav = wave.open(file_path, 'wb')
#     wav.setnchannels(CHANNELS)
#     wav.setsampwidth(audio.get_sample_size(fmt))
#     wav.setframerate(RATE)
#     wav.writeframes(b''.join(frames))
#     wav.close()
#
#
# def main():
#     stream = audio.open(format=fmt, channels=CHANNELS, rate=RATE, input=True,
#                         input_device_index=INDEX_NUM,
#                         frames_per_buffer=CHUNK)
#     print("recording start...")
#
#     # 録音処理
#     frames = []
#     for i in range(0, int(RATE / CHUNK * rec_time)):
#         data = stream.read(CHUNK)
#         frames.append(data)
#
#     print("recording  end...")
#
#     # 録音終了処理
#     stream.stop_stream()
#     stream.close()
#     # audio.terminate()
#     time.sleep(2)
#     stream = audio.open(format=fmt, channels=CHANNELS, rate=RATE, input=True,
#                         input_device_index=INDEX_NUM,
#                         frames_per_buffer=CHUNK)
#     # print("recording start...")
#
#     # 録音処理
#     for i in range(0, int(RATE / CHUNK * rec_time)):
#         data = stream.read(CHUNK)
#         frames.append(data)
#
#     print("recording  end...")
#
#     # 録音終了処理
#     stream.stop_stream()
#     stream.close()
#     audio.terminate()
#
#     # 録音データをファイルに保存
#     wav = wave.open(file_path, 'wb')
#     wav.setnchannels(CHANNELS)
#     wav.setsampwidth(audio.get_sample_size(fmt))
#     wav.setframerate(RATE)
#     wav.writeframes(b''.join(frames))
#     wav.close()
#
# if __name__ == "__main__":
#     con = serial.Serial('/dev/ttyAMA0', 115200)
#     # 手を振る動作
#     motionworks.motion1(con)
#     time.sleep(1)
#     subprocess.run(" ./jsay.sh 何を食べようとしていますか", shell=True)
#     # 録音開始
#     record()
#     subprocess.run(" ./jsay.sh なるほどね。写真を撮るために、机の上に置いてください", shell=True)
#     # 写真を撮る動作
#     motionworks.motion2(con)
#     time.sleep(0.5)
#     picture_capture.capture(0)
#     subprocess.run(" ./jsay.sh 写真撮りまーす", shell=True)
#     time.sleep(1)
#     picture_capture.capture(1)
#     time.sleep(0.5)
#     motionworks.puton(con)
#     motionworks.vsrc_send_1byte(con, '0048', 0)
#     time.sleep(1)
#     subprocess.run(" ./jsay.sh どんな味がしますか", shell=True)
#     record()
#     subprocess.run(" ./jsay.sh 好きですか", shell=True)
#     record()
#     save_record()

