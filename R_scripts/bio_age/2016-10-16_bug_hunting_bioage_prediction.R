


library(openxlsx)

# sim_file<-"R_scripts/bio_age/2016-09-27_simulated_data.xlsx"
sim_file<-"R_scripts/bio_age/2016-10-17_simulated_data.xlsx"
sim<-read.xlsx(sim_file)


bioage_script<-"R_scripts/bio_age/2016-07-14_bioage_calculator.R"
age_data_file<-"R_scripts/bio_age/2016-07-06_Heigh_prediction_data_google_doc_extract.xlsx"



set.seed(42)
playersI<-sample(1:nrow(sim),10)
for(player in playersI){
  current_age<-sim[player,"current_age"]
  name<-sim[player,"name"]
  height_estimate<-sim[player,"genetic_height_estimate"]
  height<-sim[player,"height_cm"]
  result<-system(paste("Rscript",bioage_script,height_estimate,height,age_data_file),intern=T)  
  print(paste(name,"had age",current_age,"and bio-age",result[2]))
}

#ok so that's odd



#measure 1 - test that genetic_heigh_estimates are in fact centered around 17.5 age mean
mean(sim[,"genetic_height_estimate"])

#178.9629
#that's odd






