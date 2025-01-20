from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView

from .forms import *


class GamesHome(ListView):
    paginate_by = 8
    model = Games
    template_name = 'games/games_home.html'
    context_object_name = 'games'

    def get_queryset(self):
        queryset = super().get_queryset()

        form_filter = self.get_form()
        if form_filter.is_valid():
            category = form_filter.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(cat_id=category.id)

            platform = form_filter.cleaned_data.get('platform')
            if platform:
                queryset = queryset.filter(platforms__in=[platform])

            release_date = form_filter.cleaned_data.get('date')
            if release_date == 'last_month':
                last_month = now() - timedelta(days=30)
                queryset = queryset.filter(date__gte=last_month)
            elif release_date == 'last_year':
                last_year = now() - timedelta(days=365)
                queryset = queryset.filter(date__gte=last_year)

            search = form_filter.cleaned_data.get('search')
            if search:
                queryset = queryset.filter(title__icontains=search)

        return queryset

    def get_form(self):
        return GameFilterForm(self.request.GET)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_filter'] = self.get_form()
        return context

class GamesDetailView(DetailView):
    model = Games
    template_name = 'games/details_view.html'
    slug_url_kwarg = 'game_slug'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['favorites'] = Favorite.objects.filter(user=self.request.user).values_list('game_id', flat=True)
        else:
            context['favorites'] = []
        context['authenticated'] = self.request.user.is_authenticated
        return context

class GamesUpdateView(LoginRequiredMixin, UpdateView):
    form_class = GamesForm
    model = Games
    template_name = 'games/create.html'
    slug_url_kwarg = 'game_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Форма редагування гри'
        return context


class CreateGamesView(LoginRequiredMixin, CreateView):
    form_class = GamesForm
    template_name = 'games/create.html'
    success_url = reverse_lazy('games_home')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Форма створення нової гри'
        return context

class GamesDeleteView(LoginRequiredMixin, DeleteView):
    model = Games
    success_url = '/games/'
    slug_url_kwarg = 'game_slug'
    template_name = 'games/games_delete.html'

@login_required
def add_to_favorites(request, game_slug):
    if request.method == 'POST':
        game = get_object_or_404(Games, slug=game_slug)
        favorite, created = Favorite.objects.get_or_create(user=request.user, game=game)

        if created:
            messages.success(request, f"Гра '{game.title}' додана до вподобань.")
    return redirect('game_details', game_slug=game_slug)

@login_required
def delete_from_favorites(request, game_slug):
    if request.method == 'POST':
        game = get_object_or_404(Games, slug=game_slug)
        favorite = Favorite.objects.filter(user=request.user, game=game).first()

        favorite.delete()
        messages.success(request, f"Гра '{game.title}' видалена з вподобань.")
    return redirect('game_details', game_slug=game_slug)

class FavoriteGamesView(ListView):
    paginate_by = 5
    model = Favorite
    template_name = 'games/games_home.html'
    context_object_name = 'games'

    def get_queryset(self):
        return Games.objects.filter(favorite__user=self.request.user)