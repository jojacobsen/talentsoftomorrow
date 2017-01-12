#!/usr/lib/R/bin/Rscript
args<-commandArgs()

#Args for testing stuff (not run)
# genetic_height_estimate <- 170.1
# current_height <- 140.2
 # ageData_path <- "exportable_r_scripts/bio_age/2016-07-06_Heigh_prediction_data_google_doc_extract.xlsx"

#static coded input and data-loading
# library(openxlsx)
pNames<-c('0.4th','2nd','9th','25th','50th','75th','91st','98th','99.6th')

#Cheking input argument count
if(length(args)!=7)stop("Must give 2 arguments exactly (genetic_height_estimate, current_height")


#Getting and cheking genetic_height_estimate argument
genetic_height_estimate<-as.numeric(args[6])
if(is.na(genetic_height_estimate))stop("genetic_height_estimate must be given as a number")
if(genetic_height_estimate<70 | genetic_height_estimate>240)stop("genetic_height_estimate must be given as a number between 70 and 240")


#Getting and cheking current_height argument
current_height<-as.numeric(args[7])
if(is.na(current_height))stop("current_height must be given as a number")
if(current_height<70 | current_height>240)stop("current_height must be given as a number between 70 and 240")


############################# previous data load version
#Getting and cheking ageData_path argument (a lot of these checks can be commented out, if we are sure that it runs ok)
# ageData_path<-args[8]
# if(class(ageData_path)!="character")stop("ageData_path must be given as a text")
# if(!file.exists(ageData_path))stop("ageData_path must be given as the location of an actual file")
# ageData<-read.xlsx(ageData_path)
# if(!all(pNames%in%colnames(ageData)))stop("ageData didn't contain percentiles columns:",paste(pNames,collapse=", "))
# if(!all("age"%in%colnames(ageData)))stop("ageData didn't contain age column")
# for(col in c("age",pNames)){
#   if(class(ageData[,col])!="numeric")stop(paste("column",col,"in ageData must be numeric"))
# }
# a<-as.character(ageData[,"age"])
# a[grep("\\.5",a,invert=T)] <- paste0(a[grep("\\.5",a,invert=T)],".0")
# rownames(ageData)<-a
############################# end previous data load version


############################# hard-code data script
# cat(paste0("row.names=c('",paste(rownames(ageData),collapse="','"),"'),\n"))
# for(col in colnames(ageData)){
#   cat(paste0("'",col,"'=c(",paste(ageData[,col],collapse=","),"),\n"))
#
# }
############################# hard-code data script end





############################# hard-code data section
ageData<-data.frame(
  row.names=c('2.0','2.5','3.0','3.5','4.0','4.5','5.0','5.5','6.0','6.5','7.0','7.5','8.0','8.5','9.0','9.5','10.0','10.5','11.0','11.5','12.0','12.5','13.0','13.5','14.0','14.5','15.0','15.5','16.0','16.5','17.0','17.5'),
  'age'=c(2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16,16.5,17,17.5),
  'b0'=c(NA,NA,NA,NA,-10.2567,-10.719,-11.0213,NA,NA,NA,NA,NA,NA,NA,NA,-11.1405,-11.038,-10.8286,-10.4917,-10.0065,-9.3522,-8.6055,-78632,-7.1348,-6.4299,-5.7578,-5.1282,4.5092,-3.9292,-3.4873,-3.283,-3.4156),
  'height_in'=c(NA,NA,NA,NA,1.23812,1.15964,1.10675,NA,NA,NA,NA,NA,NA,NA,NA,1.02174,0.97135,0.89589,0.81239,0.74134,0.68325,0.63869,0.60818,0.59228,0.59151,0.60643,0.63757,0.68548,0.75069,0.83375,0.9352,1.05558),
  'weight_lb'=c(NA,NA,NA,NA,-0.00872,-0.00745,-0.00648,NA,NA,NA,NA,NA,NA,NA,NA,-0.00433,-0.004,-0.004,-0.00291,-0.00242,-0.00201,0.001668,0.00139,-0.00116,-0.00083,0.000699,-7e-04,-0.00059,-0.00048,-0.00037,-0.00025,-1e-04),
  'midparent_in'=c(NA,NA,NA,NA,0.50286,0.52887,0.53919,NA,NA,NA,NA,NA,NA,NA,NA,0.43593,0.45932,0.45932,0.54781,0.58409,0.60927,0.62279,0.62407,0.61253,0.58762,0.49536,0.49536,0.42687,0.34271,0.24231,0.1251,-0.0095),
  'mean_absolute_deviation_50'=c(NA,NA,NA,NA,1,1,1,NA,NA,NA,NA,NA,NA,NA,0.9,0.925,0.95,0.96,0.97,0.985,1,1,1,1.05,1.1,1,0.9,0.7,0.5,0.4,0.3,0.3),
  'mean_absolute_deviation_90'=c(NA,NA,NA,NA,2.25,2.3,2.35,NA,NA,NA,NA,NA,NA,NA,2,2,2,2.05,2.1,2.25,2.4,2.6,2.8,2.8,2.8,2.7,2.3,1.85,1.4,1,0.6,0.6),
  '0.4th'=c(79,83,86,90,92,95,98,100,103,106,109,111,113,116,118,120,122,124,126,127,129,131,134,137,140,144,147,150,153,155,157,158),
  '2nd'=c(80,85,89,92,95,97,101,104,106,109,112,114,117,119,122,124,126,128,130,132,134,136,139,142,146,149,153,156,158,160,161,162),
  '9th'=c(83,87,91,95,98,100,104,107,110,112,115,118,121,123,126,128,130,132,134,136,139,141,144,147,151,154,158,161,163,165,166,167),
  '25th'=c(85,90,94,97,100,103,107,110,113,116,119,121,124,127,129,132,134,137,139,141,143,146,149,153,156,160,163,166,168,170,171,172),
  '50th'=c(87,92,96,100,103,106,110,113,116,119,122,125,128,131,133,136,138,141,143,145,148,151,155,159,162,166,169,171,173,175,176,177),
  '75th'=c(89,94,98,102,105,109,113,116,119,122,125,129,132,134,137,140,142,145,148,150,153,156,160,164,168,171,174,177,178,180,181,181),
  '91st'=c(91,96,101,105,108,112,116,119,123,126,129,132,135,138,141,144,146,149,152,155,158,161,165,169,173,177,180,182,184,185,185,186),
  '98th'=c(93,99,104,108,111,115,119,122,126,129,132,136,139,142,145,148,151,154,157,159,163,166,170,175,179,182,185,187,189,190,190,191),
  '99.6th'=c(96,101,106,110,114,118,122,126,129,133,136,139,143,146,149,152,155,158,161,164,167,170,176,180,184,188,190,192,194,195,195,195)
)
colnames(ageData) <- sub("^X","",colnames(ageData))
############################# hard-code data section end




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
