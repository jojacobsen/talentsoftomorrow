

d<-read.table("R_scripts/bio_age/2016-09-08_means.txt",row.names=1)



entries<-grep("_mean_",rownames(d),value=T)


pdf("2016-09-12_plots_of_development.pdf")
layout(matrix(1:4,nrow=2))
for(entry in entries){
  
  d1<-data.frame(mean=t(d[entry,])[,1],sd=t(d[sub("mean","sd",entry),])[,1],age=t(d["Age",])[,1])
    
  
  ylim <- c(min(d1[,"mean"] - d1[,"sd"]*1.96), max(d1[,"mean"] + d1[,"sd"]*1.96))
  xlim <- range(d1[,"age"])
  xlim[2] <- xlim[2]+1
  
  plot(NULL,xlim=xlim,ylim=ylim,xlab="age",ylab=sub("population_mean_","",entry))
  
  lines(d1[,"age"],d1[,"mean"],lwd=2)
  lines(d1[,"age"],d1[,"mean"]+d1[,"sd"]*1,lwd=1,col="grey50")
  lines(d1[,"age"],d1[,"mean"]+d1[,"sd"]*2,lwd=1,col="grey70")
  lines(d1[,"age"],d1[,"mean"]-d1[,"sd"]*1,lwd=1,col="grey50")
  lines(d1[,"age"],d1[,"mean"]-d1[,"sd"]*2,lwd=1,col="grey70")
  text("Mean",x=xlim[2],y=d1[nrow(d1),"mean"]+d1[nrow(d1),"sd"]*0,cex=0.7,adj=1)
  text("+1SD",x=xlim[2],y=d1[nrow(d1),"mean"]+d1[nrow(d1),"sd"]*1,cex=0.7,adj=1)
  text("+2SD",x=xlim[2],y=d1[nrow(d1),"mean"]+d1[nrow(d1),"sd"]*2,cex=0.7,adj=1)
  text("-1SD",x=xlim[2],y=d1[nrow(d1),"mean"]-d1[nrow(d1),"sd"]*1,cex=0.7,adj=1)
  text("-2SD",x=xlim[2],y=d1[nrow(d1),"mean"]-d1[nrow(d1),"sd"]*2,cex=0.7,adj=1)
}


dev.off()
