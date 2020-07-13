from django.shortcuts import render
from django.db import connection
import flag

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

            #D['topteams'] +=[(team[0],team[1],'\u2690')]

    return render(request,'home.html',D)
