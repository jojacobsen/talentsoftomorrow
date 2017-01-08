#!/Library/Frameworks/R.framework/Versions/Current/Resources/Rscript
args<-commandArgs()

#Args for testing stuff (not run)
# value <- 50.1
# population_mean <- 50
# population_sd <- 5
# direction <- "downBetter"



#static coded input and data-loading
value<-as.numeric(args[6])
population_mean<-as.numeric(args[7])
population_sd<-as.numeric(args[8])
direction<-as.character(args[9])


#Cheking input argument count
if(length(args)!=9)stop("Must give 4 arguments exactly (value, population_mean, population_sd, direction)")

if(any(is.na(c(value,population_mean,population_sd))))stop("value, population_mean, and population_sd must be given as numbers")

if(!direction %in% c("upBetter","downBetter")){
  stop("direction argument must be either upBetter or downBetter")
}

#Getting and cheking genetic_height_estimate argument
if(direction=="upBetter"){
  percentage<-round(pnorm(value,mean=population_mean,sd=population_sd)*100,1)
}else{
  percentage<-100-round(pnorm(value,mean=population_mean,sd=population_sd)*100,1)
}

#output
cat("benchmark_percent\n")
cat(percentage)
