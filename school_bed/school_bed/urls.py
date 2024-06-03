from django.urls import path
 
from . import views
 
urlpatterns = [
    path("hello/", views.hello),
    path("runoob/", views.runoob),
    path("submit_data/", views.submit_data),
    path("main/", views.view_main),
]