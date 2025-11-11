from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.dashboard_view, name='dashboard'),
    # path('announcement/', views.ann_home, name='ann_home'),
    # urls.py
    # path('event_interest/<int:ann_id>/', views.event_interest, name='event_interest'),
    path('announcements/', views.announcements, name='announcements'),
    path('event_interest/<int:ann_id>/', views.event_interest, name='event_interest'),
    path('export-event-interests/', views.export_event_interests, name='export_event_interests'),


    path('home/', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    path('generate-flashcard/<int:message_id>/', views.generate_flashcard, name='generate-flashcard'),
    # in urls.py
    path('message/<int:message_id>/add_hashtag/', views.add_hashtag, name='add-hashtag'),

    path('message/edit-hashtags/<int:pk>/', views.edit_message_hashtags, name='edit_message_hashtags'),



]
