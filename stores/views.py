from django.shortcuts import render, redirect
from .models import Store, StoreImage
from .forms import StoreForm, StoreImageForm
from django.db.models import Prefetch, Count, Q
from reviews.models import Review, Emote
import requests, json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    stores = Store.objects.all()
    context = {
        'stores': stores,
    }
    return render(request, 'stores/index.html', context)


def all_stores(request):
    stores = Store.objects.all()
    context = {
        'stores': stores,
    }
    return render(request, 'stores/all_stores.html', context)


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
    
    if request.method == 'POST':
        store_form = StoreForm(data=request.POST, files=request.FILES)
        store_image_form = StoreImageForm(data=request.POST, files=request.FILES)
        files = request.FILES.getlist('image')
        if store_form.is_valid() and store_image_form.is_valid():
            store = store_form.save(commit=False)
            if store.address:
                pos = get_location(store.address)
                store.latitude = pos.get('lat')
                store.longitude = pos.get('lng')
            store.save()

            for file in files:
                StoreImage.objects.create(store=store, image=file)

            return redirect('stores:detail', store.pk)
    else:
        store_form = StoreForm()
        store_image_form = StoreImageForm()
    context = {
        'store_form': store_form,
        'store_image_form': store_image_form,
    }
    return render(request, 'stores/create.html', context)


def detail(request, store_pk: int):
    store = Store.objects.get(pk=store_pk)
    store_images = StoreImage.objects.filter(store=store)
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
        'store_images': store_images,
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
    store_image = StoreImage.objects.filter(store=store)
    if request.method == 'POST':
        store_form = StoreForm(data=request.POST, files=request.FILES, instance=store)
        store_image_form = StoreImageForm(data=request.POST, files=request.FILES)
        files = request.FILES.getlist('image')
        if store_form.is_valid() and store_image_form.is_valid():
            store = store_form.save(commit=False)
            if store.address:
                pos = get_location(store.address)
                store.latitude = pos.get('lat')
                store.longitude = pos.get('lng')
            store.save()

            for file in files:
                StoreImage.objects.create(store=store, image=file)

            return redirect('stores:detail', store.pk)
    else:
        store_form = StoreForm(instance=store)
        store_image_form = StoreImageForm()

    context = {
        'store_form': store_form,
        'store_image_form': store_image_form,
        'store': store,
    }
    return render(request, 'stores/update.html', context)


def redirect_index(request):
    return redirect('stores:index')


def search(request):
    if request.method == 'POST':
        search = request.POST['search']        
        store = Store.objects.filter(name__contains=search)
        print(store)
        return render(request, 'stores/search.html', {'search': search, 'store': store})
    else:
        return render(request, 'stores/search.html', {})
    

@login_required
def like_stores(request, store_pk):
    store = Store.objects.get(pk=store_pk)
    me = request.user
    if store.like_users.filter(pk=request.user.pk).exists():
        store.like_users.remove(request.user)
        is_liked = False
    else:
        store.like_users.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
    }
    return JsonResponse(context)


def category(request, subject):
    subject = subject
    store = Store.objects.filter(category=subject).order_by('-pk')
    context = {
        'subject': subject,
        'store': store,
    }
    return render(request, 'stores/category.html', context)

