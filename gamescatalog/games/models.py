from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
class Categories(models.Model):
    name = models.CharField('Категорія', max_length=50, db_index=True)
    slug = models.SlugField('URL', max_length=50, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['id']


class Platforms(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField('URL', max_length=50, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Платформа'
        verbose_name_plural = 'Платформи'
        ordering = ['id']


class Games(models.Model):
    title = models.CharField('Назва', max_length=255)
    slug = models.SlugField('URL', max_length=255, unique=True, db_index=True)
    developer = models.CharField('Розробник', max_length=100)
    date = models.DateField('Дата релізу')
    description = models.TextField('Опис гри')
    image = models.ImageField(upload_to='game_images/')
    trailer_url = models.URLField(blank=True, null=True)
    platforms = models.ManyToManyField(Platforms)
    cat = models.ForeignKey('Categories', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('game_details', kwargs={'game_slug': self.slug})

    class Meta:
        verbose_name = 'Гра'
        verbose_name_plural = 'Ігри'
        ordering = ['id']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if Games.objects.filter(slug=self.slug).exclude(id=self.id).exists():
            raise ValidationError(f"Гра з назвою '{self.title}' вже існує. Будь ласка змініть назву гри.")
        super().save(*args, **kwargs)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Games, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"

    class Meta:
        verbose_name = 'Вподобання'
        verbose_name_plural = 'Вподобання'
        ordering = ['id']
        unique_together = ('user', 'game')