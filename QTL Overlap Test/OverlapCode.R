setwd("~/Documents/Academic-Research/Authored Papers/Jaltomata Data/QTL Mapping/Reproductive QTL/Data and Stats/Mapping/Overlap")

library(ggplot2) #package for plotting

#Import data:
randomSampleOverlap <- read.csv("~/Documents/Academic-Research/Authored Papers/Jaltomata Data/QTL Mapping/Reproductive QTL/Data and Stats/Mapping/Overlap/randomSampleOverlap.csv")

#Basic summary stats:
summary(randomSampleOverlap$Morph.Morph) #mean = 96.68
sd(randomSampleOverlap$Morph.Morph) #sd = 11.4405

summary(randomSampleOverlap$Color.Color) #mean = 1.345
sd(randomSampleOverlap$Color.Color) #sd = 1.128557

summary(randomSampleOverlap$Fert.Fert) #mean = 2.039
sd(randomSampleOverlap$Fert.Fert) #sd = 1.369072

summary(randomSampleOverlap$Morph.Color) #mean = 26.1
sd(randomSampleOverlap$Morph.Color) #sd = 5.649649

summary(randomSampleOverlap$Color.Fert) #mean = 3.947
sd(randomSampleOverlap$Color.Fert) #sd = 1.940301

summary(randomSampleOverlap$Fert.Morph) #mean = 30.02
sd(randomSampleOverlap$Fert.Morph) #sd = 5.80299

#Testing whether observed is sig. greater than expected by chance:
1-pnorm((133-96.68)/11.4405) #Morph-Morph
1-pnorm((1-1.345)/1.128557)  #Color-Color
1-pnorm((8-2.039)/1.369072)  #Fert-Fert
1-pnorm((14-26.1)/5.649649)  #Morph-Color
1-pnorm((2-3.947)/1.940301)  #Color-Fert
1-pnorm((31-30.02)/5.80299)  #Fert-Morph

#Testing whether observed is sig. less than expected by chance:
pnorm((133-96.68)/11.4405) #Morph-Morph
pnorm((1-1.345)/1.128557)  #Color-Color
pnorm((8-2.039)/1.369072)  #Fert-Fert
pnorm((14-26.1)/5.649649)  #Morph-Color
pnorm((2-3.947)/1.940301)  #Color-Fert
pnorm((31-30.02)/5.80299)  #Fert-Morph

#Calculating Tail Thresholds
qnorm(0.95, mean=96.68, sd=11.4405) #Morph-Morph
qnorm(0.05, mean=96.68, sd=11.4405) #Morph-Morph
qnorm(0.95, mean=1.345, sd=1.128557) #Color-Color
qnorm(0.05, mean=1.345, sd=1.128557) #Color-Color
qnorm(0.95, mean=2.039, sd=1.369072) #Fert-Fert
qnorm(0.05, mean=2.039, sd=1.369072) #Fert-Fert
qnorm(0.95, mean=26.1, sd=5.649649) #Morph-Color
qnorm(0.05, mean=26.1, sd=5.649649) #Morph-Color
qnorm(0.95, mean=3.947, sd=1.940301) #Color-Fert
qnorm(0.05, mean=3.947, sd=1.940301) #Color-Fert
qnorm(0.95, mean=30.02, sd=5.80299) #Fert-Morph
qnorm(0.05, mean=30.02, sd=5.80299) #Fert-Morph

