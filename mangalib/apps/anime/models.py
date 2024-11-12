from django.db import models
from django.db import models

class Studio(models.Model):
    studios_name = models.CharField('Название студии', max_length=70)
    description = models.TextField('Описание', null=True, blank=True)
    image = models.ImageField('Фото', upload_to='studios_image/', null=True, blank=True)

    def __str__(self):
        return self.studios_name

    class Meta:
        verbose_name = 'Студия'
        verbose_name_plural = 'Студии'


class Age(models.Model):
    name = models.CharField('Возрастное ограничение', max_length=100)
    slug = models.SlugField('слаг', max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ограничение'
        verbose_name_plural = 'Ограничения'


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=100)
    slug = models.SlugField('слаг', max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Status(models.Model):
    name = models.CharField('Статус', max_length=100)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Anime(models.Model):
    ANIME_TYPE_CHOICES = [
        ('series', 'Сериал'),
        ('movie', 'Полнометражный'),
    ]
    name = models.CharField('Название', max_length=150)
    original_name = models.CharField('Оригинальное название', max_length=150)
    description = models.TextField('Описание')
    cover = models.ImageField('Обложка', upload_to='anime_cover/')
    banner = models.ImageField('Баннер', upload_to='banner/', blank=True, null=True)
    age_limit = models.ForeignKey(Age, on_delete=models.CASCADE, related_name='age_limit')  
    rating = models.DecimalField('Рейтинг', max_digits=3, decimal_places=1, default=0.0, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='Статус', null=True, blank=True)
    year_of_manufacture = models.CharField("Год выхода", null=True, blank=True)
    studios = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='Студия')
    author = models.CharField('Автор', max_length=70, null=True, blank=True)
    genre = models.ManyToManyField(Genre, related_name='Жанр')
    duration = models.CharField('Длительность серии', max_length=50, null=True, blank=True)
    duration_film = models.CharField('Длительность фильма', max_length=50, null=True, blank=True)
    total_episodes = models.IntegerField('Всего серий', null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    anime_type = models.CharField('Тип аниме', max_length=10, choices=ANIME_TYPE_CHOICES)

    anime_file = models.FileField('Аниме файл', upload_to='movies/', null=True, blank=True)


    series_files = models.ManyToManyField('Episode', related_name='anime_series', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Анимация'
        verbose_name_plural = 'Анимации'


class Season(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='seasons')
    season_number = models.IntegerField('Номер сезона')
    title = models.CharField('Название сезона', max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.anime.name} - Сезон {self.season_number}"


class Episode(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='episodes')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes', null=True, blank=True)
    episode_number = models.IntegerField('Номер серии')
    title = models.CharField('Название серии', max_length=150)
    file = models.FileField('Файл серии', upload_to='episodes/')

    def __str__(self):
        season_part = f" - Сезон {self.season.season_number}" if self.season else ""
        return f"{self.anime.name}{season_part} - Серия {self.episode_number}"

class StarRating(models.Model):
    value = models.IntegerField('Значение')

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'

    def __str__(self):
            return f"{self.value}"

class Rating(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='rating_user')
    stars = models.ForeignKey(StarRating, on_delete=models.CASCADE)
    film = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='rating_anime')
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        ordering = ['-created']

    def __str__(self):
        return f'{self.film} - {self.stars}'

class Comment(models.Model):
    post = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='comments_author')
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


# Create your models here.
