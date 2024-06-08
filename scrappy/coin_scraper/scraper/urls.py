from django.urls import path
from .views import StartScrapingView,ScrapingStatusView


urlpatterns = [
    path('taskmanager/start_scraping',StartScrapingView.as_view(),name='start_scraping'),
    path('taskmanager/scraping_status/<str:job_id>',ScrapingStatusView.as_view(),name='scrping_status')
]