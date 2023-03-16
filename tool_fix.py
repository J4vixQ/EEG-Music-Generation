# get tonality and modify

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

from tool_midi import *

def count_note(pitches):
    # pitches is a list like df.pitch
    dict_note_count = {
        # to be modified
        # initialized in order
        0   :   0,      #  C
        1   :   0,      #  C#
        2   :   0,      #  D
        3   :   0,      #  D#
        4   :   0,      #  E
        5   :   0,      #  F
        6   :   0,      #  F#
        7   :   0,      #  G
        8   :   0,      #  G#
        9   :   0,      #  A
        10  :   0,      #  A#
        11  :   0,      #  B
    }   
    for i in pitches:
        dict_note_count[i%12] += 1
    return dict_note_count

def natural_scale(dict_note_count):
    # dict_note_count is the result of def count_note
    list_note_count = []
    for i in dict_note_count.items():
        list_note_count.append(i[1])
    
    dict_music_scale = {
        'C'   :   [0,2,4,5,7,9,11],
        'C#'  :   [1,3,5,6,8,10,0],
        'D'   :   [2,4,6,7,9,11,1],
        'D#'  :   [3,5,7,8,10,0,2],
        'E'   :   [4,6,8,9,11,1,3],
        'F'   :   [5,7,9,10,0,2,4],
        'F#'  :   [6,8,10,11,1,3,5],
        'G'   :   [7,9,11,0,2,4,6],
        'G#'  :   [8,10,0,1,3,5,7],
        'A'   :   [9,11,1,2,4,6,8],
        'A#'  :   [10,0,2,3,5,7,9],
        'B'   :   [11,1,3,4,6,8,10]}
    dict_tonality = {}

    for i in dict_music_scale.items():
        temp = 0
        for j in i[1]:
            temp += list_note_count[j]
        dict_tonality[i[0]] = temp

    # a key and a list
    tonality = max(dict_tonality, key=dict_tonality.get)

    music_scale = dict_music_scale[tonality]                # pitch%12 should be in this list
    return music_scale

def pentatonic_scale(dict_note_count):
    # 不要你离开，距离隔不开
    list_note_count = []
    for i in dict_note_count.items():
        list_note_count.append(i[1])
    
    dict_pentatonic_scale = {
        'C'   :   [0,2,4,7,9],
        'C#'  :   [1,3,5,8,10],
        'D'   :   [2,4,6,9,11],
        'D#'  :   [3,5,7,10,0],
        'E'   :   [4,6,8,11,1],
        'F'   :   [5,7,9,0,2],
        'F#'  :   [6,8,10,1,3],
        'G'   :   [7,9,11,2,4],
        'G#'  :   [8,10,0,3,5],
        'A'   :   [9,11,1,4,6],
        'A#'  :   [10,0,2,5,7],
        'B'   :   [11,1,3,6,8]}
    dict_tonality = {}

    for i in dict_pentatonic_scale.items():
        temp = 0
        for j in i[1]:
            temp += list_note_count[j]
        dict_tonality[i[0]] = temp

    # a key and a list
    tonality = max(dict_tonality, key=dict_tonality.get)
    print(tonality)

    pentatonic_scale = dict_pentatonic_scale[tonality]      # pitch%12 should be in this list
    return pentatonic_scale

def merge_dict(x,y):
    for k,v in x.items():
                if k in y.keys():
                    y[k] += v
                else:
                    y[k] = v

def music_scale(midiobj):
    tracks, names = MIDItrack(midiobj)
    totaldict = {
        0   :   0,      #  C
        1   :   0,      #  C#
        2   :   0,      #  D
        3   :   0,      #  D#
        4   :   0,      #  E
        5   :   0,      #  F
        6   :   0,      #  F#
        7   :   0,      #  G
        8   :   0,      #  G#
        9   :   0,      #  A
        10  :   0,      #  A#
        11  :   0,      #  B
    } 
    for track in tracks:
        dict_note_count = count_note(track.pitch)
        merge_dict(dict_note_count, totaldict)
    scale = natural_scale(totaldict)
    return scale

def view_notes(dict_note_count):
    list_note  = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    list_note_count = []
    for i in dict_note_count.items():
        list_note_count.append(i[1])
    plt.figure(figsize=(6, 4))
    plt.bar(list_note, list_note_count)
    plt.title('Notes')

def FX1(df, music_scale):
    df1 = df.copy(deep=True)
    df1 = df1[ (df1['pitch']%12).isin(music_scale) ]
    return df1

def FX2(df, music_scale):
    df2 = df.copy(deep=True)
    outliers = list(df2.pitch[~(df2.pitch%12).isin(music_scale)].index)     # a list of outliers' index
    for i in outliers:
        if df2.pitch[i] <= 60:
            df2.pitch[i] += 1
        else:
            df2.pitch[i] -= 1
    return df2

def FX3(df, music_scale):
    df3 = df.copy(deep=True)
    outliers = list(df3.pitch[~(df3.pitch%12).isin(music_scale)].index)     # a list of outliers' index
    outliers

    for i in outliers:
        if i==0:
            pass
        else:
            if df3.pitch[i-1] <= df3.pitch[i]:
                df3.pitch[i] -= 1
            else:
                df3.pitch[i] += 1
    return df3

def FX4(df, music_scale):
    df4 = df.copy(deep=True)
    outliers = list(df4.pitch[~(df4.pitch%12).isin(music_scale)].index)     # a list of outliers' index
    length = max(df4.index)

    for i in outliers:

        # the first note
        if i==0:
            if df4.pitch[i] <= df4.pitch[i+1]:
                df4.pitch[i] -= 1
            else:
                df4.pitch[i] += 1

        # the last note
        elif i == length:
            if df4.pitch[i-1] <= df4.pitch[i]:
                df4.pitch[i] += 1
            else:
                df4.pitch[i] -= 1

        # odinary notes
        else:
            d1 = df4.pitch[i-1] - df4.pitch[i]
            d2 = df4.pitch[i]   - df4.pitch[i+1]

            # in the middle
            if d1*d2 > 0:
                center = (df4.pitch[i-1] + df4.pitch[i+1]) / 2      # a float number
                if df4.pitch[i] > center:
                    df4.pitch[i] -= 1
                elif df4.pitch[i] < center:
                    df4.pitch[i] += 1
                else:
                    if d1 < 0:
                        df4.pitch[i] += 1
                    else:
                        df4.pitch[i] -= 1            

            # outside(dd<0) or same(dd=0) with the following note
            else:
                if d1 < 0:
                    df4.pitch[i] += 1
                else:
                    df4.pitch[i] -= 1
    return df4

