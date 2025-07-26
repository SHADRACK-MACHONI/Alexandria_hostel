from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('rooms/', views.rooms_view, name='rooms'),
    path('book-room/', views.book_room, name='book_room'),
    path('payments/', views.payments_view, name='payments'),  # define this
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('resources/', views.resource_list, name = 'resources'),
    path('chat/', views.chat_view, name='chat'),  # Add this
    path('entertainment/', views.entertainment_view, name = 'entertainment'),
    path('book-room/<int:room_id>/',views.book_room_view, name='book_room'),
    path('booking/success/',views.booking_success,name='booking_success'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'),name='login_redirect'),
]


