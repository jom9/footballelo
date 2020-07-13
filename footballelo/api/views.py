from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt#this is an api no cookies are sent hence no csrf
from django.db import connection

@csrf_exempt
def home(request):
    if request.POST:
        print(str(request.POST))
        if request.POST['team']:
            team = request.POST['team']
        if request.POST['league']:
            league = request.POST['league']
        if league and team:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM teams WHERE name=%s AND league=%s",[team,league])
                row = cursor.fetchone()
                return HttpResponse(str(row))
        return HttpResponse(str(request.POST))
    return HttpResponse("{}")
    #return render(request,'base.html',{'body':'hello'})
    #return HttpResponse("Hello, world.")
