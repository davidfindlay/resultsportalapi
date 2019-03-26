from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.MeetListView.as_view()),
    path(r'<int:meet_id>/', views.MeetResultsView.as_view()),
]
