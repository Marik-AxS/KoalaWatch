from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.db.models import Q, Count
from django.contrib import messages
from .models import *
from .forms import *

class AnimeDetailView(DetailView):
    model = Anime
    template_name = 'pages/anime_details.html'
    context_object_name = 'anime'
    queryset = Anime.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)
        context['comment_form'] = CommentForm()
        anime = self.object
        genres = anime.genre.all()

        if genres.exists():
            genre_ids = genres.values_list('id', flat=True)

            analogs = Anime.objects.filter(genre__id__in=genre_ids).exclude(id=anime.id) \
                .annotate(num_genres=Count('genre')).filter(num_genres__gte=2)
        else:
            analogs = Anime.objects.none()
        context['analogs'] = analogs
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            messages.error(request, "Вы должны быть авторизованы, чтобы оставить комментарий.")
            return redirect('anime_details', pk=self.object.pk)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            comment.save()
            return redirect('anime_details', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))


class AnimeWatchingView(DetailView):
    model = Anime
    template_name = 'pages/anime_watching.html'
    context_object_name = 'watching'
    queryset = Anime.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        anime = self.object
        episode_id = self.request.GET.get('episode_id')
        context['comment_form'] = CommentForm()

        if anime.anime_type == 'series':
            context['episodes'] = anime.episodes.order_by('season__season_number', 'episode_number')

            if episode_id:
                episode = get_object_or_404(anime.episodes, id=episode_id)
                context['episode'] = episode
                context['episode_file'] = episode.file if episode else None
                context['comments'] = Comment.objects.filter(post=self.object, episode=episode)
            else:
                episode = anime.episodes.order_by('episode_number').first()
                context['episode'] = episode
                context['episode_file'] = episode.file if episode else None
                context['comments'] = Comment.objects.filter(post=self.object, episode=episode)
        else:
            context['episode_file'] = anime.anime_file
            context['comments'] = Comment.objects.filter(post=self.object, episode=None)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object

            episode_id = request.GET.get('episode_id')
            if episode_id:
                comment.episode = get_object_or_404(self.object.episodes, id=episode_id)
            else:
                comment.episode = None

            comment.save()
            if Anime.anime_type == 'movie':
                return redirect('anime_watching', pk=self.object.pk)
            else:
                return redirect(f"{self.request.path}?episode_id={episode_id}")

        return self.render_to_response(self.get_context_data(form=form))

class StudioDetailView(DetailView):
    model = Studio
    template_name = 'pages/studio_details.html'
    context_object_name = 'studio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['studios_anime'] = Anime.objects.filter(studios=self.object)
        context['all_studios'] = Studio.objects.all()
        return context


class AnimeListView(ListView):
    model = Anime
    template_name = 'pages/all.html'
    context_object_name = 'list_anime'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Genre.objects.all()
        context['search_form'] = SearchForm(self.request.GET)

        genre_slug = self.request.GET.get('genre_slug')
        if genre_slug:
            context['selected_genre'] = Genre.objects.filter(slug=genre_slug).first()
        return context


    def get_queryset(self):
        query = self.request.GET.get('query')
        genre = self.request.GET.get('genre_slug')
        rating = self.request.GET.get('rating')
        new_release = self.request.GET.get('release')
        movies = self.request.GET.get('movie')
        queryset = Anime.objects.all()

        if genre:
            queryset = queryset.filter(genre__slug=genre)


        if rating == 'popular':
            queryset = queryset.order_by('-rating')

        if new_release == 'created_at':
            queryset = queryset.order_by('-created_at')

        if movies == 'film':
            queryset = queryset.filter(anime_type='movie')

        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset





