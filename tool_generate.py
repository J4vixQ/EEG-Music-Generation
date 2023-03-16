# general setting and instrument

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statistics import mean
from statistics import median
from miditoolkit.midi import parser as mid_parser  
from miditoolkit.midi import containers as ct

from tool_wave import *

# general setting

def get_roughBPS(time, track_brain):
    # get waves
    waveGamma = get_wave(time, track_brain,  38, 42)
    waveBeta  = get_wave(time, track_brain,  12, 38)
    waveAlpha = get_wave(time, track_brain,   8, 12)
    waveTheta = get_wave(time, track_brain,   3,  8)
    waveDelta = get_wave(time, track_brain, 0.5,  3)
    # count the strengthen's
    temp = 0
    for i in range(len(time)):
        if (waveGamma[i] * track_brain[i] > 0 
        and waveBeta[i]  * track_brain[i] > 0 
        and waveAlpha[i] * track_brain[i] > 0 
        and waveTheta[i] * track_brain[i] > 0 
        and waveDelta[i] * track_brain[i] > 0 ):
            temp += 1
    # how many dots in one wave
    freq_brain = brain_fft(time, track_brain)[0]
    freq_brain = freq_brain[freq_brain>0]
    totaltime = max(time) - min(time)
    samplerate = len(time) / totaltime
    sample_wave = samplerate / abs(mean(freq_brain))
    # beat per second
    roughBPS = temp / sample_wave / totaltime
    return roughBPS

def get_TPB_BPM(time, track_brain):
    # (TPB*BPS)*totaltime=allticks=len(time)
    # TPB has to be integer
    # in FL Studio: TPB has to be n*24
    roughBPS = get_roughBPS(time, track_brain)
    totaltime = max(time)-min(time)
    roughTPB = (len(time)/totaltime) / roughBPS
    m = int(roughTPB/24)
    TPB = m*24
    BPS = (len(time)/totaltime) / TPB
    BPM = BPS*60
    print("TPB:\t", TPB)
    print("BPM:\t", BPM)
    print()
    return TPB, BPM

def general_setting(mido_obj, TPB, BPM, numerator, denomimator):
    # general settings for mido_obj
    time_signature, time_tempo = 0, 0
    timesignature = ct.TimeSignature(numerator, denomimator, time_signature)
    tempo = ct.TempoChange(BPM, time_tempo)
    mido_obj.ticks_per_beat = TPB
    mido_obj.time_signature_changes.append(timesignature)
    mido_obj.tempo_changes.append(tempo)
    return mido_obj

# notes

def stock_note_length(mido_obj, magnet=1):
    # numerator = how many beats in a bar
    # 16/denominator = how many steps in a beat
    n = mido_obj.time_signature_changes[0].numerator
    d = mido_obj.time_signature_changes[0].denominator
    beat = int(mido_obj.ticks_per_beat)     # TPB always n*24
    bar  = int(n*beat)
    step = int(beat*d/16)
    minnote = magnet*step
    print('bar\t', 'beat\t', 'step\t', 'minnote\t')
    print(bar,'\t',beat,'\t',step,'\t',minnote,'\t')
    print()
    return bar, beat, step, minnote

def powers(time, track_brain, minnote):
    # power list
    prlist = []
    for i in range(0, len(time), minnote):
        avgpr = mean(track_brain[i : i+minnote : 1])
        prlist.append(avgpr)
    # sometimes power is below 0
    prlist = np.abs(prlist)
    return prlist

def ranges(time, track_brain, minnote):
    # range list
    rglist = []
    for i in range(0, len(time), minnote):
        minn = min(track_brain[i : i+minnote : 1])
        maxx = max(track_brain[i : i+minnote : 1])
        rglist.append(maxx-minn)     # always above 0
    return rglist

# rule 1: power->pitch, range->velocity

