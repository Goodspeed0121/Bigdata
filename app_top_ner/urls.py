from django.urls import path
from app_top_ner import views

app_name="app_top_ner"

urlpatterns = [
    path('', views.home, name='home'),
    path('api_get_cat_topkey/', views.api_get_cat_topkey, name='api_cat_topkey'),
]
