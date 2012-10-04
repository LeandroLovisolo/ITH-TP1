#!/usr/bin/env Rscript

data    = read.csv("statistics/gender-vs-mean-f0.csv")
gender  = data[,1]
mean_f0 = data[,2]

males   = c()
females = c()

for (i in 1:length(data[,1])) {
	if(data[i,1] == "0") {
		males = append(males, data[i,2])
	} else {
		females = append(females, data[i,2])
	}
}

t.test(males, females)

pdf("plots/gender-vs-mean-f0.pdf")
boxplot(males, females, names=c("Male", "Female"), ylab="F0 [Hz]")
