from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.group_list, name='group_list'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('resolve_doubt/<int:doubt_id>/', views.resolve_doubt, name='resolve_doubt'),
    path('user-type/', views.user_type_view, name='user_type'),
    
]
