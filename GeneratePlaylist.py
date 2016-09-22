"""
Author: Ajinkya Dhaigude
Author: Kowsic Jayachandiran
"""
import librosa
import numpy as np
from numpy.linalg import inv
from numpy.linalg import det
import math
import pickle
import os
from UserProfile import UserProfile

class GeneratePlaylist:

    def __init__(self):
        self.loc = ''
        #'F:/Dev/PycharmProjects/IntelligentSystems/CourseProject/'

    def userLike(self, song, like):
        song = str(song)
        print 'adding', song

        if os.path.isfile(self.loc+'usrProfile.pick'):
            with open(self.loc+'usrProfile.pick', 'rb') as h:
                myUserProfile = pickle.load(h)
        else:
            myUserProfile = UserProfile()

        if song not in myUserProfile.allSongsLike and song not in myUserProfile.allSongsDisLike:
            if like:
                myUserProfile.allSongsLike.append(song)
            else:
                myUserProfile.allSongsDisLike.append(song)

        with open(self.loc+'usrProfile.pick', 'wb') as h:
                pickle.dump(myUserProfile, h)

    def getPlaylist(self, filePath=None):

        if os.path.isfile(self.loc+'usrProfile.pick'):
            with open(self.loc+'usrProfile.pick', 'rb') as h:
                myUserProfile = pickle.load(h)
        else:
            myUserProfile = UserProfile()


        filePath = str(filePath.replace('\\', '/'))
        num = 0
        similar = []
        songNames = []

        y, sr = librosa.load(filePath, duration = 120)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc = 20)
        thisMean = [0]*20

        for j in range(len(thisMean)):
            mysum = sum(mfccs[j])
            thisMean[j] = mysum / float(len(mfccs[j]))
        covMat = np.cov(mfccs)

        InvCovMat = inv(covMat)
        DetCovMat = det(covMat)


        likedMFCCS = []
        disLikedMFCCS = []


        while os.path.isfile(self.loc+'songTuple'+str(num)+'.pick'):
            with open(self.loc+'songTuple'+str(num)+'.pick', 'rb') as h:
                mySongs = pickle.load(h)
                num += 1

            allMFCCS = mySongs.allMFCCS

            for j in range(len(allMFCCS)):

                Kl1 = ( ( np.dot(inv(allMFCCS[j][1]), covMat) ).trace() + \
                      np.dot((allMFCCS[j][0] - thisMean).transpose(), np.dot( inv(allMFCCS[j][1]), (allMFCCS[j][0] - thisMean))) + \
                      np.log(det(allMFCCS[j][1]) / DetCovMat) - 20) / 2

                Kl2 = ( ( np.dot(InvCovMat, allMFCCS[j][1]) ).trace() + \
                      np.dot((thisMean - allMFCCS[j][0]).transpose(), np.dot( InvCovMat, (thisMean - allMFCCS[j][0]))) + \
                      np.log(DetCovMat / det(allMFCCS[j][1])) - 20) / 2

                Dkl = Kl1+Kl2
                result = (math.exp((-0.068) * Dkl))
                similar.append(result)

                if mySongs.allNames[j] in myUserProfile.allSongsLike:
                    likedMFCCS.append(allMFCCS[j])
                elif mySongs.allNames[j] in myUserProfile.allSongsDisLike:
                    disLikedMFCCS.append(allMFCCS[j])

            songNames.extend(mySongs.allNames)

        nameIndex = [i[0] for i in sorted(enumerate(similar), key=lambda x:x[1], reverse=True)]

        totConsidered = 5
        nameIndex = nameIndex[:totConsidered]
        temp = []       # stores names of toConsidered songs
        for index in nameIndex:
            temp.append(songNames[index])

        similarityCoefficient = [0]*totConsidered
        for i in range(totConsidered):
            with open(self.loc+'songTuple'+str(nameIndex[i]//50)+'.pick', 'rb') as h:
                neededPickleFile = pickle.load(h)
            neededMFCCS = neededPickleFile.allMFCCS[neededPickleFile.allNames.index(songNames[nameIndex[i]])] #nameIndex[i]%50


            for like in likedMFCCS:

                Kl1 = ( ( np.dot(inv(neededMFCCS[1]), like[1]) ).trace() + \
                      np.dot((neededMFCCS[0] - like[0]).transpose(), np.dot( inv(neededMFCCS[1]), (neededMFCCS[0] - like[0]))) + \
                      np.log(det(neededMFCCS[1]) / det(like[1])) - 20) / 2

                Kl2 = ( ( np.dot(inv(like[1]), neededMFCCS[1]) ).trace() + \
                      np.dot((like[0] - neededMFCCS[0]).transpose(), np.dot( inv(like[1]), (like[0] - neededMFCCS[0]))) + \
                      np.log(det(like[1]) / det(neededMFCCS[1])) - 20) / 2

                Dkl = Kl1+Kl2
                result = (math.exp((-0.068) * Dkl))
                similarityCoefficient[i] += result


            for like in disLikedMFCCS:  #actually disliked

                Kl1 = ( ( np.dot(inv(neededMFCCS[1]), like[1]) ).trace() + \
                      np.dot((neededMFCCS[0] - like[0]).transpose(), np.dot( inv(neededMFCCS[1]), (neededMFCCS[0] - like[0]))) + \
                      np.log(det(neededMFCCS[1]) / det(like[1])) - 20) / 2

                Kl2 = ( ( np.dot(inv(like[1]), neededMFCCS[1]) ).trace() + \
                      np.dot((like[0] - neededMFCCS[0]).transpose(), np.dot( inv(like[1]), (like[0] - neededMFCCS[0]))) + \
                      np.log(det(like[1]) / det(neededMFCCS[1])) - 20) / 2

                Dkl = Kl1+Kl2
                result = (math.exp((-0.068) * Dkl))
                similarityCoefficient[i] -= result

        nameIndex = [i[0] for i in sorted(enumerate(similarityCoefficient), key=lambda x:x[1], reverse=True)]

        songNames = temp

        playlist = []
        for index in nameIndex[:4]:
            playlist.append(songNames[index])

        return playlist
