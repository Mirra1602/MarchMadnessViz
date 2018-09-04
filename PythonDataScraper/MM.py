"""
Author: Maria P.
Date: April 2014
Purpose: Parse data from the internet, reformat it and shape it for graphing
Make plots that compare teams and statistics
Specifics: Data is parsed from espn.com site and contains Regular Season data per 
rebounds, assists etc. Approximately 350 teams ; stats go back to 2002

"""
from BeautifulSoup import BeautifulSoup
import urlparse
import urllib2
import pandas as pd
import numpy as np
import cPickle
import matplotlib.pyplot as plt


class HTMLdata(object):
    """
    Parse html data from espn.com 
    """

    def __init__(self, base = 'http://espn.go.com/mens-college-basketball/statistics/team/_/stat/'):
        self.base = base
        self.glossarydict = None
            


    ### Url variables
    #yearList = map(str, range(2002, 2014))
    yearList = [2016]
    metricList = ['rebounds', 'free-throws', '3-points', 'assists', 'steals', 'blocks']
    countList = map(str, range(41, 361, 40))

    
    def urlsCurrent(self):
        """
        Returns a list of urls containing data for the current regular season.
        Year is not contained in the url for current regular season.
        base url -- list of str; each str is a new url
        urlsCurrent(base url) -> list of str
        """

        count0 = map(lambda metric: self.base + '{0}/seasontype/2/'.format(metric), self.metricList)
        urls = [map(lambda count: url + 'count/{0}'.format(count), self.countList) for url in count0]
        urls = sum(urls, []) 
        return count0 + urls # should result in 54 urls 6metrics * 9count pages

    

    def urlsPast(self):
        """
        Returns a list of urls containing data on past regular seasons.
        base url -- list of str
        urlsPast(base url) -> list of str
        """

        count0 = map(lambda metric: self.base + '{0}/seasontype/2/'.format(metric), self.metricList)
        yearUrl = [map(lambda year: url + 'year/{0}'.format(year), self.yearList) for url in count0]
        result1 = sum(yearUrl, [])
        countUrl = [map(lambda count: url + '/count/{0}'.format(count), self.countList) for url in result1]
        result2 = sum(countUrl, [])
        return result1 + result2 ### len should be 648 = (6(metric groups * 9(count pages) * 12(year groups))


 
    def extract_htmldata(self, urlList):
        """
        Returns html data from each url in a list of urls.
        urlList -- list of str; each str represents a url
        parse_sourse(list) -> list of lists; each list contains list representing the rows of the "table" 
        """

        dataList = [[] for i in range(0, len(urlList) )]
        for i in range(0,len(urlList)):
            html = urllib2.urlopen(urlList[i]).read()
            [dataList[i].append(tr.findAll(text=True)) for tr in BeautifulSoup(html).findAll('tr')] ## get each row of data
            dataList[i].append([BeautifulSoup(html).title.string[ :4]]) # get the season and add to the end of list

        return dataList




    def get_glossary(self):
        """
        Returns a dictionary of abbreviations.
        glossary() -- dict

        """
        if self.glossarydict is None:  
            urls = map(lambda metric: self.base + '{0}/'.format(metric), metricList) ## forms a url for each metric; each metric has different abbreviations

            keys, values = [], []
            for url in urls:
                html = urllib2.urlopen(url).read()
                for link in BeautifulSoup(html).findAll("div", { "class" : "foot-content" }):
                    [keys.append(span.text) for span in link.findAll('span')]
                    [values.append(span.nextSibling) for span in link.findAll('span')]
                self.glossarydict = dict(zip(keys, values))

        return self.glossarydict

    def extract_htmlcolors(url = 'http://dynasties.operationsports.com/team-colors.php?sport=ncaa'):
        """
        Returns a list of team colors 
        """

        colorList = []
        html = urllib2.urlopen(url).read()
        [colorList.append([tr.findAll(text=True)[0],tr.findAll(text=True)[-1]]) for tr in BeautifulSoup(html).findAll('tr')] ## get each row of data
        
        colorList[0] = ['TEAM','color']
        colorData = pd.DataFrame(colorList, columns= colorList[0])
        colorData.to_csv('colorData.csv', encoding='utf-8')
        
        return colorData


