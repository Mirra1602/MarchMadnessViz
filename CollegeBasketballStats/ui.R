library(shiny)

data <- read.csv("./Data/data.csv")

shinyUI(fluidPage(titlePanel(title ='Division I College Basketball Compare Team Performance'),
  fluidRow(
    column(4,      
      selectInput("team1", label = h3("Select Team 1"), 
                  choices = attributes(data$TEAM), selected = 'Duke' ) 
          )
    ),
  fluidRow(
    column(4,
      selectInput("team2", label = h3("Select Team 2"), 
                  choices = attributes(data$TEAM), selected = 'North Carolina')
        )),
  fluidRow(
    column(4,
      radioButtons("stat", label = h3("Select Stat"),
                   choices = list("Assists" = 'APG', "Rebounds" = 'RPG', "Blocks" = 'BLKPG'
                                  , "Turn Overs" = 'TOPG'
                                  , "Steals" = 'STPG'
                                  , "Points Per Game" = 'PPG'
                                  , "Free Throws" = 'FTAPG'
                                  , "Three Pointers" = 'X3PMPG'
                                  , "Offensive rebounds" = 'ORPG'
                                  , "Deffensive rebounds" = 'DRPG'
                   ), selected = 'PPG' )
          ), 
    column(8,
          plotOutput("plot"))
      )
  , 
  fluidRow(
    column(3, offset = 5,
           imageOutput("myimage1")),
    column(3,
           imageOutput("myimage2"))
    )
  
  ))