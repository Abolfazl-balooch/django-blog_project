from django.urls import path
from . import views

urlpatterns = [
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('entries/', views.ArticleListView.as_view(), name='post_entries'),

    path('details/<int:pk>', views.category_detail, name='categories'),

    path('search/', views.search, name='search'),

    path('contactUs', views.ContctUsView.as_view(), name='contact_us'),

    path('list/', views.HomePageRedirectView.as_view(), name='list2'),

    path('article/creat', views.ArticleCreateView.as_view(), name='create_article'),

    path('post/<slug:slug>/like/', views.LikeView.as_view(), name='post_like'),
    path('list/myarticles', views.ArticlePrivateListView.as_view(), name='my_articles'),

    path('update/<slug:slug>/', views.ArticleUpdateView.as_view(), name='update_article'),

    path('delete/<slug:slug>/', views.ArticleDeleteView.as_view(), name='delete_article'),

]
