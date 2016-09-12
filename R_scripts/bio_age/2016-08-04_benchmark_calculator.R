#!/usr/lib/R/bin/Rscript
args<-commandArgs()

#Args for testing stuff (not run)
# value <- 40
# population_mean <- 50
# population_sd <- 5



#static coded input and data-loading
value<-as.numeric(args[6])
population_mean<-as.numeric(args[7])
population_sd<-as.numeric(args[8])


#Cheking input argument count
if(length(args)!=8)stop("Must give 3 arguments exactly (value, population_mean, and population_sd)")


#Getting and cheking genetic_height_estimate argument
percentage<-round(pnorm(value,mean=population_mean,sd=population_sd)*100,1)


#output
cat("benchmark_percent\n")
cat(percentage)
