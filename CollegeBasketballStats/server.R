library(shiny)
library(ggplot2)


data2 <- read.csv("./Data/data.csv")
data2 <- data2[, -c(1,9)]


data16 <- read.csv("./Data/data16-17.csv", sep = '\t')
data16 <- data16[, names(data2)]

data15 <- read.csv("./Data/data15-16.csv", sep = '\t')
data15 <- data15[, names(data2)]

data14 <- read.csv("./Data/data14-16.csv")
data14 <- data14[which(data14$Season == 2014), ] #not sure where 2015 data comes from
data14 <- data14[, names(data2)]



data2 <- rbind(data14, data2, data15, data16)
colorData <- read.csv("./Data/colorData.csv")
names(colorData)[c(1,4)] <- c('TEAM','team2') 
data <- merge(data2, colorData)
data$color <- as.character(data$color)
data[data$TEAM == 'North Carolina', 'color'] <- '#A4D3EE'
#data$colour <- '#98BFE5'  


shinyServer(function(input, output) {
  
# to extract color and logo for each team
  firstsub1 <- reactive({
    subset(data, data$TEAM %in% input$team1, select =c('TEAM','color','Logo') )
  })
  
  firstsub2 <- reactive({
    subset(data, data$TEAM %in% input$team2, select =c('TEAM','color','Logo') )
  })
  
# extract data for both teams in one dataframe for the specified metric
  secondsub <- reactive({
    subset(data, data$TEAM %in% input$team1 | data$TEAM %in% input$team2, select = c('TEAM', 'Season', input$stat, 'color') )
    
  })
  
  
  p <- reactive({
    switch(input$stat,
    #APG = ggplot(data = secondsub(), aes(x=factor(Season), y = APG, fill=TEAM)) + 
    #geom_bar(position=position_dodge(), width=.8, stat="identity") + 
    #xlab("Season") + ylab("Average per game") + theme_bw(18) + theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)),

    APG = ggplot(data = secondsub(), aes(x=Season, y = APG, fill=TEAM)) + 
      geom_line(aes(linetype = TEAM )) + geom_point( size=3, shape=21) +
      xlab("Season") + ylab("Average per game") + theme_bw(18) + 
      theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)),
    
    #RPG = ggplot(data = secondsub(), aes(x=factor(Season), y = RPG, fill=TEAM)) + 
    #  geom_bar(position=position_dodge(), width=.8, stat="identity") + 
    #  xlab("Season") + ylab("Average per game") + theme_bw(18)+theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)),    

    RPG = ggplot(data = secondsub(), aes(x=Season, y = RPG, fill=TEAM)) + 
      geom_line(aes(linetype = TEAM )) + geom_point( size=3, shape=21) +
      xlab("Season") + ylab("Average per game") + theme_bw(18) + 
      theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)),
        
    #BLKPG = ggplot(data = secondsub(), aes(x=factor(Season), y = BLKPG, fill=TEAM)) + 
    #  geom_bar(position=position_dodge(), width=.8, stat="identity") + 
    #  xlab("Season") + ylab("Average per game") + theme_bw(18)+theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)),
    
    BLKPG = ggplot(data = secondsub(), aes(x=Season, y = BLKPG, fill=TEAM)) + 
      geom_line(aes(linetype = TEAM )) + geom_point( size=3, shape=21) +
      xlab("Season") + ylab("Average per game") + theme_bw(18) + 
      theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)),    
    
    #TOPG = ggplot(data = secondsub(), aes(x=factor(Season), y = TOPG, fill=TEAM)) + 
    #  geom_bar(position=position_dodge(), width=.8, stat="identity") + 
    #  xlab("Season") + ylab("Average per game") + theme_bw(18)+theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)),
    
    TOPG = ggplot(data = secondsub(), aes(x=Season, y = TOPG, fill=TEAM)) + 
      geom_line(aes(linetype = TEAM )) + geom_point( size=3, shape=21) +
      xlab("Season") + ylab("Average per game") + theme_bw(18) + 
      theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)),     
    
    #STPG = ggplot(data = secondsub(), aes(x=factor(Season), y = STPG, fill=TEAM)) + 
    #  geom_bar(position=position_dodge(), width=.8, stat="identity") + 
    #  xlab("Season") + ylab("Average per game") + theme_bw(18)+theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)),

    STPG = ggplot(data = secondsub(), aes(x=Season, y = STPG, fill=TEAM)) + 
      geom_line(aes(linetype = TEAM )) + geom_point( size=3, shape=21) +
      xlab("Season") + ylab("Average per game") + theme_bw(18) + 
      theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)), 
        
    #PPG = ggplot(data = secondsub(), aes(x=factor(Season), y = PPG, fill=TEAM)) + 
    #  geom_bar(position=position_dodge(), width=.8, stat="identity") + 
    #  xlab("Season") + ylab("Average per game") + theme_bw(18)+theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)),

    PPG = ggplot(data = secondsub(), aes(x=Season, y = PPG, fill=TEAM)) + 
      geom_line(aes(linetype = TEAM )) + geom_point( size=3, shape=21) +
      xlab("Season") + ylab("Average per game") + theme_bw(18) + 
      theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)), 
        
    #FTAPG = ggplot(data = secondsub(), aes(x=factor(Season), y = FTAPG, fill=TEAM)) + 
    #  geom_bar(position=position_dodge(), width=.8, stat="identity") + 
    #  xlab("Season") + ylab("Average per game") + theme_bw(18)+theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)),
 
    FTAPG = ggplot(data = secondsub(), aes(x=Season, y = FTAPG, fill=TEAM)) + 
      geom_line(aes(linetype = TEAM )) + geom_point( size=3, shape=21) +
      xlab("Season") + ylab("Average per game") + theme_bw(18) + 
      theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)),     
       
    #X3PMPG = ggplot(data = secondsub(), aes(x=factor(Season), y = X3PMPG, fill=TEAM)) + 
    #  geom_bar(position=position_dodge(), width=.8, stat="identity") + 
    #  xlab("Season") + ylab("Average per game") + theme_bw(18)+theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)),
 
    X3PMPG = ggplot(data = secondsub(), aes(x=Season, y = X3PMPG, fill=TEAM)) + 
      geom_line(aes(linetype = TEAM )) + geom_point( size=3, shape=21) +
      xlab("Season") + ylab("Average per game") + theme_bw(18) + 
      theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)),     
    
    #ORPG = ggplot(data = secondsub(), aes(x=factor(Season), y = ORPG, fill=TEAM)) + 
    #  geom_bar(position=position_dodge(), width=.8, stat="identity") + 
    #  xlab("Season") + ylab("Average per game") + theme_bw(18)+theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)),

    ORPG = ggplot(data = secondsub(), aes(x=Season, y = ORPG, fill=TEAM)) + 
      geom_line(aes(linetype = TEAM )) + geom_point( size=3, shape=21) +
      xlab("Season") + ylab("Average per game") + theme_bw(18) + 
      theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)), 
        
    #DRPG = ggplot(data = secondsub(), aes(x=factor(Season), y = DRPG, fill=TEAM)) + 
    #  geom_bar(position=position_dodge(), width=.8, stat="identity") + 
    #  xlab("Season") + ylab("Average per game") + theme_bw(18)+theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5)) 
    
    DRPG = ggplot(data = secondsub(), aes(x=Season, y = DRPG, fill=TEAM)) + 
      geom_line(aes(linetype = TEAM )) + geom_point( size=3, shape=21) +
      xlab("Season") + ylab("Average per game") + theme_bw(18) + 
      theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5))
    )
  })

  

  
  
    output$myimage1 <- renderImage({
      # When input$n is 3, filename is ./images/image3.jpeg
      image1 <- normalizePath(file.path('./logos', firstsub1()[1,3]))
      image2 <- normalizePath(file.path('./logos', firstsub2()[1,3]))
      # Return a list containing the filename and alt text
      list(src = image1, #width = 20, height = 20,
           alt = "Image number")
      
    }, deleteFile = FALSE)
  
  output$myimage2 <- renderImage({
    # When input$n is 3, filename is ./images/image3.jpeg
      image2 <- normalizePath(file.path('./logos', firstsub2()[1,3]))
                                                    
      # Return a list containing the filename and alt text
    list(src = image2, #width = 20, height = 20,
              alt = "Image number")
                                                         
  }, deleteFile = FALSE)
  
  
  
  
  output$plot <- renderPlot({
    color1 <- firstsub1()[1,2] 
    color2 <- firstsub2()[1,2] 
    #color1 <- '#000080' 
    #color2 <- '#87CEFA' 
    if (as.character(firstsub1()[1,1]) < as.character(firstsub2()[1,1]) ){
      myPalette <- c(color1 , color2)
      p() + scale_fill_manual(values=myPalette)}
    else {
      myPalette <- c(color2 , color1)
      p() + scale_fill_manual(values=myPalette)}

  })
  

})


