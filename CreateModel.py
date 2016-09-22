"""
Author: Ajinkya Dhaigude
Author: Kowsic Jayachandiran
"""
from __future__ import print_function
import librosa
import numpy as np
import pickle
from SongData import SongData
import os

num = 0

myData = SongData()
for songFile in os.listdir("songs/allSongs"):


    # if num < 101:
    #     continue

    if num > 0 and num % 50 == 0:
        print('saving' + 'songTuple'+str(num//50)+'.pick')
        with open('songTuple'+str((num//50)-1)+'.pick','wb') as h:
            pickle.dump(myData, h)
        myData = SongData()


    print(str(num)+' working on '+songFile)
    y, sr = librosa.load("songs/allSongs/" + songFile, duration = 120)

    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc = 20)

    thisMean = [0]*20
    for j in range(len(thisMean)):
        mysum = sum(mfccs[j])
        thisMean[j] = mysum / float(len(mfccs[j]))
    covMat = np.cov(mfccs)

    myData.allMFCCS.append((np.asarray(thisMean), np.asarray(covMat)))
    myData.allNames.append(songFile)

    num += 1

with open('songTuple'+str(num//50)+'.pick', 'wb') as h:
            pickle.dump(myData, h)

print ('done!')