from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio_home, name='portfolio_home'),  # Your portfolio page
    path('api/projects/', views.project_list_create, name='project_api'),  # API endpoint
]
