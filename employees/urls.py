from django.urls import path
from .views import home
from .views import upload_csv

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_csv, name='upload')
]