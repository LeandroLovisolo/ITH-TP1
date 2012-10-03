#!/usr/bin/env python2

import os
import sys
import string

def get_corpus_data():
    f = open("corpus/data.csv")    # format: <student>, <subject>, <gender>, <age>
    lines = f.readlines()
    f.close()

    to_fields_list = lambda x: x.strip().split(",")
    to_fields_dict = lambda x: {"student": x[0], "subject": x[1], "gender": x[2], "age": x[3]}

    lines = map(to_fields_list, lines)
    dicts = map(to_fields_dict, lines)

    return dicts


def mean_word_length(ipu_filename):
    f = open(ipu_filename)
    lines = f.readlines()
    f.close()

    get_words      = lambda x: string.join(x.strip().split(" ")[2:])
    is_not_silence = lambda x: x != "#"
    to_array       = lambda x, y: x + y.split(" ")
    to_word_length = lambda x: len(x)

    words   = map(get_words, lines)
    words   = filter(is_not_silence, words)
    words   = reduce(to_array, words, [])
    lengths = map(to_word_length, words)
    mean    = sum(lengths) / len(lengths)

    return mean  

def find_datum_in_corpus(student, subject, corpus):
    for datum in corpus:
        if datum["student"] == student and datum["subject"] == subject:
            return datum

    raise Error(filename + " doesn't match any subject in the corpus.")

def get_filename_info(filename):
    return {"student": filename.split("-")[0],
            "subject": filename.split("-")[1][0],
            "task":    filename.split("-")[1][1]}

def main():
    # if len(sys.argv) < 2:
    #     print "Usage: " + sys.argv[0] + " <operation>"
    #     print "  where <operation> is one of:"
    #     print "    foo: documentation"
    #     print "    bar: documentation"
    #     return

    corpus_data = get_corpus_data()

    filenames = os.listdir("corpus/ipus")
    
    for fn in filenames:
        fn_info = get_filename_info(fn)

        datum = find_datum_in_corpus(fn_info["student"],
                                     fn_info["subject"],
                                     corpus_data)

        datum["task_" + fn_info["task"] + "_mean_word_length"] = mean_word_length("corpus/ipus/" + fn)


    print corpus_data


if __name__ == '__main__': main()