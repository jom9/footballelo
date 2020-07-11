from MySQLdb import _mysql
import sys
import scrapeSeason
from datetime import datetime
import requests
def AddSeason(league: str,year: int, db)->None:
    data = scrapeSeason.GetGames(league,year)
    teams = {}

    print(league,year)
    for team in data.keys():
        db.query("SELECT elo FROM teams WHERE name=\""+ team+"\" AND league=\""+league+"\"")
        result = db.store_result()
        #print(result.fetch_row())
        if result.fetch_row() != ():
            #print(result.fetch_row())
            teams[team] =  int(result.fetch_row()[0][0])
        else:
            teams[team] = 1500
    for homeTeam in data.keys():

        for game in data[homeTeam]:
            awayTeam = game[1]
            awayElo = teams[awayTeam]
            homeElo = teams[homeTeam]
            matchResult = game[0]
            scoreHome = int(matchResult.split('–')[0])
            scoreAway = int(matchResult.split('–')[1])
            insertVal = '(\''+str(year)+'\',\''+homeTeam+'\',\''+awayTeam+'\',\''+str(homeElo)+'\',\''+str(awayElo)+'\',\''+str(scoreHome)+'-'+str(scoreAway)+'\')'
            #print("INSERT INTO games (date,team1,team2,elo1,elo2,result) VALUES"+insertVal)
            db.query("INSERT INTO games (date,team1,team2,elo1,elo2,result) VALUES"+insertVal)
            #formulation for elo at http://eloratings.net/about
            # We is expected results, dr is difference in scroe
            dr = homeElo - awayElo
            We =  1.0/(10**(-(dr+100)/400) + 1)
            K = 40
            if scoreHome>scoreAway:#win
                W = 1.0
                if abs(scoreHome-scoreAway) ==1:
                    K=K
                elif abs(scoreHome-scoreAway) ==2:
                    K *= 1.5
                elif abs(scoreHome-scoreAway ==3):
                    K*= 1.75
                else:
                    K += K*(.75+abs(scoreHome-scoreAway)-3)/8
                teams[homeTeam] = int(homeElo + K*(W-We))
                teams[awayTeam] = int(awayElo + K*(0-(1-We)))
            elif scoreHome< scoreAway:
                W = 0
                teams[homeTeam] = int(homeElo + K*(W-We))
                teams[awayTeam] = int(awayElo + K*(1-(1-We)))
            else:
                W = .5
                teams[homeTeam] = int(homeElo + K*(W-We))
                teams[awayTeam] = int(awayElo + K*(W-(1-We)))


    for team in teams:
        db.query("SELECT elo FROM teams WHERE name=\""+ team+"\" AND league=\""+league+"\"")
        result = db.store_result()
        if result.fetch_row() != ():
            db.query("UPDATE teams SET elo=\'"+str(teams[team])+"\' WHERE name=\'"+team+"\'")
        else:
            db.query("INSERT INTO teams (name,elo,league) VALUES(\'"+team+'\',\''+ str(teams[team])+'\',\''+ league+  "\')")

if __name__=="__main__":
    '''
    hst = input("Enter the host URL:")
    usernme = input("Enter the Username:")
    password = input("Enter password:")
    dbnme = input("Enter the database name?")
    '''
    hst = 'sql.njit.edu'
    usernme = 'jom9'
    password = 'G0donlyknows!'
    dbnme = 'jom9'
    db=_mysql.connect(host=hst,user=usernme,passwd=password,db=dbnme)


    while True:
        league = input("Enter the league you wish to add. Enter ALL if you wish to get all available leagues. Enter HELP to get list of all leagues")
        year = input("Enter the year you wish to add. Enter ALL if you wish to get data from every season")
        if league == "HELP":
            for val in scrapeSeason.leagues.keys():
                print(val)
            continue
        elif league == "ALL":
            for le in scrapeSeason.leagues:
                if year == "ALL":
                    for yr in range(  scrapeSeason.leagues[le], datetime.now().year-1):
                        AddSeason(le,yr,db)
                else:
                    AddSeason(le,int(year),db)
            break
        else:
            if year == "ALL":
                for yr in range(  scrapeSeason.leagues[league], datetime.now().year):
                    AddSeason(league,yr,db)
            else:
                AddSeason(league,int(year),db)
