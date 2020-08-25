from django.urls import path
from api import views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('ious/', views.IOUList.as_view()),
    path('ious/<int:pk>/', views.IOUDetail.as_view()),
]