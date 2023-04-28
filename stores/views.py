from django.shortcuts import render, redirect
from .models import Store
from .forms import StoreForm
from django.db.models import Avg, Prefetch, Count, Case, When, Q
from reviews.models import Review, Emote

# Create your views here.
def index(request):
    stores = Store.objects.all()
    context = {
        'stores': stores,
    }
    return render(request, 'stores/index.html', context)


def create(request):
    if not request.user.is_superuser:
        return redirect('stores:index')
    
    if request.method == 'GET':
        form = StoreForm()
    else:
        form = StoreForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('stores:index')
    
    context = {
        'form': form,
    }
    return render(request, 'stores/create.html', context)


EMOTIONS = [
    {'label': '좋아요;', 'value': 1},
    {'label': '싫어요', 'value': 2},
]

def detail(request, store_pk: int):
    store = Store.objects.get(pk=store_pk)
    reviews = Review.objects.filter(store=store).annotate(
        likes=Count('emote', filter=Q(emote__emotion='1')),
        dislikes=Count('emote', filter=Q(emote__emotion='2')),
    )
    context = {
        'store':store,
        'reviews': reviews,
    }
    return render(request, 'stores/detail.html', context)


def delete(request, store_pk: int):
    if not request.user.is_superuser:
        return redirect('stores:index')
    
    store = Store.objects.get(pk=store_pk)
    store.delete()
    return redirect('stores:index')


def update(request, store_pk: int):
    if not request.user.is_superuser:
        return redirect('stores:index')
    
    store = Store.objects.get(pk=store_pk)
    if request.method == 'GET':
        form = StoreForm(instance=store)
    else:
        form = StoreForm(data=request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect('stores:index')
    
    context = {
        'form': form,
    }
    return render(request, 'stores/update.html', context)