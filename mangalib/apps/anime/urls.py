from django.urls import path
from .views import *

urlpatterns = [
    path('anime_details/<int:pk>/', AnimeDetailView.as_view(), name='anime_details'),
    path('anime_watching/<int:pk>/', AnimeWatchingView.as_view(), name='anime_watching'),
    path('studio_details/<int:pk>/', StudioDetailView.as_view(), name='studio'),
    path('anime_list/', AnimeListView.as_view(), name='anime_list'),
]