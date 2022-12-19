from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.StoryView.as_view(), name="story"),
    path('<int:pk>/edit/', views.StoryEditView.as_view(), name="storyEdit"),
    path('<int:pk>/delete/', views.StoryDeleteView.as_view(), name="storyDelete"),
    path('<int:pk>/like/', views.like, name="like"),
    path('add-story/', views.AddStoryView.as_view(), name='newStory'),
]
