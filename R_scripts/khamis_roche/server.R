library("shiny")

# basedir <- "C:/Users/FOLK/Documents/Work/Bioinformatics/2016-03-22_tot_genetics/talentsoftomorrow_genetics"

basedir <-"/srv/shiny-server"


#For testing a set of realistic parameters
# uniqueID<-"id_57n662948"
# current_height<-140
# current_age<-10
# current_weight<-50
# mother_height<-170
# father_height<-180
# gender<-"Male"
# 
# 
# uniqueID<-"id_57n662948"
# current_height<-150
# current_age<-12
# current_weight<-50
# mother_height<-170
# father_height<-180
# gender<-"Male"
# 
# 
# uniqueID<-"id_57n662948"
# current_height<-165
# current_age<-14
# current_weight<-50
# mother_height<-170
# father_height<-180
# gender<-"Male"
# 
# 
# uniqueID<-"id_57n662948"
# current_height<-175
# current_age<-16
# current_weight<-50
# mother_height<-170
# father_height<-180
# gender<-"Male"



#for figuring out the MAD50 and MAD90 relation to SD
# set.seed(42)
# n<-1000
# MAD50_results<-data.frame(row.names=seq(0.3,1.1,0.1))
# for(MAD50_c in rownames(MAD50_results)){
#   MAD50<-as.numeric(MAD50_c)
#   observations<-vector()
#   for(sd1 in seq(0.1,1.5,0.05)){
#     values<-rnorm(n,180,sd1)
#     MADX <- signif(sum(abs(180 - values) <MAD50) /n,2)
#     names(MADX)<-sd1
#     observations<-c(observations,MADX)
#   }
#   observations<-observations[order(abs(observations-0.5))]
#   SD_corresponding_to_MAD50<-names(observations)[1]
#   print(paste("An sd",SD_corresponding_to_MAD50,"corresponds best to a",MAD50,"MAD50 threshold with a value of",observations[1]))
#   MAD50_results[MAD50_c,"SD"] <- SD_corresponding_to_MAD50
# }
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


# set.seed(42)
# n<-1000
# MAD90_results<-data.frame(row.names=seq(0.6,2.9,0.1))
# for(MAD90_c in rownames(MAD90_results)){
#   MAD90<-as.numeric(MAD90_c)
#   observations<-vector()
#   for(sd1 in seq(0.1,2,0.05)){
#     values<-rnorm(n,180,sd1)
#     MADX <- signif(sum(abs(180 - values) <MAD90) /n,2)
#     names(MADX)<-sd1
#     observations<-c(observations,MADX)
#   }
#   observations<-observations[order(abs(observations-0.9))]
#   SD_corresponding_to_MAD90<-names(observations)[1]
#   print(paste("An sd",SD_corresponding_to_MAD90,"corresponds best to a",MAD90,"MAD90 threshold with a value of",observations[1]))
#   MAD90_results[MAD90_c,"SD"] <- SD_corresponding_to_MAD90
# }
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