def func_p2p(prlist, ph_high=108, ph_middle=60, ph_low=21):
    # rescale : power -> pitch
    # by default in piano range
    pr_max = max(prlist)
    pr_mid = median(prlist)
    pr_min = min(prlist)
    k_high = (ph_high - ph_middle) / (pr_max-pr_mid)
    k_low  = (ph_middle - ph_low) /  (pr_mid-pr_min)
    b_high = ph_middle - k_high * pr_mid
    b_low  = ph_middle - k_low  * pr_mid
    center = pr_mid
    print("Convert:\tmin\tmid\tmax")
    print("power:\t\t", "%.2f"%pr_min, '\t', "%.2f"%pr_mid, '\t', "%.2f"%pr_max)
    print("pitch:\t\t",        ph_low, '\t',     ph_middle, '\t',       ph_high)
    print()
    return k_high, k_low, b_high, b_low, center

def power_pitch(prlist, funcp2p):
    # pitch list
    phlist = []
    k_high, k_low, b_high, b_low, center = funcp2p      # funcp2p is a tuple
    for i in prlist:
        if i>=center:
            ph = round(i*k_high + b_high)
            phlist.append(ph)
        else:
            ph = round(i*k_low + b_low)
            phlist.append(ph)
    return phlist

def func_r2v(rglist, vt_heavy=120, vt_middle=80, vt_light=40):
    # rescale : range -> velocity
    # by default I don't want mute parts
    rg_max  = max(rglist)
    rg_mid  = median(rglist)
    rg_min  = min(rglist)
    k_loud  = (vt_heavy-vt_middle) / (rg_max-rg_mid)
    k_quiet = (vt_middle-vt_light) / (rg_mid-rg_min)
    b_loud  = vt_middle - k_loud  * rg_mid
    b_quiet = vt_middle - k_quiet * rg_mid
    center = rg_mid
    print("Convert:\tmin\tmid\tmax")
    print("range:\t\t",  "%.2f"%rg_min, '\t', "%.2f"%rg_mid, '\t', "%.2f"%rg_max)
    print("velocity:\t",      vt_light, '\t',     vt_middle, '\t',      vt_heavy)
    print()
    return k_loud, k_quiet, b_loud, b_quiet, center

def range_velocity(rglist, funcr2v):
    # velocity list
    vtlist = []
    k_loud, k_quiet, b_loud, b_quiet, center = funcr2v      # funcr2v is a tuple
    for i in rglist:
        if i>=center:
            vt = round(i*k_loud + b_loud)
            vtlist.append(vt)
        else:
            vt = round(i*k_quiet + b_quiet)
            vtlist.append(vt)
    return vtlist

def EEG_MIDI_p2p_r2v(time, track_brain, numerator=4, denomimator=4, magnet=1, pithces=(108,60,21), velocities=(120,80,40)): 

    print("Generating MIDI : power->pitch range->velocity ... \n")

    # general setting
    TPB, BPM = get_TPB_BPM(time, track_brain)

    mido_obj = mid_parser.MidiFile()
    mido_obj = general_setting(mido_obj, TPB, BPM, numerator, denomimator)

    # instrument
    bar, beat, step, minnote = stock_note_length(mido_obj, magnet)

    ph_high,  ph_middle, ph_low   = pithces         # tuple
    vt_heavy, vt_middle, vt_light = velocities      # tuple

    prlist  = powers(time, track_brain, minnote)
    funcp2p = func_p2p(prlist, ph_high,  ph_middle, ph_low)
    phlist  = power_pitch(prlist, funcp2p)

    rglist  = ranges(time, track_brain, minnote)
    funcr2v = func_r2v(rglist, vt_heavy, vt_middle, vt_light)
    vtlist  = range_velocity(rglist, funcr2v)

    starstime = list(range( 0,       len(time),         minnote))
    endstime  = list(range( minnote, len(time)+minnote, minnote))

    track_music = ct.Instrument(program=0, is_drum=False, name=track_brain.name)
    mido_obj.instruments.append(track_music)

    for i in range(len(starstime)):
        note = ct.Note(start=starstime[i], end=endstime[i], pitch=phlist[i], velocity=vtlist[i])
        mido_obj.instruments[0].notes.append(note)

    print("MIDI Generation Complete.\n")
    return mido_obj

# rule 2: range->pitch, power->velocity

