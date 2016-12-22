

#!/Library/Frameworks/R.framework/Versions/Current/Resources/Rscript
args<-commandArgs()


#Run like this
# Rscript 2016-08-20_khamis_roche.R 140 10 50 170 180 male 2016-05-22_khamis_roche_coefficents.txt


#Here's a set of realistic parameters for testing
# current_height<-140
# current_age<-10
# current_weight<-50
# mother_height<-170
# father_height<-180
# gender<-"Male"
# 
# 
# current_height<-150
# current_age<-12
# current_weight<-50
# mother_height<-170
# father_height<-180
# gender<-"Male"
# 
# 
# current_height<-165
# current_age<-14
# current_weight<-50
# mother_height<-170
# father_height<-180
# gender<-"Male"
# 
# 
# current_height<-175
# current_age<-16
# current_weight<-50
# mother_height<-170
# father_height<-180
# gender<-"Male"





#!/usr/lib/R/bin/Rscript
args<-commandArgs()


#Cheking input argument count
if(length(args)!=12)stop("Must give 7 arguments exactly (current_height, current_age, current_weight, mother_height, father_height, gender, coefficients_file)")


current_height<-as.numeric(args[6])
if(is.na(current_height))stop("(1) current_height must be given as a number (cm)")
if(current_height<70 | current_height>240)stop("(1) current_height must be given as a number between 70 and 240")


current_age<-as.numeric(args[7])
if(is.na(current_age))stop("(2) current_age must be given as a number (year)")
if(current_age<5 | current_age>40)stop("(2) current_age must be given as a number between 4 and 40")
if(!current_age%in%seq(4,17.5,by=0.5))stop("Age must be either 12, 12.5, 13, 13.5... etc")
current_age_c<-as.character(current_age)

current_weight<-as.numeric(args[8])
if(is.na(current_weight))stop("(3) current_weight must be given as a number (kg)")
if(current_weight<30 | current_weight>130)stop("(3) current_weight must be given as a number between 30 and 130")

mother_height<-as.numeric(args[9])
if(is.na(mother_height))stop("(4) mother_height must be given as a number (cm)")
if(mother_height<100 | mother_height>230)stop("(4) mother_height must be given as a number between 100 and 230")


father_height<-as.numeric(args[10])
if(is.na(father_height))stop("(5) father_height must be given as a number (cm)")
if(father_height<100 | mother_height>230)stop("(5) father_height must be given as a number between 100 and 230")



gender<-tolower(args[11])
if(is.na(gender))stop("(6) gender must be given as a character")
if(!gender%in%c("male","female"))stop("(6) gender must be given as a character which is either male or female")



coefficients_file<-args[12]
if(!file.exists((coefficients_file)))stop(paste("(7) coefficients_file must be given as a path of a file (e.g. 2016-05-22_khamis_roche_coefficents.txt). The current working dir is",getwd()))





MAD50_result<-rbind(
  c(0.3, 0.45),
  c(0.4, 0.55),
  c(0.5, 0.75),
  c(0.6,  0.9),
  c(0.7, 1.05),
  c(0.8,  1.2),
  c(0.9, 1.35),
  c(1,   1.45),
  c(1.1,  1.5)
)
colnames(MAD50_result) <- c("MAD50","SD")
rownames(MAD50_result)<-MAD50_result[,"MAD50"]


MAD90_result<-rbind(
  c(0.6, 0.35),
  c(0.7, 0.45),
  c(0.8, 0.45),
  c(0.9, 0.55),
  c(1,    0.6),
  c(1.1, 0.65),
  c(1.2, 0.75),
  c(1.3,  0.9),
  c(1.4, 0.85),
  c(1.5,  0.9),
  c(1.6, 0.95),
  c(1.7,    1),
  c(1.8,  1.1),
  c(1.9,  1.1),
  c(2,    1.2),
  c(2.1, 1.35),
  c(2.2,  1.3),
  c(2.3, 1.35),
  c(2.4,  1.4),
  c(2.5, 1.55),
  c(2.6,  1.5),
  c(2.7, 1.65),
  c(2.8, 1.65),
  c(2.9,  1.7)
)
colnames(MAD90_result) <- c("MAD90","SD")
rownames(MAD90_result)<-MAD90_result[,"MAD90"]







#conversions
cm_per_inch <- 2.54
current_height_in <- current_height / cm_per_inch
lb_per_kg <- 0.453592
current_weight_lb <- lb_per_kg * current_weight

midparent_height_in <- mean(c(father_height,mother_height)) / cm_per_inch

if(gender != "male")stop("Only male implemented")


coefficients<-read.table(coefficients_file,sep="\t",header=T,row.names=1)

if(any(is.na(t(coefficients[current_age_c,])[,1])))stop("Actually this age-level is still not implemented. Need OCR of table 1 of Khamis-Roche. Right now I just entered a few by hand")
b_0<-coefficients[current_age_c,"b0"]
b_height<-coefficients[current_age_c,"height_in"]
b_weight<-coefficients[current_age_c,"weight_lb"]
b_midparent<-coefficients[current_age_c,"midparent_in"]


adult_stature_in <- b_0 + b_height*current_height_in + b_weight*current_weight_lb + b_midparent*midparent_height_in

adult_stature_cm <- adult_stature_in * cm_per_inch

MAD50<-coefficients[current_age_c,"mean_absolute_deviation_50"] * cm_per_inch
MAD90<-coefficients[current_age_c,"mean_absolute_deviation_90"] * cm_per_inch





#output
cat("adult_height_guess_cm\n")
cat(adult_stature_cm)
cat("\nmean_absolute_deviation_50\n")
cat(MAD50)
cat("\nmean_absolute_deviation_90\n")
cat(MAD90)
cat("\n")


