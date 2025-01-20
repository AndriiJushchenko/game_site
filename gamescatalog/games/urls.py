from django.urls import path
from . import views

urlpatterns = [
    path('', views.GamesHome.as_view(), name='games_home'),
    path('favorites', views.FavoriteGamesView.as_view(), name='favorites'),
    path('create', views.CreateGamesView.as_view(), name='create'),
    path('<slug:game_slug>', views.GamesDetailView.as_view(), name='game_details'),
    path('<slug:game_slug>/update', views.GamesUpdateView.as_view(), name='games_update'),
    path('<slug:game_slug>/delete', views.GamesDeleteView.as_view(), name='games_delete'),
    path('<slug:game_slug>/add_favorite', views.add_to_favorites, name='add_favorite'),
    path('<slug:game_slug>/delete_favorite', views.delete_from_favorites, name='delete_favorite')
]