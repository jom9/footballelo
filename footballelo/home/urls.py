from django.urls import path

from . import views

urlpatterns = [
    path('Home', views.home, name='home'),
    path('genImg', views.genImg, name='genImg'),
    path('About', views.about, name='about'),
    path('Api', views.api, name='API'),
]
