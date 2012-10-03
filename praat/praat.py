#!/usr/bin/env python2

import os
import sys
from optparse import OptionParser
from subprocess import Popen, PIPE
import csv
import re

PRAAT_PATH= './praat'

def get_wav_duration(wav):
    check_praat()
    check_file('duration.praat')
    args= [PRAAT_PATH, 'duration.praat', wav]
    p= Popen(args, stdout=PIPE)
    out= p.stdout.read()
    return float(out)
    
def run_praat(wav, start, end, min_pitch, max_pitch):
    check_praat()
    check_file('acoustics.praat')
    args= [PRAAT_PATH, 'acoustics.praat', wav, str(start),
           str(end), str(min_pitch), str(max_pitch)]
    
    p= Popen(args, stdout=PIPE)
    out= p.stdout.read()
    res= {}
    for line in out.split('\n'):
        line= line.strip()
        if len(line) == 0: continue
        k, v= line.split(':')
        if v == '--undefined--': v= -1
        else: v= float(v)
        res[k.lower()]= v
    
    return res

def get_dicts(wav, window_size, step, min_pitch, max_pitch):
    duration= get_wav_duration(wav)
    start= 0
    end= window_size
    ds= []
    print "computing..."
    while start < duration:
        print "\t t=%.02fs" % start
        d= run_praat(wav, start, end, min_pitch, max_pitch)
        d['t']= start
        ds.append(d)
        start+= step
        end+= step
    return ds

def generate_csv(ds, csv_fname):
    fields= ds[0].keys()
    fields.remove('t')
    fields.insert(0,'t')
    with open(csv_fname,'w') as f:
        writer= csv.DictWriter(f, fields)
        writer.writerow(dict(zip(fields,fields)))
        for row in ds:
            writer.writerow(row)

def check_praat():
    if not os.path.exists(PRAAT_PATH):
        err= """ No se encuentra el ejecutable de praat. Reemplazar
        la variable PRAAT_PATH especificando su ubicacion """
        raise ValueError(err)

def check_file(fname):
    if not os.path.exists(fname):
        err= """ No se encuentra %s. Debe estar en el directorio
                 actual: %s"""  % (fname, os.path.abspath('.'))
        raise ValueError(err)


def main():
    usage= 'usage: %prog [options] wav_fname csv_fname'
    parser= OptionParser(usage=usage)
    parser.add_option('-m', '--min-pitch', dest='min_pitch', default= 100, 
                            type='float', help='minimun pitch, for F0 computation. Default: 100Hz')
    parser.add_option('-M', '--max-pitch', dest='max_pitch', default= 850, 
                            type='float', help='maximum pitch, for F0 computation. Default: 850Hz')
    parser.add_option('-w', '--window-size', dest='window_size', default= 0.2, 
                            type='float', help='window size for computing statistics. Default: 0.2s')
    parser.add_option('-s', '--step', dest='step', default= None,
                            type='float', help='step for moving window. Default: window_size/2')

    options, args= parser.parse_args(sys.argv[1:])
    if options.step is None: options.step= options.window_size/2
    if len(args) < 1: parser.error('missing wav file name')
    if len(args) < 2: parser.error('missing csv file name')
    
    wav_fname, csv_fname= args[:2]
    if not os.path.exists(wav_fname): parser.error('wav fname does not exist')
    if os.path.exists(csv_fname): print 'WARNING: csv fname already exist, overriding...'
    
    ds= get_dicts(wav_fname, options.window_size, options.step, options.min_pitch, options.max_pitch)
    generate_csv(ds, csv_fname)
    print "done!"


if __name__ == '__main__': main()
