from django.urls import path
from . import views

urlpatterns = [
    path('crud/',views.PostCrudView.as_view(),name='user_post_curd'),
    path('lastest/',views.LastFiftyPost.as_view(),name='last_fifty_post'),
]