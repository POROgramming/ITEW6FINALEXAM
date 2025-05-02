from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderListCreateView, OrderItemCreateView, CheckoutLogListView, RegisterView, CheckoutLogCreateView
from .views import user_info
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register('products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', OrderListCreateView.as_view()),
    path('order-items/', OrderItemCreateView.as_view()),
    path('checkout-logs/create/', CheckoutLogCreateView.as_view()),
    path('checkout-logs/', CheckoutLogListView.as_view()),
    path('register/', RegisterView.as_view()),
    path('user/', user_info),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
