from django.urls import path
from . import views


app_name = 'stores'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:store_pk>/', views.detail, name='detail'),
    path('<int:store_pk>/delete/', views.delete, name='delete'),
    path('<int:store_pk>/update/', views.update, name='update'),
    path('search/', views.search, name='search'),
    path('<int:store_pk>/like-stores/', views.like_stores, name='like_stores'),
    path('category/<str:subject>/', views.category, name='category'),
    path('all/', views.all_stores, name='all_stores'),
    path('<int:store_pk>/menu/create/', views.menu_create, name='menu_create'),
    path('<int:store_pk>/menu/<int:menu_pk>/delete/', views.menu_delete, name='menu_delete'),
]
]