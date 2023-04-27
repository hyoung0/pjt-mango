from django.shortcuts import render, redirect
from .models import Store
from .forms import StoreForm

# Create your views here.
def index(request):
    
    return render(request, 'stores/index.html')


def create(request):
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
    return render(request, 'stores/create.html')