# Define server logic for random distribution application
shinyServer(function(input, output) {
	
	output$plot1 <- renderPlot({ 
		# Take a dependency on input$goButton
		
		if(input$goButton == 0){
			return(NULL)
		}else if(input$goButton > 0) {
			print(paste("Ok",input$goButton))
		}
		
		uniqueID<-isolate(input$uniqueID)
		current_height<-isolate(input$current_height)
		current_age<-isolate(input$current_age)
		current_weight<-isolate(input$current_weight)
		mother_height<-isolate(input$mother_height)
		father_height<-isolate(input$father_height)
		gender<-isolate(input$gender)
		
		
		if(nchar(uniqueID)!=12)stop("uniqueID must have 12 digits")
		if(length(grep("^id_",uniqueID))==0)stop("uniqueID must start with 'id_'")
		# pDataFile<-paste("/home/ubuntu/data/",uniqueID,"/pData.txt",sep="")
		# if(!file.exists(paste("/home/ubuntu/data/",uniqueID,sep=""))){
		# 	Sys.sleep(3) #wait a little to prevent raw-force fishing	
		# 	stop("Did not find a user with this id")
		# }
		
		
		current_height<-as.numeric(current_height)
		if(is.na(current_height))stop("Heigt must be given as a number")
		if(current_height < 100 | current_height > 220)stop("Height must be between 100 and 220 cm")
		cm_per_inch <- 2.54
		current_height_in <- current_height / cm_per_inch
		
		current_age<-as.numeric(current_age)
		if(is.na(current_age))stop("Age must be given as a number")
		if(current_age < 4 | current_age > 18)stop("Age must be between 3 and 18 years")
		if(!current_age%in%seq(4,17.5,by=0.5))stop("Age must be either 12, 12.5, 13, 13.5... etc")
		current_age_c<-as.character(current_age)
		
		current_weight<-as.numeric(current_weight)
		if(is.na(current_weight))stop("Weight must be given as a number")
		if(current_weight < 15 | current_weight > 90)stop("Weight must be between 15 and 90 kg")
		lb_per_kg <- 0.453592
		current_weight_lb <- lb_per_kg * current_weight
		
		mother_height<-as.numeric(mother_height)
		if(is.na(mother_height))stop("Mother height must be given as a number")
		if(mother_height < 140 | mother_height > 195)stop("Mother height must be between 140 and 195 cm")
		
		
		father_height<-as.numeric(father_height)
		if(is.na(father_height))stop("Father height must be given as a number")
		if(father_height < 150 | father_height > 210)stop("Father height must be between 150 and 210 cm")
		
		midparent_height_in <- mean(c(father_height,mother_height)) / cm_per_inch
		
		if(gender != "Male")stop("Only male implemented")
		
		coefficients_file<-paste(basedir,"KhamisRoche/2016-05-22_khamis_roche_coefficents.txt",sep="/")
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
		
		
		# SD1_inch<-as.numeric(MAD50_result[as.character(round(MAD50,digits=1)),"SD"])
		# SD2_inch<-as.numeric(MAD90_result[as.character(round(MAD90,digits=1)),"SD"])
		
		# SD1 <- SD1_inch * cm_per_inch
		# SD2 <- SD2_inch * cm_per_inch
		
		n<-100
		x <- seq(current_age,18,length.out=n)
		y <- seq(current_height,adult_stature_cm,length.out=n)
		
		inflation_factor<-(x-current_age) / (18-current_age)
		# inflation_factor<-1
		plot(NULL,xlim=range(x),ylim=range(y),log="x")
		

		
		xlim = c(17,18)
		ylim = c(adult_stature_cm-7,adult_stature_cm+7)
		par(mai=c(1.02,0.82,0.82,1.02))
		plot(x,y,type="l", xlim=xlim, ylim=ylim,
		     xlab="age (y)",ylab="",lwd=2,yaxt="n")
		axis(4,at=seq(130,220,1),labels=seq(130,220,1))
		mtext(side=4,text="height (cm)",line=3)
		
		#plotting MAD90
		upper_x<-x
		upper_y <-y+MAD90*inflation_factor
		lower_x <-rev(x)
		lower_y <-rev(y-MAD90*inflation_factor)
		polygon(x=c(upper_x,lower_x),y=c(upper_y,lower_y),col=rgb(0,0,1,0.3),border=NA)
		
		#plotting MAD50
    upper_x<-x
    upper_y <-y+MAD50*inflation_factor
    lower_x <-rev(x)
    lower_y <-rev(y-MAD50*inflation_factor)
		polygon(x=c(upper_x,lower_x),y=c(upper_y,lower_y),col=rgb(0,0,1,0.4),border=NA)
		
		legend("topleft",legend=c("Best guess","MAD50","MAD90"),lty=c(1,1,1),
		       lwd=c(2,5,5),col=c(rgb(0,0,0),rgb(0,0,1,0.6),rgb(0,0,1,0.3)))
		
		text(x=17.9, y=adult_stature_cm+2,label=paste("Best guess:",round(adult_stature_cm),"cm"),adj=1)
		
    abline(v=18,lwd=1)				
		
	})
	
})


