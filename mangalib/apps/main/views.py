from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView
from ..anime.models import *


class HomeView(TemplateView):
    template_name = 'pages/index.html'
    model = Anime
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anime'] = Anime.objects.all()
        context['populars'] = Anime.objects.all().order_by('-rating')
        context['latest_releases'] = Anime.objects.all().order_by('-created_at')
        context['movies'] = Anime.objects.filter(anime_type='movie')
        context['top_views'] = Anime.objects.order_by('-view_count')[:5]
        return context