from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login , name='login'),

    path('register', views.register , name='register'),

    path('logout', views.user_logout , name='logout'),

    path('profile/edit', views.profile_edit , name='edit_profile'),

    path('profile/<str:username>', views.UserProfileView.as_view() , name='show_profile'),

]