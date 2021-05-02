from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from django.contrib.auth.models import User
from .models import Menu,Order,OrderItem
from .serializer import  MenuSerializer, OrderSerializer, UserSerializer, UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status
 

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes =[
        '/api/',
        '/api/menu/',
        '/api/dish/<id>',
        'api/users/profile/',
        'api/users/login',
        'api/users/registeruser/',
        'api/add/order/',
        'api/orders/',
        'api/myorders/',
        'api/order/<str:pk>/',
        'api/order/<str:pk>/pay/',
    ]
    return Response(routes)

@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user= request.user
    serializer = UserSerializer(user , many=False)
    return  Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getMenu(request):
    menu= Menu.objects.all()
    serializer = MenuSerializer(menu , many=True)
    return  Response(serializer.data)

@api_view(['GET'])
def getDish(request, id):
    dish = Menu.objects.get(_id = id)
    serializer = MenuSerializer(dish , many=False)
    return  Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderitem(request):
    user= request.user
    data = request.data
    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0 :
        return Response({'Detail':'NO order items'},status=status.HTTP_400_BAD_REQUEST)
    else : 
        # create order
        order = Order.objects.create(
           user= user,
           paymentMethod=data['paymentMethod'],
           taxPrice=data['taxPrice'],
           totalPrice=data['totalPrice'], 
        )

        # create orderItem
        for i in orderItems:
            dish = Menu.objects.get(_id=i['dish'])

            item = OrderItem.objects.create(
                menu=dish,
                order=order,
                name=dish.dish_name,
                qty=i['qty'],
                price=i['price'],
                image=dish.image.url,
            )

            dish.counterInStock -= item.qty
            dish.save()
    
    serializer = OrderSerializer(order , many=False)
    return  Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):

    user = request.user

    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Not authorized to view this order'},
                     status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    order = Order.objects.get(_id=pk)

    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()

    return Response('Order was paid')

