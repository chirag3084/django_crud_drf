from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import include
from . import views as user_views

urlpatterns = [
    path('register/', user_views.register, name='register-page'),
    path('login/', auth_views.LoginView.as_view(template_name = "users/login.html"), name='login-page'),
    path('logout/', user_views.logout_user, name='logout'),
    path('profile/<int:pk>/', include([
        path('', user_views.ProfileDetailsView.as_view(), name='profile-page'),
        path('edit/', user_views.ProfileEditView.as_view(), name='profile-edit'),
        path('delete/', user_views.ProfileDeleteView.as_view(), name='profile-delete'),
    ])),
]
