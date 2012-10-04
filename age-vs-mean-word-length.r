#!/usr/bin/env Rscript

data             = read.csv("statistics/age-vs-mean-word-length.csv")
age              = data[,1]
mean_word_length = data[,2]

cor.test(age, mean_word_length)

pdf("plots/age-vs-mean-word-length.pdf")
plot(age, mean_word_length, xlab="Age", ylab="Mean Word Length")
