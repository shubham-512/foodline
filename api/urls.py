from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.getRoutes, name="home"),
    path('api/menu/', views.getMenu, name="menu"),
    path('api/users/profile/', views.getUserProfile, name="user-profile"),
    path('api/users/profile/update/', views.updateUserProfile, name="user-profile-update"),
    path('api/dish/<str:id>/', views.getDish, name="dish"),
    path('api/dish/category/<str:category>/', views.getDishCategory, name="dish-category"),
    path('api/users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/users/registeruser/', views.registerUser, name="register-user"),
    path('api/users/', views.getUsers, name="user-profile"),
    path('api/add/order/', views.addOrderitem, name="add-order"),
    path('api/orders/', views.getOrders, name='orders'),
    path('api/myorders/', views.getMyOrders, name='myorders'),
    path('api/order/<str:pk>/', views.getOrderById, name='user-order'),
    path('api/order/<str:pk>/pay/', views.updateOrderToPaid, name='pay'),
    
    
]