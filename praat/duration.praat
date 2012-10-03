# Praat script that takes as input a sound file (.wav) and returns the 
# length in seconds.

# get the sound file
form Input parameters for sound length
  comment Sound File:
  word file .wav
endform

# read in the interval tier and save as text grid
Open long sound file... 'file$'

# get the duration
dur = Get duration

echo 'dur:4'

