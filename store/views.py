from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .models import Product, Order, OrderItem, CheckoutLog
from .serializers import (
    ProductSerializer, OrderSerializer, OrderItemSerializer,
    CheckoutLogSerializer
)
from rest_framework.serializers import ModelSerializer

# 🔐 User Registration
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# 🛍️ Product Management (CRUD)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if OrderItem.objects.filter(product=product).exists():
            return Response(
                {'error': 'Cannot delete product that has already been ordered.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)



# 📦 Customer Order Handling
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()  
    serializer_class = OrderSerializer

class OrderItemCreateView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def perform_create(self, serializer):
        order_item = serializer.save()

        product = order_item.product
        if product.stock < order_item.quantity:
            raise serializers.ValidationError("Not enough stock available.")
        product.stock -= order_item.quantity
        product.save()

        # ✅ Create CheckoutLog (log each individual item checkout OR one per order — adjust as needed)
        CheckoutLog.objects.create(
            employee=self.request.user,
            order=order_item.order
        )



# 👨‍💼 Checkout Monitoring
class CheckoutLogListView(generics.ListAPIView):
    queryset = CheckoutLog.objects.all()
    serializer_class = CheckoutLogSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date_checked']

class CheckoutLogCreateView(generics.CreateAPIView):
    queryset = CheckoutLog.objects.all()
    serializer_class = CheckoutLogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'is_staff': request.user.is_staff
    })