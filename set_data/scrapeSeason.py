
import sys
import requests
from bs4 import element
from bs4 import BeautifulSoup
from typing import List
import re
from unicodedata import normalize
leagues = {'EPL':1992,'LaLiga':1997,'Bundesliga':1963,'Serie A':1955}





def BuildLink(league: str, year: int)->str:
    if league == 'EPL':
        if year>2006:
            return "https://en.wikipedia.org/wiki/"+str(year)+'-'+str(year+1)[-2:]+"_Premier_League"
        elif year<=2006 and year>=1992:
            return "https://en.wikipedia.org/wiki/"+str(year)+'-'+str(year+1)[-2:]+"_FA_Premier_League"
        else:
            raise Exception("Sorry that year is not in record")
    elif league == 'LaLiga':
        if year == 1999:
            return "https://en.wikipedia.org/wiki/1999-2000_La_Liga"
        elif year>=1997:
            return "https://en.wikipedia.org/wiki/"+str(year)+'-'+str(year+1)[-2:] +"_La_Liga"
        raise Exception("Sorry that year is not in record")
    elif league == 'Bundesliga':
        if year == 1999:
            return "https://en.wikipedia.org/wiki/1999-2000_Bundesliga"
        if year>=1963:
            return "https://en.wikipedia.org/wiki/"+str(year)+'-'+str(year+1)[-2:] +"_Bundesliga"
    elif league == 'Serie A':
        if year>= 1955:
            return "https://en.wikipedia.org/wiki/"+str(year)+'-'+str(year+1)[-2:] +"_Serie_A"
    raise Exception("Sorry, this leagues is not supported? Try using on of these:",leagues)
def GetTeams(teams: List[element.Tag] )->List[str]: #takes in a soup element tag( i.e the table) and gets all the teams an returns it in a list
        teamNames = []
        for i in range(len(teams)):
            if i==0:
                continue
            if teams[i].find("th").find("a") is None:
                teamNames += [" ".join( teams[i].find("th").get_text(strip=True).replace('\n','').replace(u'\xa0',u' ').split())]
            else:
                teamNames += [  " ".join( teams[i].find("th").find("a").get_text(strip=True).replace('\n', '').replace(u'\xa0',u' ').split())]
            #\xa0 is caused by an error in 2016 LaLiga!
        print(teamNames)
        return teamNames
def BreakDownTable(teams : List[element.Tag] ) -> dict:
    Games = {} # performance by dict with keys are the team name and the value is a list of home games
    teamNames = GetTeams(teams)#gets team names
    for i in range(len(teams)):#goes through the rows of table
        if i==0:#ignore the first one since it just has the team names that are shortended
            continue

        if teams[i].find("th").find("a") is None:
            teamName = " ".join( teams[i].find("th").get_text(strip=True).replace('\n','').replace(u'\xa0',u' ').split())
        else:
            teamName = " ".join(teams[i].find("th").find("a").get_text(strip=True).replace('\n', '').replace(u'\xa0',u' ').split())# get the team name
        Games[teamName] = []# make a list of all the games played at home
        j=0
        for game in teams[i].find_all('td'):
            if re.compile("\d+").match(game.text.replace('\n', '')):
                awayTeam = teamNames[j].replace('\n', '')
                res = ''.join(c for c in game.text[:-1] if c.isdigit() or c=='–')
                Games[teamName] += [(res,awayTeam)]# added with score string then away team
            j+=1

    return Games
def GetGames(league,season):
    targetLeague = league
    targetSeason = season
    page = requests.get(BuildLink(targetLeague,targetSeason))

    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find("table", class_="wikitable plainrowheaders")
    L = BreakDownTable(table.find_all('tr') )
    #print(L)
    return L
if __name__ == "__main__":
    targetLeague = sys.argv[1]
    targetSeason = int(sys.argv[2])
    page = requests.get(BuildLink(targetLeague,targetSeason))

    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find("table", class_="wikitable plainrowheaders")

    print(BreakDownTable(table.find_all('tr') ) )
