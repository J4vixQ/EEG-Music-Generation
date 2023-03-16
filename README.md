# EEG Music Generation

Work of my Student Research Project.

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

>**miditoolkit** https://github.com/YatingMusic/miditoolkit
>
>**chorder** https://github.com/joshuachang2311/chorder
>
>**EMOPIA** (midi dataset) https://github.com/annahung31/EMOPIA
>
>**muse-lsl** (eeg dataset) https://github.com/alexandrebarachant/muse-lsl
