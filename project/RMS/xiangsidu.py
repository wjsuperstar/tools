import librosa
import numpy as np

#0.01283784028646155
#0.01125248352266469

test_file1 = r'duanafter_1kHz_0dB_48000_16_2.wav' #0.010928150776998257
#test_file = r'wangtianxafter_1kHz_0dB_48000_16_2.wav' #0.008178537615925586
test_file2 = r'Picture\WUC01330_20230215_after_1kHz_0dB_48000_16_2.wav'
# 加载音频文件
audio1, sr1 = librosa.load(test_file1, sr=None)
audio2, sr2 = librosa.load(test_file2, sr=None)
# 提取MFCC特征向量
mfcc1 = librosa.feature.mfcc(y=audio1, sr=sr1, n_mfcc=13)
mfcc2 = librosa.feature.mfcc(y=audio2, sr=sr2, n_mfcc=13)
# 将MFCC特征向量序列转换为一个特征向量
feature1 = np.mean(mfcc1.T, axis=0)
feature2 = np.mean(mfcc2.T, axis=0)
# 计算欧氏距离
dist = np.linalg.norm(feature1 - feature2)
# 打印相似度
print(f'音频相似度为：{1 / (1 + dist)}')