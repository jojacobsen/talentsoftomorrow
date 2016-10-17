
rm(list=)

library(openxlsx)
getwd()
means_data<-read.table(file="R_scripts/bio_age/2016-09-29_means.txt",sep="\t",stringsAsFactors=F,row.names=1,header=T)

colnames(means_data)<-sub("^X","",colnames(means_data))
w1<-which(!1:ncol(means_data)%in%grep("\\.5$",colnames(means_data)))
colnames(means_data)[w1]<-paste0(colnames(means_data)[w1],".0")


nmax<-350
set.seed(42)

#get names source and percentile names
names_source <- read.xlsx("R_scripts/bio_age/2016-07-06_random_player_name_source.xlsx")
pNames<-c('0.4th','2nd','9th','25th','50th','75th','91st','92nd','99.6th')

data_types<-grep("_mean_",rownames(means_data),value=T)

score_0_5<-c("population_mean_ball_control","population_mean_finishing","population_mean_aerial","population_mean_tackling","population_mean_passing","population_mean_creativity","population_mean_motivation","population_mean_composure","population_mean_game_intelligence","population_mean_confidence")


rooster <- data.frame(row.names=as.character(1:nmax))

for(n in 1:nmax){
  firstName<-sample(sub(" .+$","",names_source[,"Name"]),1)
  lastName<-sample(sub("^.+ ","",names_source[,"Name"]),1)
  name<-paste(firstName,lastName)
  rooster[n,"name"] <- name
  
  #get current age
  current_age<-0
  while(current_age<9.5 | current_age > 17.5){
    current_age <- signif(rnorm(mean=12,sd=2,1),4)
  }
  current_age_character<-round(current_age*2)/2
  if(length(grep("\\.5$",current_age_character))==1){
    current_age_character <- as.character(current_age_character)
  }else{
    current_age_character <- paste0(as.character(current_age_character),".0")
  }
  
  rooster[n,"current_age"] <- current_age
  rooster[n,"current_age_character"] <- current_age_character
  

  
  
  
  #loop over four types of data
  for(y_lab_selection in data_types){
    #Get current state
    mean<-means_data[y_lab_selection,current_age_character]
    sd<-means_data[sub("_mean_","_sd_",y_lab_selection),current_age_character]
    
    current_state<- signif(rnorm(1,mean=mean,sd=sd),3)
    
    if(y_lab_selection%in%score_0_5 & current_state>5){
      current_state<-5
    }

    if(y_lab_selection%in%score_0_5 & current_state<0){
      current_state<-0
    }
    
        
    rooster[n,sub("population_mean_","",y_lab_selection)] <- current_state
    
    #get historical data
    t1<-which(colnames(means_data)%in%current_age_character)
    if(current_age_character=="9.5")next
    history_data_point_count <- sample(1:(t1-1),1)
    history<-vector()
    for(i in 1:history_data_point_count){
      historic_age <- colnames(means_data)[i]
      that_age_mean<-means_data[y_lab_selection,t1-i]
      that_age_sd<-means_data[sub("_mean_","_sd_",y_lab_selection),t1-i]
      
      above_level<- (current_state-mean)*(that_age_sd /sd) + rnorm(1,mean=0,that_age_sd*0.1)
      
      
      historic_state <- signif(above_level+that_age_mean,4)
      if(is.na(historic_state))break
      
      if(y_lab_selection%in%score_0_5 & historic_state>5){
        historic_state<-5
      }
      
      if(y_lab_selection%in%score_0_5 & historic_state<0){
        historic_state<-0
      }
      
      history<-c(history,paste(historic_age,historic_state,sep="/"))
    }
    
    rooster[n,paste0("historic_",sub("population_mean_","",y_lab_selection))]<-paste(rev(history),collapse=" // ")
  }
  
  
  #get predicted genetic height
  current_height<-rooster[n ,"height_cm"]
  mean<-means_data["population_mean_height_cm" ,current_age_character]
  sd<-means_data["population_sd_height_cm",current_age_character]
  current_percentile<-pnorm(current_height,mean=mean,sd=sd)
  mean_final<-means_data["population_mean_height_cm" ,"17.5"]
  sd_final<-means_data["population_sd_height_cm","17.5"]
  final_height_just_by_percentile<-qnorm(current_percentile, mean=mean_final,sd=sd_final)
  genetic_height_estimate<-signif(final_height_just_by_percentile+rnorm(mean=0, sd=2,1),4)
  rooster[n,"genetic_height_estimate"] <- genetic_height_estimate
  
  
  #get SNPs
  rooster[n,"ACTN3"]<-sample(c("0/0","0/1","0/1","1/1"),1)
  rooster[n,"AGT"] <-sample(c("0/0","0/1","0/1","1/1"),1)
  rooster[n,"COL1A1"] <-sample(c("0/0","0/1","0/1","1/1"),1)
  
  
  
    
}




write.xlsx(rooster,file="R_scripts/bio_age/2016-10-17_simulated_data.xlsx") 