#Plotting:
#ggplot(mean_floral_morph, aes(cor.dia.h.mean, fill=Group)) + geom_density(alpha=.25) + expand_limits(x = c(10, 40), y = c(-0.04, 0.3)) + geom_linerange(x=15.32, ymax=0.35, ymin=0, colour="purple") + geom_linerange(x=12.22, ymax=0.35, ymin=0, colour="purple", linetype=2) + geom_linerange(x=24.58, ymax=0.35, ymin=0, colour="darkgreen") + geom_linerange(x=24.59, ymax=0.35, ymin=0, colour="darkgreen", linetype=2)+ geom_linerange(x=29.05, ymax=0.35, ymin=0, colour="red") + geom_linerange(x=29.74, ymax=0.35, ymin=0, colour="darkcyan") + geom_linerange(x=32.12, ymax=0.35, ymin=0, colour="darkcyan", linetype=2) + labs(title = "Corolla Diameter", x="Mean Corolla Diameter (cm)", y="Density") + annotate("text", label = "mean=15.32", x = 13.5, y = -0.01, size = 5, colour = "purple") + annotate("text", label = "parent=12.22", x = 13.5, y = -0.03, size = 5, colour = "purple") + annotate("text", label = "mean=24.58", x = 22, y = -0.01, size = 5, colour = "darkgreen") + annotate("text", label = "parent=24.59", x = 22, y = -0.03, size = 5, colour = "darkgreen") + annotate("text", label = "mean=29.74", x = 30, y = -0.01, size = 5, colour = "darkcyan") + annotate("text", label = "parent=32.12", x = 30, y = -0.03, size = 5, colour = "darkcyan") + annotate("text", label = "mean=29.05", x = 38, y = -0.01, size = 5, colour = "red") 

p1=ggplot(randomSampleOverlap, aes(x=Morph.Morph)) + geom_histogram(binwidth=1, position="dodge") + labs(title="Overlap within Morph Traits", x="No. Overlap Events", y="No. Simulations") + geom_linerange(x=133, ymax=500, ymin=0, colour="red") + geom_linerange(x=77.86, ymax=500, ymin=0, colour="blue") + geom_linerange(x=115.5, ymax=500, ymin=0, colour="blue")
p2=ggplot(randomSampleOverlap, aes(x=Color.Color)) + geom_histogram(binwidth=1, position="dodge") + labs(title="Overlap within Color Traits", x="No. Overlap Events", y="No. Simulations") + geom_linerange(x=1, ymax=5000, ymin=0, colour="red") + geom_linerange(x=3.2, ymax=5000, ymin=0, colour="blue") + geom_linerange(x=0, ymax=5000, ymin=0, colour="blue")
p3=ggplot(randomSampleOverlap, aes(x=Fert.Fert)) + geom_histogram(binwidth=1, position="dodge") + labs(title="Overlap within Fertility Traits", x="No. Overlap Events", y="No. Simulations") + geom_linerange(x=8, ymax=4000, ymin=0, colour="red") + geom_linerange(x=4.29, ymax=4000, ymin=0, colour="blue") + geom_linerange(x=0, ymax=4000, ymin=0, colour="blue")
p4=ggplot(randomSampleOverlap, aes(x=Morph.Color)) + geom_histogram(binwidth=1, position="dodge") + labs(title="Overlap between Morph and Color Traits", x="No. Overlap Events", y="No. Simulations") + geom_linerange(x=14, ymax=800, ymin=0, colour="red") + geom_linerange(x=35.39, ymax=800, ymin=0, colour="blue") + geom_linerange(x=16.81, ymax=800, ymin=0, colour="blue")
p5=ggplot(randomSampleOverlap, aes(x=Color.Fert)) + geom_histogram(binwidth=1, position="dodge") + labs(title="Overlap between Color and Fertility Traits", x="No. Overlap Events", y="No. Simulations") + geom_linerange(x=2, ymax=3000, ymin=0, colour="red") + geom_linerange(x=7.14, ymax=3000, ymin=0, colour="blue") + geom_linerange(x=0.76, ymax=3000, ymin=0, colour="blue")
p6=ggplot(randomSampleOverlap, aes(x=Fert.Morph)) + geom_histogram(binwidth=1, position="dodge") + labs(title="Overlap between Morph and Fertility Traits", x="No. Overlap Events", y="No. Simulations") + geom_linerange(x=31, ymax=800, ymin=0, colour="red") + geom_linerange(x=39.57, ymax=800, ymin=0, colour="blue") + geom_linerange(x=20.47, ymax=800, ymin=0, colour="blue")

# Multiple plot function
#
# ggplot objects can be passed in ..., or to plotlist (as a list of ggplot objects)
# - cols:   Number of columns in layout
# - layout: A matrix specifying the layout. If present, 'cols' is ignored.
#
# If the layout is something like matrix(c(1,2,3,3), nrow=2, byrow=TRUE),
# then plot 1 will go in the upper left, 2 will go in the upper right, and
# 3 will go all the way across the bottom.
#
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}

multiplot(p1, p2, p3, p4, p5, p6, cols=2)
