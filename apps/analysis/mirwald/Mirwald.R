#!/usr/lib/R/bin/Rscript
args<-commandArgs()


#intake of variables
if(length(args)!=9)stop("Must give 4 arguments exactly (age, height, weight, sitting_height)")

age<-as.numeric(args[6])
if(is.na(age))stop("(1) age must be given as a number (tear)")
if(age<4 | age>18)stop("(1) age must be given as a number between 4 and 18")


height<-as.numeric(args[7])
if(is.na(height))stop("(2) height must be given as a number (cm)")
if(height<70 | height>240)stop("(2) height must be given as a number between 70 and 240")

weight<-as.numeric(args[8])
if(is.na(weight))stop("(3) weight must be given as a number (kg)")
if(weight<30 | weight>130)stop("(3) weight must be given as a number between 30 and 130")

sitting_height<-as.numeric(args[9])
if(is.na(sitting_height))stop("(2) sitting_height must be given as a number (cm)")
if(sitting_height<70 | sitting_height>240)stop("(2) sitting_height must be given as a number between 70 and 240")



#documentation notes
#This formula is taken from Mirwald et al, the following section (for boys)
# (Eq. 3) Maturity Offset=-9.236 +0.0002708*Leg Length and Sitting Height interaction -0.001663*Age and Leg Length interaction + 0.007216*Age and Sitting Height interaction + 0.02292*Weight by Height ratio
#where R = 0.94, R2 = 0.891, and SEE = 0.592.

#also note the Eq. 1 (seems very different, actually)
# Maturity Offset = -29.769 + 0.0003007·Leg Length and Sitting Height interaction -0.01177*Age and Leg Length interaction + 0.01639*Age and Sitting Height interaction +0.445*Leg by Height ratio,

#Also note this from the manuscript:
# The present results indicate that maturity offset can be estimated within an error of +/- 1 yr 95% of the time. We believe this level of accuracy is sufficient for adolescence to be assigned a maturational classification.

#this is from https://www.google.dk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&cad=rja&uact=8&ved=0ahUKEwjVg7yO9KXRAhUVNVAKHbIPA6sQFggkMAE&url=https%3A%2F%2Fwww.researchgate.net%2Fprofile%2FAdam_Baxter-Jones%2Fpublication%2F261365968_application_of_Maturity_Offset%2Flinks%2F02e7e53416a3777e0b000000&usg=AFQjCNFAgVCJRtmZqoTWXcEeaIBQ_ylAZw&sig2=x19UT3-W8OK2G8YdoO-hCQ&bvm=bv.142059868,d.ZWM (saved as application_of_Maturity_Offset.doc in github)


#example 1 (from https://kinesiology.usask.ca/growthutility/results.php)
# age <- 15
# height <- 170.5
# weight <- 60.3
# sitting_height <- 82.3
#should give 0.2 (and it does)


#example 2 (from the above word doc)
# age<-12.084 
# height<-157.0
# weight<-53.0
# sitting_height<-79.6
#should give -1.4082 (and it does)





#active formula
leg_length <- height - sitting_height
maturity_offset <- -9.236 +0.0002708*leg_length*sitting_height - 0.001663*age*leg_length + 0.007216*age* sitting_height + 0.02292*(100*weight /height)
APHV <- maturity_offset + age #Predicted age at peak height velocity (APHV)



#output
cat("Maturity offset\n")
cat(maturity_offset)
cat("\nPredicted age at peak height velocity (APHV):\n")
cat(APHV)
cat("\n")
