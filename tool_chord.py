# get chord series and convert back to midi

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statistics import mean
from statistics import median
from miditoolkit.midi import parser as mid_parser  
from miditoolkit.midi import containers as ct
from chorder import Chord, Dechorder

from tool_fix import *

def notenames():
    note_names  = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    print(note_names)
    return note_names

def aboutchord():
# CM    大三和弦    C,E,G       1,3,5       0,4,7       大三度 + 小三度
# Cm    小三和弦    C,D#,G      1,2#,5      0,3,7       小三度 + 大三度
# Co    减三和弦    C,D#,F#     1,2#,4#     0,3,6       小三度 + 小三度
# C+    增三和弦    C,E,G#      1,3,5#      0,4,8       大三度 + 大三度

# C7    属七和弦    C,E,G,A#    1,3,5,6#    0,4,7,10    大三和弦 + 小三度
# CM7   大七和弦    C,E,G,B     1,3,5,7     0,4,7,11    大三和弦 + 大三度
# Cm7   小七和弦    C,D#,G,A#   1,2#,5,6#   0,3,7,10    小三和弦 + 小三度
# Co7   减七和弦    C,D#,F#,A   1,2#,4#,6   0,3,6,9     减三和弦 + 小三度
# C/o7  半减七和弦  C,D#,F#,A#  1,2#,4#,6#  0,3,6,10    减三和弦 + 大三度

# Csus2 挂二和弦    C,D,G       1,2,5       0,2,7       三 -> 二
# Csus4 挂四和弦    C,F,G       1,4,5       0,5,7       三 -> 四
    pass

def qualityCode(chordquality):
    # use a dict, change later
    if   chordquality == 'M':
        return 0
    elif chordquality == 'm':
        return 1
    elif chordquality == 'o':
        return 2
    elif chordquality == '+':
        return 3
    elif chordquality == '7':
        return 4
    elif chordquality == 'M7':
        return 5
    elif chordquality == 'm7':
        return 6
    elif chordquality == 'o7':
        return 7
    elif chordquality == '/o7':
        return 8
    elif chordquality == 'sus2':
        return 9
    elif chordquality == 'sus4':
        return 10
    else:           # q == 'Empty':
        return -1

def codeQuality(code):
    dictCQ = {
        0 : 'M',
        1 : 'm',
        2 : 'o',
        3 : '+',
        4 : '7',
        5 : 'M7',
        6 : 'm7',
        7 : 'o7',
        8 : '/o7',
        9 : 'sus2',
        10: 'sus4',
        -1: 'Empty'
    }
    return dictCQ[code]

def MIDIchord(midiobj):
    # return 2 dataframe of by-beat chords, one original, the other in C
    scale = music_scale(midiobj)
    mainnote = scale[0]
    list_note  = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    chordlist = Dechorder.dechord(midiobj, list_note)
    chordlist = chordlist[:-1]      # they end with NA
    chords,  root_pc, quality,  bass_pc = [],[],[],[]
    chordsC, rootC,   qualityC, bassC   = [],[],[],[]       # to be used to train AI with emotion data

    for i in chordlist:
        if i != Chord():
            chords.append(str(i))
            root_pc.append(int(i.root_pc))
            quality.append(i.quality)
            bass_pc.append(int(i.bass_pc))
        else:
            chords.append('None')
            root_pc.append(-1)
            quality.append('Empty')
            bass_pc.append(-1)
    dict_chords = {"name":chords, "root_pc":root_pc, "quality":quality, "bass_pc":bass_pc}
    df_chords = pd.DataFrame(dict_chords)

    for i in chordlist:
        if i != Chord():
            i=i.transpose(mainnote)
            chordsC.append(str(i))
            rootC.append(int(i.root_pc))
            qualityC.append(i.quality)
            bassC.append(int(i.bass_pc))
        else:
            chordsC.append('None')
            rootC.append(-1)
            qualityC.append('Empty')
            bassC.append(-1)
    dict_chordsC = {"name":chordsC, "root_pc":rootC, "quality":qualityC, "bass_pc":bassC}
    df_chordsC = pd.DataFrame(dict_chordsC)

    return df_chords, df_chordsC

def chordlock(df_chords):
    # using root_pc and quality in df_chords to get the %12 chrod notes
    # return a list of by-beat chords, each chord is a list
    chordnotes = []
    for i in df_chords.index:
        r = df_chords.root_pc[i]
        q = df_chords.quality[i]
        if   q == 'M':
            chordnotes.append([r, r+4, r+7])
        elif q == 'm':
            chordnotes.append([r, r+3, r+7])
        elif q == 'o':
            chordnotes.append([r, r+3, r+6])
        elif q == '+':
            chordnotes.append([r, r+4, r+8])
        elif q == '7':
            chordnotes.append([r, r+4, r+7, r+10])
        elif q == 'M7':
            chordnotes.append([r, r+4, r+7, r+11])
        elif q == 'm7':
            chordnotes.append([r, r+3, r+7, r+10])
        elif q == 'o7':
            chordnotes.append([r, r+3, r+6, r+9])
        elif q == '/o7':
            chordnotes.append([r, r+3, r+6, r+10])
        elif q == 'sus2':
            chordnotes.append([r, r+2, r+7])
        elif q == 'sus4':
            chordnotes.append([r, r+5, r+7])
        else:           # q == 'Empty':
            chordnotes.append([-127, -127, -127])
    return chordnotes

def chordmerge(chordnotes):
    chordinfo = []
    i = 0
    while i < len(chordnotes):
        duration = 1
        if i>0:
            while i<len(chordnotes) and chordnotes[i-1]==chordnotes[i] and duration<4:
                i+=1
                duration+=1
            chordinfo.append((chordnotes[i-1], duration))   # duration is an interger, the amount of beats in this chord
        i+=1
    return chordinfo

def chordtrack(chordinfo, octave, beat):
    # chordinfo is a list
    # octave should not be larger than 5
    newtrack = pd.DataFrame(columns=['start', 'end', 'pitch', 'velocity'])
    lastend = 0
    for i in chordinfo:
        pitches = i[0]
        duration = i[1]
        for j in pitches:
            newtrack = newtrack.append({'start':lastend, 'end':lastend+duration*beat, 
            'pitch':j+octave*12, 'velocity':100}, ignore_index=True)
        lastend += duration*beat

    newtrack = newtrack[newtrack.pitch!=octave*12-127]
    return newtrack


