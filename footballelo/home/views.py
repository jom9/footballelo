from django.shortcuts import render
from django.db import connection
import flag
from django.http import HttpResponse
from django import forms
import requests
from django.contrib.sites.shortcuts import get_current_site
class teamForm(forms.Form):
    homeTeam = forms.CharField(label='Home Team', max_length=100)
    awayTeam = forms.CharField(label='Away Team', max_length=100)
def home(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM teams ORDER BY elo DESC")
        teams = cursor.fetchmany(25)
        D = {'topteams':[]}
        for team in teams:

            if team[2] == 'LaLiga':
                D['topteams'] +=[(team[0],team[1],'ESP.png' )]
            elif team[2] == 'EPL':
                D['topteams'] +=[(team[0],team[1],'ENG.png')]
            elif team[2] == 'Bundesliga':
                D['topteams'] +=[(team[0],team[1],'GER.png')]
            elif team[2] == 'Serie A':
                D['topteams'] +=[(team[0],team[1],'ITA.png')]
            else:
                D['topteams'] +=[(team[0],team[1],'\u2690')]

            # We = P(A) + .5*P(AB)
    if request.method == 'POST':
        form = teamForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                print(request.POST)
                awayTeam = request.POST['awayTeam']
                homeTeam = request.POST['homeTeam']

                cursor.execute("SELECT elo FROM teams WHERE name=%s",[homeTeam])

                homeElo = cursor.fetchone()
                cursor.execute("SELECT elo FROM teams WHERE name=%s",[awayTeam])
                awayElo = cursor.fetchone()
                if homeElo is None or awayElo is None:
                    D['Info'] = 'Sorry that team was not found, try something else'
                    D['homeWinPer'] = ''
                    D['awayWinPer'] = ''
                else:
                    D['Info'] = 'Curious to see how a team performs in a hypothetical match? Enter a home team and an away team to see the probabilty of each outcome'
                #print(homeTeam,awayTeam,homeElo,awayElo)
                    homeElo= homeElo[0]
                    awayElo= awayElo[0]
                    dr = homeElo - awayElo
                    We =  1.0/(10**(-(dr+100)/400) + 1)
                    D['homeWinPer'] = round(We,4)*100
                    D['awayWinPer'] = round(1-We,4)*100
    else:
        D['Info'] = 'Curious to see how a team performs in a hypothetical match? Enter a home team and an away team to see the probabilty of each outcome'
        form = teamForm()
        D['homeWinPer'] = ''
        D['awayWinPer'] = ''
    D['form'] = form
    return render(request,'home.html',D)
def api(request):
    return render(request,'api.html')
def about(request):
    return render(request,'about.html')
def genImg(request):
    numOfTop = 7
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM teams ORDER BY elo DESC")
        teams = cursor.fetchmany(numOfTop)
        D = {'topteams':[]}
        for team in teams:

            if team[2] == 'LaLiga':
                D['topteams'] +=[(team[0],'LaLiga' )]
            elif team[2] == 'EPL':
                D['topteams'] +=[(team[0],'EPL')]
            elif team[2] == 'Bundesliga':
                D['topteams'] +=[(team[0],'Bundesliga')]
            elif team[2] == 'Serie A':
                D['topteams'] +=[(team[0],'Serie A')]
            else:
                D['topteams'] +=[(team[0],'NA')]
        teams = {}
        for topteam in D['topteams']:
            cursor.execute("SELECT * FROM games WHERE team1 = %s OR team2=%s ORDER BY date ASC",[topteam[0],topteam[0]])
            games = cursor.fetchall()
            teams[topteam] = []
            for game in games:
                teams[topteam]+=[game]
        import numpy as np
        import matplotlib.pyplot as plt
        print(plt.style.available)
        #plt.style.use(['dark_background', 'presentation'])
        plt.style.use(['dark_background'])
        scores = []
        years = []
        plots = []
        i = 0
        fig, ax = plt.subplots()
        for team in teams.keys():
            scores+=[[]]
            years += [[]]
            j = 0
            gamesPerSeason = {}
            for game in teams[team]:
                #print(game)
                if int(game[0])<2000:
                    continue
                else:
                    print(game)
                    if int(game[0])  in gamesPerSeason.keys():

                        gamesPerSeason[int(game[0])]+=1
                    else:
                        gamesPerSeason[int(game[0])] = 0
                    if team[1] == 'Bundesliga':
                        years[-1] += [int(game[0]) + gamesPerSeason[int(game[0])]/34.0]
                    else:
                        years[-1] += [int(game[0]) + gamesPerSeason[int(game[0])]/38.0]
                    print(game[1],team[0],game[1]==team[0])
                    if game[1]==team[0]:
                        scores[-1]+=[int(game[3])]
                        print(scores[-1][-1])
                    else:
                        scores[-1]+=[int(game[4])]
                        print(scores[-1][-1])
                j +=1
            #print(len(years[-1]),team)
            plots +=[ ax.plot(years[-1],scores[-1],label=team[0])]
        legend = ax.legend(  fontsize='x-large',bbox_to_anchor=(1, .75),fancybox=True, framealpha=0.5)
        plt.xlabel("Year")
        plt.ylabel("ELO rating")
        #plt.show()
        plt.savefig('home\\static\\ratingsplot.png',bbox_inches='tight',transparent=True)
        plt.close()
    return HttpResponse('Done')
