from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.game_hub, name='game'),      
                        path('hub/', views.game_hub, name='game_hub'),                    # Game Hub (list of games)
    path('firewall/', views.firewall_game, name='firewall'),        # Game 1: Firewall Guardian
    path('memory/', views.memory_game, name='memory'),              # Game 2: Code Memory Matrix
    path('typespeed/', views.typespeed_game, name='typespeed'),     # Game 3: C++ Type Speed
    path('update_xp/', views.update_xp, name='update_xp'),         # XP updater API
]
