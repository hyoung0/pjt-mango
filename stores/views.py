from django.shortcuts import render, redirect
from .models import Store
from .forms import StoreForm
from django.db.models import Prefetch, Count, Q
from reviews.models import Review, Emote
import requests, json

# Create your views here.
def index(request):
    stores = Store.objects.all()
    context = {
        'stores': stores,
    }
    return render(request, 'stores/index.html', context)


def get_location(address: str):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    headers = {"Authorization": "KakaoAK 7efccf8a0b485cae348d86aee268d72b"}
    api_json = json.loads(str(requests.get(url,headers=headers).text))
    if not api_json['documents']:
        return {"lat": None, "lng": None}
    
    address = api_json['documents'][0]['address']
    crd = {"lat": str(address['y']), "lng": str(address['x'])}
    address_name = address['address_name']

    return crd
    
    
def create(request):
    if not request.user.is_superuser:
        return redirect('stores:index')
    
    if request.method == 'GET':
        form = StoreForm()
    else:
        form = StoreForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            if store.address:
                pos = get_location(store.address)
                store.latitude = pos.get('lat')
                store.longitude = pos.get('lng')
            form.save()
            return redirect('stores:index')
    
    context = {
        'form': form,
    }
    return render(request, 'stores/create.html', context)


def detail(request, store_pk: int):
    store = Store.objects.get(pk=store_pk)
    if request.user.is_authenticated:
        reviews = Review.objects.filter(store=store).prefetch_related(
            Prefetch('emote_set', queryset=Emote.objects.filter(emotion=1), to_attr='likes'),
            Prefetch('emote_set', queryset=Emote.objects.filter(emotion=1, user=request.user), to_attr='like_exist'),
            Prefetch('emote_set', queryset=Emote.objects.filter(emotion=2), to_attr='dislikes'),
            Prefetch('emote_set', queryset=Emote.objects.filter(emotion=2, user=request.user), to_attr='dislike_exist')
        )
    else:
        reviews = Review.objects.filter(store=store).prefetch_related(
            Prefetch('emote_set', queryset=Emote.objects.filter(emotion=1), to_attr='likes'),
            Prefetch('emote_set', queryset=Emote.objects.filter(emotion=2), to_attr='dislikes'),
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
        form = StoreForm(data=request.POST, files=request.FILES, instance=store)
        if form.is_valid():
            store = form.save(commit=False)
            if store.address:
                pos = get_location(store.address)
                store.latitude = pos.get('lat')
                store.longitude = pos.get('lng')
            form.save()
            return redirect('stores:index')
    
    context = {
        'form': form,
        'store': store,
    }
    return render(request, 'stores/update.html', context)


def redirect_index(request):
    return redirect('stores:index')