class DATA(object):
    """
    Format parsed html data. Initializes with a list containing lists of data from each web page.
    """
    #dataList = cPickle.load(open('dataList.p', 'rb'))
    # def __init__(self, dataList = dataList):
    #     self.dataList = dataList
    def __init__(self):
        pass
    

    def extractTable(self,dataList):
        """
        Formats the data by deleting sub headers and headers that appear within the data.
        Also formats the main header in the presence of double headers.
        dataList -- a list of lists; each list contains list representing the rows of the "table"
        extractTable() -> list
        """

        for data in dataList:
            if len(data[0]) < len(data[-2]):    # subheader distinguishes between Per game and total; after subheader was removed some column names are identical and 
                data[1][4], data[1][5] = data[1][4] + 'PG', data[1][5] + 'PG'   # need to be changed to reflect Per game
                data[1][6], data[1][7] = data[1][6] + 'Total', data[1][7] + 'Total' # and total
            [data.remove(row) for row in data[:-1] if len(row) < len(data[-2])] # data[:-1] to exclude ['2013']
            header = data.pop(0)
            [data.remove(row) for row in data if row[0] == 'RK']
            data.insert(0,header)
        return dataList



    def addSeason(self, dataList):
        """
        Returns formated dataList.
        Adds a 'Season' to the end of header row (first list) of each dataList object.
        Adds season value to end of each list/row within each dataList object.
        Season value is stored at the end of each list object and is poped after it is assimilated in the data.

        dataList -- a list of lists
        addSeason(List) --> list 
        """

        for data in dataList:   # dataList contains a list with data from each url
            data[0].append('Season')    # add column name to the end of header
            [data[i].append(data[-1][0]) for i in range(1,len(data)-1)] # data[-1][i] = ['2013']' add the season value to th end fo each row
            data.pop(-1)

        return dataList



    def combined(self, dataList):
        """
        Recombines the dataList objects per identical header(first row(list)).
        
        dataList -- a list of lists
        combined(dataList) -> list
        """

        dataList.sort()     # dataList contains a list with data from each url
        header = dict((tuple(x[0]), x[1:]) for x in dataList).keys() # get unique headers(first element of each list) by passing them as keys ato a dictionary
        combined = [[] for i in range(0, len(header)) ]
        for i in range(0, len(header)):
            [combined[i].append(data) for data in dataList if data[0] == list(header[i])]   # based on its header group the list into a new list   

        return combined ## each combined list has 117lists = 13season*9pages



    def dfList(self, combined):
        """
        Returns dataframes of the lists passed as an attribute ans passes them to a dfList. 
        Concatinates the dataframes within each dfList into one DataFrame

        combined -- a list of list
        dfList(combined) -> list of dataframes
        """

        dfList = [[] for i in range(0, len(combined))]
        for i in range(0, len(combined)): # each list in combined has lists with identical headers
            for data in combined[i]:
        # have to map the data as it should be a list type but is ResultSet from Beautifulsoup
                dfList[i].append(pd.DataFrame(map(list, data)[1:], columns = map(list, data)[0]) )

        for i in range(0, len(dfList)):
            dfList[i] = pd.concat(dfList[i]) #, ignore_index = True) - shoudld be added to ignore headers but crashes

        return dfList




    def mergeDF(self, df):
        """
        Returns merged dataframes. 
        dfList -> list of dataframes
        mergeDF(dfList) -> dataframe

        """

        for i in range(1,len(df)):
            #colsToUse = (df[i].columns - df[0].columns).tolist() ## to avoid duplicating columns when merging; some columns repeat in the dataframes
            colsToUse = list(set(dfList[i].columns) - set(dfList[0].columns))
            colsToUse.append('TEAM'); colsToUse.append('Season') # need to add TEAM and Season to facilitate merging on those columns
            
            mergeDF = pd.merge(df[0], df[i][colsToUse], how='left', on=['TEAM', 'Season'] )
            df[0] = mergeDF
        mergeDF = mergeDF.drop(['RK'], 1)
        return mergeDF


    # def DFtoCSV(self, dataframe):
    #     dataframe.to_csv('data.csv', encoding='utf-8')



