
from django.urls import path
from map import views

appname = 'map'

urlpatterns = [
    path('', views.default_map, name="default"),
    
]
