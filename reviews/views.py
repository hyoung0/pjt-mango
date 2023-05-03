from django.shortcuts import render, redirect
from .forms import ReviewForm, ReviewImageForm
from .models import Review, ReviewImage, Emote
from stores.models import Store
from django.contrib.auth.decorators import login_required


@login_required
def create(request, store_pk):
    store = Store.objects.get(pk=store_pk)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        review_image_form = ReviewImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if review_form.is_valid() and review_image_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.store = Store.objects.get(pk=store_pk)
            review.save()
            
            for file in files:
                ReviewImage.objects.create(review=review, image=file)

            return redirect('stores:detail', store_pk)
    else:
        review_form = ReviewForm()
        review_image_form = ReviewImageForm()
    context = {
        'review_form': review_form,
        'review_image_form': review_image_form,
        'store': store,
    }
    return render(request, 'reviews/create.html', context)


@login_required
def update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST, instance=review)
            review_image_form = ReviewImageForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid() and review_image_form.is_valid():
                review_form.save()
                return redirect('stores:detail', review.store.pk)
        else:
            review_form = ReviewForm(instance=review)
            review_image_form = ReviewImageForm(instance=review)
        context = {
            'review_form': review_form,
            'review_image_form': review_image_form,
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


@login_required
def emotes(request, review_pk, emotion):
    review = Review.objects.get(pk=review_pk)
    my_emote = Emote.objects.filter(review=review, user=request.user)
    input_emote = Emote.objects.filter(review=review, user=request.user, emotion=emotion)

    # 기존에 좋아요/싫어요 버튼을 누른 경우 지금 누른 버튼이라면 삭제, 다른 버튼이라면 동작하지 않도록!
    if my_emote.exists():
        if input_emote.exists():
            my_emote.delete()
    else:
        Emote.objects.create(review=review, user=request.user, emotion=emotion)
    return redirect('stores:detail', review.store.pk)