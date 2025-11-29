from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('load_route/<int:route_id>/', views.load_route, name='load_route'),
    path('delete_route/<int:route_id>/', views.delete_route, name='delete_route'),
]