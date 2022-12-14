from django.urls import path

from .views import (AboutView, BlogView, 
                    ContactView, AuthorView, 
                    HomeView, CreatePostView, 
                    DetailPostView, DetailCityView,
                    CreateTaskView, DelTaskView
                    )

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('detail/<int:pk>', DetailPostView.as_view(), name='detail_post'),
    path('create/post/', CreatePostView.as_view(), name='create-post'),
    path('create/account/', CreatePostView.as_view(), name='create-account'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('user/<username>', AuthorView.as_view(), name='user'),
    path('city/<slug:slug>', DetailCityView.as_view(), name='detail_city'),
    path('createtask/', CreateTaskView.as_view(), name='create_task'),
    path('deltask/', DelTaskView.as_view(), name='del_task'),
    
    # path('registration/', RegistrationView.as_view(), name='registration'),
]
