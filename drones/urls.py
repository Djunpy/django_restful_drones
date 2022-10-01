from django.urls import path

from . import views

urlpatterns = [
    path('', views.ApiRoot.as_view()),
    path('drone-categories/', views.DroneCategoryList.as_view(), name='dronecategory-list'),
    path('drones/', views.DroneList.as_view(), name='drone-list'),
    path('competitions/', views.CompetitionList.as_view(), name='competition-list'),
    path('pilots/', views.PilotList.as_view(), name = 'pilot-list'),
    path('drone-category/<int:pk>/', views.DroneCategoryDetail.as_view(), name='dronecategory-detail'),
    path('drone/<int:pk>/', views.DroneDetail.as_view(), name='drone-detail'),
    path('pilot/<int:pk>/', views.PilotDetail.as_view(), name='pilot-detail'),
    path('competition/<int:pk>/', views.CompetitionDetail.as_view(), name='competition-detail'),
]
