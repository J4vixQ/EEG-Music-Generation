# parse midi file and make midi file

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statistics import mean
from statistics import median
from miditoolkit.midi import parser as mid_parser  
from miditoolkit.midi import containers as ct

# midi -> dataframe

def parseMIDI(mido_obj):
    # mido_obj = mid_parser.MidiFile("path of X.mid")
    print(' > ticks per beat:', mido_obj.ticks_per_beat)

    print('\n > time signatures:', mido_obj.time_signature_changes[0].numerator, '/', mido_obj.time_signature_changes[0].denominator)

    print('\n > tempo:', mido_obj.tempo_changes[0].tempo)

    print('\n > number of tracks:', len(mido_obj.instruments))
    for i in mido_obj.instruments:
        print('     > number of notes for track', i.name, ':', len(i.notes))
    
    print()

def MIDIgeneral(midiobj):
    # general
    general = { "TPB" : midiobj.ticks_per_beat, 
                "numerator" : midiobj.time_signature_changes[0].numerator, 
                "denomimator" : midiobj.time_signature_changes[0].denominator, 
                "BPM" : midiobj.tempo_changes[0].tempo }
    df_general = pd.DataFrame(general, index=[0])
    return df_general

def MIDIinstrument(midiobj):
    # instruments
    program = []
    is_drum = []
    instruname = []
    for i in midiobj.instruments:
        program.append(i.program)
        is_drum.append(i.is_drum)
        instruname.append(i.name)
    instruments = {"program":program, "is_drum":is_drum, "name":instruname}
    df_instruments = pd.DataFrame(instruments)
    return df_instruments

def MIDItrack(midiobj):
    # return a tuple: (list_tracks, list_names)
    # list_tracks: a list of dataframes
    # list_names: a list of names
    tracks = []
    names = []

    # each track
    for i in midiobj.instruments:
        start = []
        end = []
        pitch = []
        velocity = []
        # each note
        for j in i.notes:
            start.append(j.start)
            end.append(j.end)
            pitch.append(j.pitch)
            velocity.append(j.velocity)
        data = {'start':start, 'end':end, 'pitch':pitch, 'velocity':velocity}
        df = pd.DataFrame(data)
        tracks.append(df)
        names.append(i.name)
    return tracks, names

def saveCSV(midiobj, path_xlxs):
    # for the ones has many instruments
    writer=pd.ExcelWriter(path_xlxs)

    # general
    df_general = MIDIgeneral(midiobj)
    df_general.to_excel(excel_writer=writer, sheet_name='general', index=False)

    # instrument
    df_instrument = MIDIinstrument(midiobj)
    df_instrument.to_excel(excel_writer=writer, sheet_name='instrument', index=False)

    # each track
    tracks, names = MIDItrack(midiobj)
    for i in range(len(names)):
        tracks[i].to_excel(excel_writer=writer, sheet_name=names[i], index=False)

    writer.save()
    writer.save()
    print("Done")

def saveCSV(df_general, df_instrument, tracks, names, path_xlxs):
    # for the ones has many instruments
    writer=pd.ExcelWriter(path_xlxs)

    # general
    df_general.to_excel(excel_writer=writer, sheet_name='general', index=False)

    # instrument
    df_instrument.to_excel(excel_writer=writer, sheet_name='instrument', index=False)

    # each track
    for i in range(len(names)):
        tracks[i].to_excel(excel_writer=writer, sheet_name=names[i], index=False)

    writer.save()
    writer.save()
    print("Done")

# dataframe -> midi

def generalMIDI(df_general, midiobj):
    # midiobj should be a new empty file
    tpb = int(df_general['TPB'])
    n = int(df_general['numerator'][0])
    d = int(df_general['denomimator'][0])
    bpm = float(df_general['BPM'][0])
    timesignature = ct.TimeSignature(n, d, 0)
    tempo = ct.TempoChange(bpm, 0)
    midiobj.ticks_per_beat = tpb
    midiobj.time_signature_changes.append(timesignature)
    midiobj.tempo_changes.append(tempo)
    return midiobj

def instrumentMIDI(df_instruments, midiobj):
    for i in df_instruments.index:
        temptrack = ct.Instrument(
            program=df_instruments['program'][i], 
            is_drum=df_instruments['is_drum'][i], 
            name   =df_instruments['name'][i]    )
        midiobj.instruments.append(temptrack)
    return midiobj

def trackMIDI(tracks, names, midiobj):
    # tracks is a list of dataframe
    for i in range(len(midiobj.instruments)):
        for j in tracks[i].index:
            note = ct.Note(
                start    = tracks[i]['start'][j],
                end      = tracks[i]['end'][j], 
                pitch    = tracks[i]['pitch'][j],
                velocity = tracks[i]['velocity'][j] )
            midiobj.instruments[i].notes.append(note)
        print()
    return midiobj

def add_track(midiobj, track):
    # new instrument
    chord = ct.Instrument(program=0, is_drum=False, name="chord")
    midiobj.instruments.append(chord)
    # new track
    for i in track.index:
        note = ct.Note(
            start    = track['start'][i],
            end      = track['end'][i], 
            pitch    = track['pitch'][i],
            velocity = track['velocity'][i] )
        midiobj.instruments[-1].notes.append(note)
    return midiobj
