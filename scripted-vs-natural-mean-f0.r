#!/usr/bin/env Rscript

data             = read.csv("statistics/scripted-vs-natural-mean-f0.csv")
scripted_mean_f0 = data[,1]
natural_mean_f0  = data[,2]

t.test(scripted_mean_f0, natural_mean_f0)

pdf("plots/scripted-vs-natural-mean-f0.pdf")
boxplot(scripted_mean_f0, natural_mean_f0, names=c("Scripted", "Natural"), ylab="F0 [Hz]")