def func_r2p(rglist, ph_high=108, ph_middle=60, ph_low=21):
    # rescale : range -> pitch
    # by default in piano range
    rg_max = max(rglist)
    rg_mid = median(rglist)
    rg_min = min(rglist)
    k_high = (ph_high - ph_middle) / (rg_max-rg_mid)
    k_low  = (ph_middle - ph_low) /  (rg_mid-rg_min)
    b_high = ph_middle - k_high * rg_mid
    b_low  = ph_middle - k_low  * rg_mid
    center = rg_mid
    print("Convert:\tmin\tmid\tmax")
    print("range:\t\t", "%.2f"%rg_min, '\t', "%.2f"%rg_mid, '\t', "%.2f"%rg_max)
    print("pitch:\t\t",        ph_low, '\t',     ph_middle, '\t',       ph_high)
    print()
    return k_high, k_low, b_high, b_low, center

def range_pitch(rglist, funcr2p):
    # pitch list
    phlist = []
    k_high, k_low, b_high, b_low, center = funcr2p      # modelsr2p is a tuple
    for i in rglist:
        if i>=center:
            ph = round(i*k_high + b_high)
            phlist.append(ph)
        else:
            ph = round(i*k_low + b_low)
            phlist.append(ph)
    return phlist

def func_p2v(prlist, vt_heavy=120, vt_middle=80, vt_light=40):
    # rescale : power -> velocity
    # by default I don't want any silence
    pr_max  = max(prlist)
    pr_mid  = median(prlist)
    pr_min  = min(prlist)
    k_loud  = (vt_heavy-vt_middle) / (pr_max-pr_mid)
    k_quiet = (vt_middle-vt_light) / (pr_mid-pr_min)
    b_loud  = vt_middle - k_loud  * pr_mid
    b_quiet = vt_middle - k_quiet * pr_mid
    center = pr_mid
    print("Convert:\tmin\tmid\tmax")
    print("power:\t\t",  "%.2f"%pr_min, '\t', "%.2f"%pr_mid, '\t', "%.2f"%pr_max)
    print("velocity:\t",      vt_light, '\t',     vt_middle, '\t',      vt_heavy)
    print()
    return k_loud, k_quiet, b_loud, b_quiet, center

def power_velocity(prlist, funcr2v):
    # velocity list
    vtlist = []
    k_loud, k_quiet, b_loud, b_quiet, center = funcr2v      # modelsp2v is a tuple
    for i in prlist:
        if i>=center:
            vt = round(i*k_loud + b_loud)
            vtlist.append(vt)
        else:
            vt = round(i*k_quiet + b_quiet)
            vtlist.append(vt)
    return vtlist

def EEG_MIDI_r2p_p2v(time, track_brain, numerator=4, denomimator=4, magnet=1, pithces=(108,60,21), velocities=(120,80,40)): 

    print("Generating MIDI : range->pitch power->velocity ... \n")

    # general setting
    TPB, BPM = get_TPB_BPM(time, track_brain)

    mido_obj = mid_parser.MidiFile()
    mido_obj = general_setting(mido_obj, TPB, BPM, numerator, denomimator)

    # instrument
    bar, beat, step, minnote = stock_note_length(mido_obj, magnet)

    ph_high,  ph_middle, ph_low   = pithces         # tuple
    vt_heavy, vt_middle, vt_light = velocities      # tuple

    rglist  = ranges(time, track_brain, minnote)
    funcr2p = func_r2p(rglist, ph_high,  ph_middle, ph_low)
    phlist  = range_pitch(rglist, funcr2p)

    prlist  = powers(time, track_brain, minnote)
    funcp2v = func_p2v(prlist, vt_heavy, vt_middle, vt_light)
    vtlist  = power_velocity(prlist, funcp2v)

    starstime = list(range( 0,       len(time),         minnote))
    endstime  = list(range( minnote, len(time)+minnote, minnote))

    track_music = ct.Instrument(program=0, is_drum=False, name=track_brain.name)
    mido_obj.instruments.append(track_music)

    for i in range(len(starstime)):
        note = ct.Note(start=starstime[i], end=endstime[i], pitch=phlist[i], velocity=vtlist[i])
        mido_obj.instruments[0].notes.append(note)

    print("MIDI Generation Complete.\n")
    return mido_obj

