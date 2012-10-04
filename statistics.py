#!/usr/bin/env python2

import os
import sys
import string

def mean_word_length(ipu_filename):
    f = open(ipu_filename)
    lines = f.readlines()
    f.close()

    get_words      = lambda x: string.join(x.strip().split(" ")[2:])
    is_not_silence = lambda x: x != "#"
    to_array       = lambda x, y: x + y.split(" ")
    to_word_length = lambda x: float(len(x))

    words   = map(get_words, lines)
    words   = filter(is_not_silence, words)
    words   = reduce(to_array, words, [])
    lengths = map(to_word_length, words)
    mean    = sum(lengths) / len(lengths)

    return mean

def mean_f0(csv_filename):
    f = open(csv_filename)
    lines = f.readlines()
    f.close()

    get_fields      = lambda x: x.split(",")
    get_f0s         = lambda x: x[3]
    is_not_silence  = lambda x: x != "-1"

    lines = lines[1:]   # remove headers
    lines = map(get_fields, lines)
    f0s   = map(get_f0s, lines)
    f0s   = filter(is_not_silence, f0s)
    f0s   = map(float, f0s)
    mean  = sum(f0s) / len(f0s)

    return mean

def load_corpus_data():
    f = open("corpus/data.csv")    # format: <student>, <subject>, <gender>, <age>
    lines = f.readlines()
    f.close()

    to_fields_list = lambda x: x.strip().split(",")
    to_fields_dict = lambda x: {"student": x[0], "subject": x[1], "gender": x[2], "age": x[3]}

    lines = map(to_fields_list, lines)
    dicts = map(to_fields_dict, lines)

    return dicts

def find_datum_in_corpus(student, subject, corpus):
    for datum in corpus:
        if datum["student"] == student and datum["subject"] == subject:
            return datum

    raise Exception(student + "-" + subject + " not found in the corpus.")

def get_filename_info(filename):
    return {"student": filename.split("-")[0],
            "subject": filename.split("-")[1][0],
            "task":    filename.split("-")[1][1]}

def analyze_directory(dirname, function, key_suffix, corpus_data):
    for fn in os.listdir(dirname):
        fn_info        = get_filename_info(fn)
        datum          = find_datum_in_corpus(fn_info["student"], fn_info["subject"], corpus_data)
        new_key        = "task_" + fn_info["task"] + "_" + key_suffix
        datum[new_key] = function(dirname + "/" + fn)

def mean_or_none(x, y):
    if x != None and y != None:
        return (x + y) / 2
    elif x != None and y == None:
        return x
    elif x == None and y != None:
        return y
    else:
        return None

def main():
    if len(sys.argv) != 2 or not (sys.argv[1] in ["age-vs-mean-word-length",
                                                  "gender-vs-mean-f0",
                                                  "scripted-vs-natural-mean-f0"]):
        print "Usage: " + sys.argv[0] + " <operation>"
        print "  where <operation> is one of:"
        print "    age-vs-mean-word-length:     produces a list of (age, mean word length) pairs."
        print "    gender-vs-mean-f0:           produces a list of (gender, mean f0) pairs."
        print "    scripted-vs-natural-mean-f0: produces a list of (scripted f0, natural f0) pairs."
        return
    
    corpus_data = load_corpus_data()
    analyze_directory("corpus/ipus", mean_word_length, "mean_word_length", corpus_data)
    analyze_directory("corpus/csvs", mean_f0, "mean_f0", corpus_data)

    operation = sys.argv[1]

    if operation == "age-vs-mean-word-length":
        print "Age,Mean Word Length"
        for datum in corpus_data:
            mean = mean_or_none(datum.get("task_1_mean_word_length"),
                                datum.get("task_2_mean_word_length"))
            if mean != None:
                print datum["age"] + "," + str(mean)
        return

    if operation == "gender-vs-mean-f0":
        print '"Gender (0 = male, 1 = female)","Mean F0"'
        for datum in corpus_data:
            mean = mean_or_none(datum.get("task_1_mean_f0"),
                                datum.get("task_2_mean_f0"))
            if mean != None:
                print ("0" if datum["gender"] == "m" else "1") + "," + str(mean)
        return

    if operation == "scripted-vs-natural-mean-f0":
        print '"Scripted F0","Natural F0"'
        for datum in corpus_data:
            scripted = datum.get("task_1_mean_f0")
            natural  = datum.get("task_2_mean_f0")
            if scripted == None and natural == None:
                continue
            else:
                def none_as_blank(x): return "" if x == None else str(x)
                print none_as_blank(scripted) + "," + none_as_blank(natural)
        return    

    if operation == "natural-vs-scripted-mean-f0":
        pass

if __name__ == '__main__': main()
