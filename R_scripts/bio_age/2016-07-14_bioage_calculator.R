#!/usr/lib/R/bin/Rscript
args<-commandArgs()

#Args for testing stuff (not run)
# genetic_height_estimate <- 170.1
# current_height <- 140.2
# ageData_path <- "R_scripts/bio_age/2016-07-06_Heigh_prediction_data_google_doc_extract.xlsx"

#static coded input and data-loading
library(openxlsx)
pNames<-c('0.4th','2nd','9th','25th','50th','75th','91st','98th','99.6th')

#Cheking input argument count
if(length(args)!=8)stop("Must give 3 arguments exactly (genetic_height_estimate, current_height, and ageData_path)")


#Getting and cheking genetic_height_estimate argument
genetic_height_estimate<-as.numeric(args[6])
if(is.na(genetic_height_estimate))stop("genetic_height_estimate must be given as a number")
if(genetic_height_estimate<70 | genetic_height_estimate>240)stop("genetic_height_estimate must be given as a number between 70 and 240")


#Getting and cheking current_height argument
current_height<-as.numeric(args[7])
if(is.na(current_height))stop("current_height must be given as a number")
if(current_height<70 | current_height>240)stop("current_height must be given as a number between 70 and 240")


#Getting and cheking ageData_path argument (a lot of these checks can be commented out, if we are sure that it runs ok)
ageData_path<-args[8]
if(class(ageData_path)!="character")stop("ageData_path must be given as a text")
if(!file.exists(ageData_path))stop("ageData_path must be given as the location of an actual file")
ageData<-read.xlsx(ageData_path)
if(!all(pNames%in%colnames(ageData)))stop("ageData didn't contain percentiles columns:",paste(pNames,collapse=", "))
if(!all("age"%in%colnames(ageData)))stop("ageData didn't contain age column")
for(col in c("age",pNames)){
  if(class(ageData[,col])!="numeric")stop(paste("column",col,"in ageData must be numeric"))
}
a<-as.character(ageData[,"age"])
a[grep("\\.5",a,invert=T)] <- paste0(a[grep("\\.5",a,invert=T)],".0")
rownames(ageData)<-a



#Perform the genetic-age calculations      
closest_percentile_i<-which.min(abs(ageData["17.5",pNames] - genetic_height_estimate))
closest_percentile<-pNames[closest_percentile_i]
y_offset<- genetic_height_estimate-ageData["17.5",closest_percentile]
percentile_slope <- ageData[,closest_percentile]
gen_diff <-percentile_slope - current_height
older_bioband_i<-which(!is.na(gen_diff) & gen_diff>0)[1]
older_bioband<-rownames(ageData)[older_bioband_i ]
younger_bioband<-rownames(ageData)[older_bioband_i-1 ]
o_bb_h<-ageData[older_bioband,closest_percentile]+y_offset
y_bb_h<-ageData[younger_bioband,closest_percentile]+y_offset
percent_in_bb<- (current_height-y_bb_h) / (o_bb_h-y_bb_h)
genetic_age <- percent_in_bb * 0.5 + as.numeric(younger_bioband)
i_1<-which(rownames(ageData)%in%older_bioband)
i_n<-nrow(ageData)
x_slope<-ageData[i_1:i_n,"age"]
y_slope<-ageData[i_1:i_n,closest_percentile]+y_offset
x_slope <- c(genetic_age,x_slope)
y_slope<- c(current_height, y_slope)




#output
cat("genetic_age\n")
cat(genetic_age)
cat("\nx_slope\n")
cat(x_slope)
cat("\ny_slope\n")
cat(y_slope)
cat("\n")
