#!/usr/bin/env python2

import os

def main():
    wavs_dir = "../corpus/wavs/"
    csvs_dir = "../corpus/csvs/"

    for wav in os.listdir(wavs_dir):
        csv = wav.replace(".wav", ".csv")
        print "\nGenerating .csv for " + wav + "\n"
        os.system("./praat.py " + wavs_dir + wav + " " + csvs_dir + csv)

if __name__ == '__main__': main()
