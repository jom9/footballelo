from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt#this is an api no cookies are sent hence no csrf
from django.db import connection
import json
@csrf_exempt
def home(request):
    if request.POST:

        if request.POST['team'] and request.POST['league']:
            team = request.POST['team']
            league = request.POST['league']

        if league and team:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM teams WHERE name=%s AND league=%s",[team,league])
                row = cursor.fetchone()
                return HttpResponse(json.JSONEncoder().encode({row[0]:row[1]}))
        return HttpResponse('{}')

    return HttpResponse("{}")
@csrf_exempt
def games(request):
    if request.POST:
        if request.POST['team'] and request.POST['league']:
            team = request.POST['team']
            league = request.POST['league']
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM games WHERE team1=%s OR team2=%s ORDER BY date ASC",[team,team])
                rows = cursor.fetchall()
                games =[]
                for row in rows:
                    games+=[row]
                return HttpResponse(json.JSONEncoder().encode({team:games}))
    return HttpResponse("{}")
