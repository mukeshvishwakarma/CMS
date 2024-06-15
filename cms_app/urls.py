from django.urls import path
from .views import UserCreateView, ContentItemListCreateView, ContentItemDetailView, LoginView, ContentItemSearchView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='login'),  # Custom login view
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('contents/', ContentItemListCreateView.as_view(), name='content-list-create'),
    path('contents/<int:pk>/', ContentItemDetailView.as_view(), name='content-detail'),
    path('contents/search/', ContentItemSearchView.as_view(), name='content-search'),
]
