from django.urls import path
from . import views

urlpatterns = [

    path('', views.home , name='home'),
    path('room/<str:pk>' , views.room , name='room'),
    path('createroom/' , views.create_room , name='createroom' ),
    path('updateroom/<str:pk>' , views.update_room , name='updateroom' ),
    path('deleteroom/<str:pk>' , views.delete_room , name='deleteroom'),
    path('login/' ,views.loginpage , name='login'),
    path('logout/',views.logoutview , name='logout' ),
    path('register/',views.registerpage , name='register' ),
    path('deletemsg/<str:pk>',views.delete_msg , name='deletemsg' ),
    path('roomcode/<str:pk>',views.roomcode , name='roomcode' ),
    path('profile/<str:pk>',views.profilepage , name='profile' ),
    path('browsetopics/',views.browsetopics , name='browsetopics' ),
    path('activity/',views.activity , name='activity' ),
    path('useractivity/<str:pk>',views.useractivity , name='useractivity' ),
]