from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request,'base.html',{'body':'hello'})
    #return HttpResponse("Hello, world.")
