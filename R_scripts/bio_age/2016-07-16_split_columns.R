#!/usr/bin/Rscript
args<-commandArgs()

#Args for testing stuff (not run)
# data_path <- "C:/Users/FOLK/Documents/Work/Bioinformatics/2016-03-22_tot_genetics/talentsoftomorrow_genetics/bioAge/2016-07-06_simulated_data.xlsx"

#static coded input and data-loading
library(openxlsx)

#Cheking input argument count
if(length(args)!=6)stop("Must give 1 argument exactly")


#Getting and cheking data_path argument
data_path<-args[6]
if(class(data_path)!="character")stop("data_path must be given as a text")
if(!file.exists(data_path))stop("data_path must be given as the location of an actual file")
data<-read.xlsx(data_path)



for(col in grep("^historic",colnames(data),value=T)){
  for(i in 1:nrow(data)){
    s1<-strsplit(data[i,col], " // ")[[1]]
    for(j in 1:length(s1)){
      s2<-strsplit(s1[j],"/")[[1]]
      data[i,paste0(col,"_age_",j)]<-s2[1]
      data[i,paste0(col,"_val_",j)]<-s2[2]
    }
  }
}

write.xlsx(data,file=basename(data_path))
