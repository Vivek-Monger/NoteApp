from django.urls import path, include
from django.contrib.auth.views import LogoutView
<<<<<<< HEAD
from rest_framework_simplejwt.views import TokenRefreshView
=======
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
>>>>>>> master
from . import views
from . import api_views
from . import api_auth_views

urlpatterns = [
    # Web interface URLs
    path('', views.NoteListView.as_view(), name='note_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('note/create/', views.NoteCreateView.as_view(), name='note_create'),
    path('note/<int:pk>/edit/', views.NoteUpdateView.as_view(), name='note_update'),
    path('note/<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),
    
    # JWT API URLs
    path('api/register/', api_auth_views.api_register, name='api_register'),
    path('api/login/', api_auth_views.api_login, name='api_login'),
    path('api/logout/', api_auth_views.api_logout, name='api_logout'),
<<<<<<< HEAD
=======
    path('api/token/', TokenObtainPairView.as_view(), name='api_token_obtain_pair'),
>>>>>>> master
    path('api/token/refresh/', api_auth_views.api_refresh_token, name='api_token_refresh'),
    
    # DRF API URLs
    path('api/v1/', include([
        path('register/', api_views.register_view, name='drf_register'),
        path('login/', api_views.CustomTokenObtainPairView.as_view(), name='drf_login'),
        path('logout/', api_views.logout_view, name='drf_logout'),
        path('profile/', api_views.user_profile, name='drf_profile'),
        path('notes/', api_views.note_list_create, name='drf_note_list'),
        path('notes/<int:pk>/', api_views.note_detail, name='drf_note_detail'),
    ])),
]
