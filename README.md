# EEG Music Generation

Work of my Student Research Project.

![avatar](https://github.com/J4vixQ/EEG-Music-Generation/blob/main/files/pic/_process.png)

#

**Here are some brief pics/audio to demostrate the key process**

1. Turn brain wave into midi music:

<img src="https://github.com/J4vixQ/EEG-Music-Generation/blob/main/files/pic/brainwave_slice.png" alt="brainwave_slice" width="800">

<img src="https://github.com/J4vixQ/EEG-Music-Generation/blob/main/files/pic/midi.png" alt="midi" width="800">

2. Count the proportion of notes and determine the scale:

<img src="https://github.com/J4vixQ/EEG-Music-Generation/blob/main/files/pic/count_before.png" alt="count_before" width="400"> <img src="https://github.com/J4vixQ/EEG-Music-Generation/blob/main/files/pic/count_after.png" alt="count_after" width="400">

3. Move the outlier notes to the scale:

<img src="https://github.com/J4vixQ/EEG-Music-Generation/blob/main/files/pic/note_before.png" alt="note_before" width="800">

<img src="https://github.com/J4vixQ/EEG-Music-Generation/blob/main/files/pic/note_after.png" alt="note_after" width="800">

4. Extract and detect chord:

<img src="https://github.com/J4vixQ/EEG-Music-Generation/blob/main/files/pic/extract_chord.jpeg" alt="extract_chord"> <img src="https://github.com/J4vixQ/EEG-Music-Generation/blob/main/files/pic/missing_chords.jpeg" alt="missing_chords"> 

5. Predict the missing chord:

<img src="https://github.com/J4vixQ/EEG-Music-Generation/blob/main/files/pic/loss.png" alt="loss" width="400"> <img src="https://github.com/J4vixQ/EEG-Music-Generation/blob/main/files/pic/accuracy.png" alt="accuracy" width="400"> 

## Notebooks

>**Generation.ipynb** converts brain wave to midi without any consideration of aesthetic feeling.
>
>**Fix.ipynb** detects tonality and move the outliers.
>
>**Chord.ipynb** try to detect chord, but often with incomplete results.
>
>**Emotion.ipynb** machine learning to predict the missing chord based on emotion and chords around.

##

## Python tools

>**tool_wave.py** basic fft, ifft and bandpass filter.
>
>**tool_midi.py** implement of miditoolkit, easy transformation method between midi and dataframe, save as csv with multiple sheets including general setting, instrument, notes of each instrument.
>
>**tool_generate.py** choose ticks per beat, numerator, denominator, tempo based on the brain wave, cut the brain wave into small slices and calculate average power and range in each slice, and then convert them to pitch and velocity of the midi file. 
>
>**tool_fix.py** count and visualize notes to get the most likely tonality, with different methods to move the outlying mote to the closest pitch.
>
>**tool_chord.py** extract chord list from a midi file, get a 2 dataframe of by-beat chords, one original, the other in C scale, and using root pitch and chord quality to form a new track of chord which could be added to another midi file.
>
>**tool_emotion.py** get all chord in EMOPIA dataset, prepare for machine learning.

##

## Files

>**Rule 1.mid** power->pitch, range->velocity.
>
>**Rule 2.mid** range->pitch, power->velocity.
>
>**FX 1.mid** remove outliers to fix Rule 1.mid
>
>**FX 2.mid** move towards C5 to fix Rule 1.mid
>
>**FX 3.mid** move towards the previous note to fix Rule 1.mid
>
>**FX 4.mid** move away from the neighbour notes to fix Rule 1.mid
>
>**LYA_G.mid** self-made midi of melody and chords of <光年之外> by G.E.M in G major.
>
>**LYA_G_noChord.mid** self-made midi but without chords.
>
>**LYA_G_withChord.mid** extract chords from LYA_G.mid and add a new track to LYA_G_noChord.mid

##

## Reference

>**Music Composition from the Brain Signal: Representing the Mental State by Music** https://doi.org/10.1155/2010/267671
>
>**miditoolkit** https://github.com/YatingMusic/miditoolkit
>
>**chorder** https://github.com/joshuachang2311/chorder
>
>**EMOPIA** (midi dataset) https://github.com/annahung31/EMOPIA
>
>**muse-lsl** (eeg dataset) https://github.com/alexandrebarachant/muse-lsl
