from django.urls import path
from . import views

urlpatterns = [

    path('create_user/', views.CreateUser, name="create-user"),
    path('update_user/<str:pk>/', views.updateUser, name="update-user"),
    path('delete_user/<str:pk>/', views.deleteUser, name="delete-user"),
    path('user_search/', views.user_search),
    path('users_based_on_tag/', views.users_based_on_tag, name="users_based_on_tag-user"),
    path('create_discussion/', views.CreateDiscussion, name="create-discussion"),
    path('update_discussion/<str:pk>/', views.updateDiscussion, name="update-discussion"),
    path('discussion_search/', views.discussion_search),
    path('delete_discussion/<str:pk>/', views.deleteUser, name="delete-discussion"),
    path('discussion_based_on_tags/<str:pk>/', views.discussion_based_on_tags, name="tags-discussion")
]