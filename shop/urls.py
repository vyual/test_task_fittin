from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from shop.views import CartItemViewSet, CategoryViewSet, MyTokenObtainPairView, OrderViewSet, ProductViewSet

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


router = routers.DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r'cart', CartItemViewSet, basename='cart')

router.register(r"orders", OrderViewSet)


urlpatterns = [
    path("", include(router.urls)),

    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
