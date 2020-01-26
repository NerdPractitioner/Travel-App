# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    # path('index', views.index, name='index'),
    path('', views.index, name='index'),
    path('contact_add/<str:user_id>', views.add_contact, name='add_contact'),
    path('contact_remove/<str:user_id>', views.remove_contact, name='remove_contact'),
    # path('<str:room_name>/', views.room, name='room',)
    path('with_contact/<int:user_id>/', views.start_one_to_one_chat, name='start_react_one_to_one_chat',),
    path('<int:chat_id>/', views.react_chat, name='react_chat',),
    path('<str:chat_id>/', views.react_chat, name='react_chat',),
    # path('', views.react_chat, name='room_default',),
]