class PlotMM(object):

    data = pd.read_csv('data.csv')

    def __init__(self, data = data):
        self.data = data


    def matchup_graph(self, team1 = 'North Carolina', team2 = 'Duke', metric = 'PPG', year = 2013):
        """
        Returns a barplot of team1 and team2 for the desired metric and year.
        """
        
        tempdf = self.data.loc[((self.data.TEAM == team1) | (self.data.TEAM == team2)) 
                 & (self.data.Season == year), [metric,'TEAM','Season']]
        plotdf = tempdf.pivot(index = 'Season', columns='TEAM', values = metric)
        plot = plotdf.plot(kind='barh', figsize=(10,7))#, xlim = (0,10))
        plot.set_ylabel(metric)
        plt.show()
        # plt.bar((0.5, 1.5), 
        # [  self.data.loc[(self.data.TEAM == team1) & (self.data.Season == year), metric].values[0] 
        # ,  self.data.loc[(self.data.TEAM == team2) & (self.data.Season == year), metric].values[0] ], width=0.2, color=['b','r'])
        # plt.xticks((0.6, 1.6), (team1,team2) )
        return plt.show()



    def team_graph(self, team = 'North Carolina', metric = 'PPG', year = 2013):
        """
        Returns a barplot of team1 and team2 for the desired metric and year.
        """
        
        tempdf = self.data.loc[(self.data.TEAM == team) & (self.data.Season == year), [metric,'TEAM','Season']]
        plotdf = tempdf.pivot(index = 'Season', columns='TEAM', values = metric)
        plotdf.plot(kind='barh', figsize=(8,4))
        plt.show()
        return plt.show()


    def ts_plot(self, team = 'North Carolina',  metric = 'PPG'):
        """
        Returns a plot of a time series plot of the metric for team.
        ts_plot2() -> img
        """

        dftemp = self.data.loc[(self.data.TEAM == team) , [metric, 'Season'] ]
        dftemp = dftemp.sort(['Season'])       

        plot = dftemp.plot(y=metric, x='Season',style='-o')
        plot.set_ylabel(metric)
        plot.set_title(team)
        plt.show()



    def ts_plot2(self, team1 = 'North Carolina', team2 = 'Duke', metric = 'PPG'):
        """
        Returns a plot of a time series plot of the metric for team1 and team2.
        ts_plot2() -> img
        """

        tempdf = self.data.loc[(self.data.TEAM == team1) | (self.data.TEAM == team2), [metric, 'Season', 'TEAM'] ]
        tempdf = tempdf.sort(['Season'])
        plotdf = tempdf.pivot(index = 'Season', columns='TEAM', values = metric)


        plot = plotdf[team1].plot(style='-o', figsize=(10, 7))
        plotdf[team2].plot(style='-o')
        plot.set_ylabel(metric)
        plot.legend()
        # plot.set_title()

        return plt.show()





    def assists_stats(self, team = 'North Carolina', year = 2013):
        """
        Returns a barplot the desired metric for specified tema and year.
        """

        cols = [col for col in self.data.columns if col.startswith('A')] ## extract the columns with assists data
        plotdf = self.data.loc[(self.data.TEAM == team) & (self.data.Season == year), cols]
        plotdf.plot(subplots=True, kind = 'bar')
        return plt.show()


    def blocks_stats(self, team = 'North Carolina', year = 2013):
        """
        Returns a barplot of team1 and team2 for the desired metric and year.
        """

        cols = [col for col in self.data.columns if col.startswith('B')]
        plotdf = self.data.loc[(self.data.TEAM == team) & (self.data.Season == year), cols]
        plotdf.plot(subplots=True, kind = 'bar')
        return plt.show()


    def rebounds_stats(self, team = 'North Carolina'):
        """
        Returns a barplot of team1 and team2 for the desired metric and year.
        """

        cols = [col for col in data.columns if col.startswith('A')]
        plotdf = self.data.loc[(self.data.TEAM == team) & (self.data.Season == year), cols]
        plotdf.plot(subplots=True, kind = 'bar')

        return plt.show()




        




if __name__ == "__main__":
    
    ### HTMLparse class
    parser = HTMLdata()


    #urlList = parser.urlsCurrent() + parser.urlsPast()
    urlList = parser.urlsPast()
    print len(urlList)

    # doc = parser.glossary()

    dataList = parser.extract_htmldata(urlList)
    cPickle.dump(dataList, open('dataList15-16.p', 'wb'))



    ### DATA class
    dataList = cPickle.load(open('dataList15-16.p', 'rb'))

    data = DATA()
    table = data.extractTable(dataList)

    addSeason = data.addSeason(table)

    combined = data.combined(addSeason)

    dfList = data.dfList(combined)

    mDF = data.mergeDF(dfList)
    print mDF.head()


    ### PlotMM class
    # data.DFtoCSV(mDF)

    #plott = PlotMM()
    #plott.ts_plot2()


