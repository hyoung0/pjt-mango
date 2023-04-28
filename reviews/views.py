from django.shortcuts import render, redirect
from .forms import ReviewForm
from .models import Review, Emote
from stores.models import Store
from django.contrib.auth.decorators import login_required


@login_required
def create(request, store_pk):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.store = Store.objects.get(pk=store_pk)
            review.save()
            return redirect('stores:detail', store_pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
        'store_pk': store_pk,
    }
    return render(request, 'reviews/create.html', context)


@login_required
def update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, request.FILES, instance=review)
            if form.is_valid():
                form.save()
                return redirect('stores:detail', review.store.pk)
        else:
            form = ReviewForm(instance=review)
        context = {
            'form': form,
            'review': review,
        }
        return render(request, 'reviews/update.html', context)
    else:
        return redirect('stores:detail', review.store.pk)


@login_required
def delete(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if review.user == request.user:
        review.delete()
    return redirect('stores:detail', review.store.pk)


EMOTIONS = [
    {'label': '좋아요', 'value': 1},
    {'label': '싫어요', 'value': 2},
]

@login_required
def emotes(request, review_pk, emotion):
    review = Review.objects.get(pk=review_pk)
    my_emotion = Emote.objects.filter(review=review, user=request.user, emotion=emotion)
    if my_emotion.exists():
        my_emotion.delete()
    else:
        Emote.objects.create(review=review, user=request.user, emotion=emotion)
    return redirect('stores:detail', review.store.pk)

# 내가 좋아요/싫어요 버튼을 눌렀다면 안누른 버튼 비활성화
# store detail page로 EMOTIONS 옮기고 context 담아서 출력