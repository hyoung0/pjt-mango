from django.shortcuts import render, redirect
from .models import Store
from .forms import StoreForm

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


def detail(request, store_pk: int):
    store = Store.objects.get(pk=store_pk)
    
    context = {
        'store':store,
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