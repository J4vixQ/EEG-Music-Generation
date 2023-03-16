import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from statistics import mean
from statistics import median
from miditoolkit.midi import parser as mid_parser  
from miditoolkit.midi import containers as ct
from chorder import Chord, Dechorder
from tool_chord import *

def chord44EMOPIA(path_Q):
    # get chords as sentences (1 sentence is 4x4 beats)
    # return an array of 4x4 beats chords (root_pch and quality)
    # [[r1,q1], [r2,q2], [r16,q16]] ...
    Q_chord = []
    for midiname in os.listdir(path_Q):
        fullpath = os.path.join(path_Q,midiname)
        midi_obj = mid_parser.MidiFile(fullpath)
        df_chordsC = MIDIchord(midi_obj)[1]                     # in C sccale
        df_chordsC = df_chordsC[['root_pc', 'quality']]         # only need root note pitch and quality of chord
        df_chordsC['quality'] = df_chordsC['quality'].map( lambda x : qualityCode(x) )
        df_chordsC = df_chordsC[df_chordsC.root_pc!=-1]         # some empty chords
        sentences  = int(len(df_chordsC)/16)                    # 1 sentence is 4x4 beats
        for i in range(sentences):
            temp = df_chordsC[i*16:(i+1)*16]
            Q_chord.append(np.array(temp))
    Q_chord = np.array(Q_chord)
    return Q_chord

def chord11EMOPIA(path_Q):
    # get chords as a full song
    # return chord list of each song
    # [[r1,q1], [r2,q2], [rEND,qEND]] ...
    Q_chord = []
    for midiname in os.listdir(path_Q):
        fullpath = os.path.join(path_Q,midiname)
        midi_obj = mid_parser.MidiFile(fullpath)
        df_chordsC = MIDIchord(midi_obj)[1]                     # in C sccale
        df_chordsC = df_chordsC[['root_pc', 'quality']]         # only need root note pitch and quality of chord
        df_chordsC['quality'] = df_chordsC['quality'].map( lambda x : qualityCode(x) )
        df_chordsC = df_chordsC[df_chordsC.root_pc!=-1]         # some empty chords
        Q_chord.append(np.array(df_chordsC))
    Q_chord = np.array(Q_chord)
    return Q_chord

def ChordPerSong(filepath):
    # chord list of a whole song
    midi_obj   = mid_parser.MidiFile(filepath)
    chordC = MIDIchord(midi_obj)[1]                             # in C sccale
    chordC = chordC[chordC.name!='None']                        # some empty chords
    chordC = chordC['name'].apply(lambda x: x.split('/')[0])    # only need name & split the 'Am/E'
    if len(chordC)==0:
        return []
    else:
        return list(chordC)

def ChordPerSet(foldpath):
    # list of (chord list of lots of songs) in the same emotion set
    biglist = []
    for midiname in os.listdir(foldpath):
        filepath = os.path.join(foldpath, midiname)
        chord = ChordPerSong(filepath)
        if chord!=[]:
            biglist.append(chord)
    return biglist