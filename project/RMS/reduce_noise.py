import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

# 加载音频
y, sr = librosa.load("wangtianxafter_1kHz_0dB_48000_16_2.wav")
fig, ax = plt.subplots(nrows=2)
librosa.display.waveshow(y, sr=sr, ax=ax[0])
ax[0].set(title='raw wave')
ax[0].label_outer()

# 计算音频中的噪音信息
noise_info = librosa.effects.split(y, top_db=30)

# 定义一个抑制噪音的函数
def noise_reduction(y, noise_info):
    y_clean = np.zeros_like(y)
    for start, end in noise_info:
        y_part = y[start:end]
        m = np.mean(y_part)
        s = np.std(y_part)
        y_part = np.clip(y_part, m-s, m+s)
        y_clean[start:end] += y_part
    return y_clean

# 调用抑制噪音的函数
y_clean = noise_reduction(y, noise_info)

# 保存抑制噪音后的音频
#librosa.output.write_wav("wang_audio_clean.wav", y_clean, sr)
sf.write("wang_audio_clean.wav", y_clean, sr)

librosa.display.waveshow(y_clean, sr=sr, ax=ax[1])
ax[1].set(title='reduce wave')
ax[1].label_outer()

#plt.show()

