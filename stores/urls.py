from django.urls import path
from . import views


app_name = 'stores'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:store_pk>/', views.detail, name='detail'),
    path('delete/<int:store_pk>/', views.delete, name='delete'),
    path('update/<int:store_pk>/', views.update, name='update'),
]