# author - Richard Liao
# Dec 26 2016
import numpy as np
import pandas as pd

from collections import defaultdict
import re

from bs4 import BeautifulSoup

import sys
import os

#os.environ['KERAS_BACKEND'] = 'theano'


import h5py
import csv


MAX_SEQUENCE_LENGTH = 500
MAX_NB_WORDS = 20000
EMBEDDING_DIM = 100
VALIDATION_SPLIT = 0.0




# analysis
labelpredict = []
labelreal = []

predictnum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ] #11
predictandrealnum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]  # 11
realnum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ] #11
data_result = pd.read_csv('./save/predict_result.tsv', sep='\t', delimiter="\t")


print("analying")


for idx in range(data_result.labelpredict.shape[0]):
    labelpredict.append(data_result.labelpredict[idx])
    labelreal.append(data_result.labelreal[idx])

print()
print(len(labelpredict))
print(len(labelreal))
# part labels
#labelnum  :  label's name
#num  :  sentence's number
#labelpredict labelreal  :  result read
#predictnum predictandrealnum realnum :  labels' quantity
allpredictandrealnum = 0
allpredictnum = 0
allrealnum = 0
allprecision = 0
allrecall = 0
for labelnum in range(0,11):
    # print(type(labelnum))
    # print(type(labelpredict[0]))

    for num in range(0 , len(labelpredict)):
        if str(labelpredict[num]) == str(labelnum):
            predictnum[labelnum] = predictnum[labelnum] + 1
            if str(labelreal[num]) == str(labelnum): # two label equal simultaneously
                predictandrealnum[labelnum] = predictandrealnum[labelnum] + 1
    for num in range(0 , len(labelpredict)):
        if str(labelreal[num]) == str(labelnum):
            realnum[labelnum] = realnum[labelnum] + 1

    if predictandrealnum[labelnum] == 0:
        F = 0
    # elif realnum[labelnum] == 0:
    #     F = 0
    else:
        F = 2*predictandrealnum[labelnum]*predictandrealnum[labelnum]/(predictnum[labelnum] * realnum[labelnum])/(predictandrealnum[labelnum]/predictnum[labelnum] + predictandrealnum[labelnum]/realnum[labelnum] )


    # if labelnum != 0:
    allpredictandrealnum += predictandrealnum[labelnum]
    allpredictnum += predictnum[labelnum]
    allrealnum += realnum[labelnum]


    if predictandrealnum[labelnum] != 0:
        print("label " + str(labelnum) + " Precision: " +  str(predictandrealnum[labelnum]+0.0) + "/" + str(predictnum[labelnum]+0.0))
        print("label " + str(labelnum) + " Recall: " +  str(predictandrealnum[labelnum]+0.0) + "/" + str(realnum[labelnum]+0.0))

        precision = predictandrealnum[labelnum]/predictnum[labelnum]
        recall = predictandrealnum[labelnum]/realnum[labelnum]
    else:
        print("label " + str(labelnum) + " Precision: " + str(0.0))
        print("label " + str(labelnum) + " Recall: " + str(0.0))
        precision = 0
        recall = 0
    print("label " + str(labelnum) + ": ")
    print(str(round(precision, 2)) +" & " + str(round(recall, 2)) + " & "+ str(round(F, 2)))
    print("label " + str(labelnum) + " F1: " + str(F))
    print("--------------------------------------------------------------")
    if labelnum == 0:
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("--------------------------------------------------------------")

    allprecision += precision
    allrecall += recall
    # if predictnum[labelnum] == 0 :  #there will be a error if 0/0
    #     print("label " + str(labelnum) + " precision:  0.0 (0/0)")
    # else:
    #     print("label " + str(labelnum) + " precision:  " +  str((predictandrealnum[labelnum]+0.0)/(predictnum[labelnum]+0.0)))


# print(predictnum)
# print(predictandrealnum)
# print(realnum)

print("micro precision: " + str(allpredictandrealnum/allpredictnum))
print("micro recall: " + str(allpredictandrealnum/allrealnum))
print("micro F1: " + str(2*allpredictandrealnum*allpredictandrealnum/(allrealnum*allpredictnum)/(allpredictandrealnum/allpredictnum + allpredictandrealnum/allrealnum)))

print("macro precision: " + str(allprecision/11))
print("macro recall: " + str(allrecall/11))
print("macro F1: " + str(2*allprecision*allrecall/(11*11)/(allprecision/11 + allrecall/11) ) )
