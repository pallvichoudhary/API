from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer,ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .serializers import OrderItemCreateSerializer, OrderSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from api.filters import ProductFilter,InStockFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from api.filters import OrderFilter
from rest_framework.decorators import action







class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class=ProductFilter
    filter_backends =[DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,InStockFilterBackend]

    pagination_class=PageNumberPagination
    pagination_class.page_size=2
    pagination_class.page_size_query_param='size'
    pagination_class.page_query_param="pageNum"
    pagination_class.max_page_size=10
    
    search_fields=['=name','description']
    ordering_fields=['name','price','stock']


    def get_permissions(self):
        self.permission_classes=[AllowAny]
        if self.request.method == 'POST':
            self.permission_classes=[IsAdminUser]
        return super().get_permissions()





# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)




class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg='product_id'

    def get_permissions(self):
        self.permission_classes =[AllowAny]
        if self.request.method in ['PUT','PATCH','DELETE']:
            self.permission_classes=[IsAdminUser]
        return super().get_permissions()

# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)\



class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset=Order.objects.prefetch_related('items__product')
    serializer_class=OrderSerializer
    Permission_classes=[IsAuthenticated]
    pagination_class=None
    filterset_class=OrderFilter
    filter_backends=[DjangoFilterBackend]

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderItemCreateSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        qs= super().get_queryset()
        if not self.request.user.is_staff:
            qs=qs.filter(user = self.request.user)
        
      


    @action(
        detail=False,
        methods=['get'],
        url_path='user-objects',
    )


    def user_orders(self,request):
        orders=self.get_queryset().filter(user=request.user)
        serializer= self.get_serializer(orders,many=True)
        return Response(serializer.data)





class ProductCreateAPIView(generics.CreateAPIView):
    model=Product
    serializer_class=ProductSerializer

# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related('items__product')
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

class UserOrderListAPIView(generics.ListAPIView):
    queryset=Order.objects.prefetch_related('items__product')
    serializer_class=OrderSerializer
    permission_classes = [IsAuthenticated]



    def get_queryset(self):
       user=self.request.user
       qs=super().get_queryset()
       return qs.filter(user=user)





class ProductInfoAPIView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        count= products.count() # type: ignore
        max_price= products.aggregate(max_price=Max('price'))['max_price'] # type: ignore
     
        data={
         'products':products,
          'count':count,
          'max_price': max_price
        }
        serializer = ProductInfoSerializer(data)
        return Response(serializer.data)




@api_view(['GET'])
def product_info(request):
    products=Product.objects.all()
    serializer=ProductInfoSerializer({
        'products':products,
        'count':len(products),
        'max_price':products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)
