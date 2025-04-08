from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='quora/login.html'), name='login'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('ask/', views.ask_question, name='ask'),
    path('question/<int:question_id>/', views.view_question, name='view_question'),
    path('like/<int:answer_id>/', views.like_answer, name='like_answer'),
]

