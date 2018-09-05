# MarchMadnessViz

This project scrapes various KPIs fron espn's website using python and builds an intrative visualization in r-Shiny. 
The final result can be seen here:
https://vizbon.shinyapps.io/CollegeBasketballStats/

The project consists of two parts. First one, PythonDataScraper, has two main classes. One consists of fucntions which define and scrape multiple pages of data from Espn website. In the second class, using panda, the data is transformed into a standart dataframe for graphing. There is also a small class with functions for basic plotting using matplotlib.


Second part of the project is in CollegeBasketBallStats. I build a r-shiny app using the scraped data, teams logos and colors.
