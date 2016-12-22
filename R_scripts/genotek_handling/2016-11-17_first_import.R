



#first transfer annotation file
unzip Axiom_UKB_WCSG.na35.annot.csv.zip


#then get (only) the necessary fields:
#"Probe Set ID","Affy SNP ID","dbSNP RS ID","dbSNP Loctype","Chromosome","Physical Position","Position End"
cut -d ',' -f 1,3,5,6 Axiom_UKB_WCSG.na35.annot.csv > Axiom_UKB_WCSG.na35.annot.only.pos.csv


#need one with names like AX-11113867, AX-94381027, AFFX-SNP-000484 (so 1)


#then in R
rm(list=ls())

#define positions
annotation_file<-"/home/ubuntu/misc_files/annotation/Axiom_UKB_WCSG.na35.annot.only.pos.csv"
input_file<-"/home/ubuntu/2016-11-17_genotek/sample genotyping report.txt"
output_folder<-"/home/ubuntu/imputations/imputation_folder_SAMPLENAME/"


#load samples
annotation<-read.table(annotation_file,sep=",",stringsAsFactors = F,comment.char="#",header=T)
input<-read.table(input_file,sep="\t",stringsAsFactors = F,header=T,quote="",comment.char="",skip=5)


#define sample names
not_sample_names<-c("probeset_id","dbSNP_RS_ID")
sampleNames<-colnames(input)[!colnames(input)%in%not_sample_names]

#OPTIONALLY put new sampleNames on top here
set.seed(42)
previous_colnames<-colnames(input)
for(previous in sampleNames){
  previous_colnames[previous_colnames%in%previous]<-paste(sample(c(1:9,letters),5,replace=T),collapse="")  
}
colnames(input)<-previous_colnames
sampleNames<-colnames(input)[!colnames(input)%in%not_sample_names]





#check nrow is approax same
l1<-sum(annotation[,"dbSNP.RS.ID"]%in%input[,"dbSNP_RS_ID"])
# 788113
l2<-sum(input[,"dbSNP_RS_ID"]%in%annotation[,"dbSNP.RS.ID"])
# 782965
if((l1-l2)/l2>0.01)stop("Double check that there's not too much difference in annotation file and input file")


#merge by affy id
rownames(input)<-input[,"probeset_id"]
rownames(annotation)<-annotation[,"Probe.Set.ID"]

#merge
m1<-cbind(input,annotation[rownames(input),])

#define chr-order and re-order file
chr_order<-c('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','X','Y','MT')
m1[,"Chromosome"]<-factor(m1[,"Chromosome"],levels=chr_order)
m1<-m1[order(m1[,"Chromosome"],m1[,"Physical.Position"]),]


#remove the ones with no chromosome
m1<-m1[!is.na(m1[,"Chromosome"]),]

#remove the ones with no rs-id
m1<-m1[!m1[,"dbSNP_RS_ID"]%in%"",]

# Format like this
# #Genetic data is provided below as five TAB delimited columns.  Each line
# #corresponds to a SNP.  Column one provides the SNP identifier (rsID where
# #possible).  Columns two and three contain the chromosome and basepair position
# #of the SNP using human reference build 37.1 coordinates.  Columns four and five
# #contain the two alleles observed at this SNP (genotype).  The genotype is reported
# #on the forward (+) strand with respect to the human reference.
# #rsid   chromosome      position        allele1 allele2
# rs4477212       1       82154   TT
# rs3131972       1       752721  GG
# rs12562034      1       768448  AG

#check build
# m1[m1[,"dbSNP_RS_ID"]%in%"rs10507375",]
# Probe.Set.ID dbSNP.RS.ID Chromosome Physical.Position
# AFFX-KIT-000014 AFFX-KIT-000014  rs10507375         13          27573612
# grep rs10507375 id_1395Nh100_raw_data.txt
# rs10507375      13      27573612        GT
#ok looks like it's the same



template<-data.frame("#rsid"=m1[,"dbSNP_RS_ID"], chromosome=m1[,"Chromosome"], position=m1[,"Physical.Position"],genotype=NA,check.names=F)

for(sample in sampleNames){
  print(sample)
  #prepare folder
  folder_out<-sub("SAMPLENAME",sample,output_folder)

  #prepare data file  
  d1<-template
  d1[,"genotype"]<-m1[,sample]
  filename_out<-paste0(sample,"_raw_data.txt")
  dir.create(folder_out)
  write.table(d1,file=paste0(folder_out,filename_out),sep="\t",row.names=F,col.names=T,quote=F)
  
  #prepare variables file
  email<-"lassefolkersen@gmail.com"
  filename<-filename_out
  protect_from_deletion<-TRUE
  uniqueID<-sample
  save(email,filename,protect_from_deletion,uniqueID, file=paste0(folder_out,"variables.rdata"))
  
  #prepare job status
  write.table("Job is ready",file=paste0(folder_out,"job_status.txt"),sep="\t",row.names=F,col.names=F,quote=F)
  
  
}



