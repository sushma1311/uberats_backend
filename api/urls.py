#backend/api/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomerSignupView, RestaurantSignupView,LoginView,CountryListView,CustomerProfileView,RestaurantListView, RestaurantDetailView, AddToCartView, CartUpdateView, FinalizeOrderView,AddFavoriteView,RemoveFavoriteView,FavoriteListView,RemoveFromCartView,CartView, RestaurantProfileView, AddDishView, EditDishView, AddressListView, AddressDetailView, OrdersListView, RestaurantOrdersView,UpdateOrderStatusView, ClearCartView
  # Import your view classes

urlpatterns = [
    path('customer-signup/', CustomerSignupView.as_view(), name='customer-signup'),
    path('restaurant-signup/', RestaurantSignupView.as_view(), name='restaurant-signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', CustomerProfileView.as_view(), name='customer-profile'),
    path('restaurant-profile/', RestaurantProfileView.as_view(), name='restaurant-profile'),
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<int:id>/menu/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/finalize/', FinalizeOrderView.as_view(), name='finalize-order'),
    path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/update/<int:item_id>/', CartUpdateView.as_view(), name='update-cart'),
    path('cart/clear/', ClearCartView.as_view(), name='clear-cart'),

    
    path('favorites/add/', AddFavoriteView.as_view(), name='add-favorite'),
    path('favorites/remove/', RemoveFavoriteView.as_view(), name='remove-favorite'),
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),

    path('dishes/add/', AddDishView.as_view(), name='add-dish'),  # Endpoint to add a dish
    path('dishes/<int:dish_id>/edit/', EditDishView.as_view(), name='edit-dish'),  # Endpoint to edit a dish

    path('addresses/', AddressListView.as_view(), name='address-list'),  # List and create addresses
    path('addresses/<int:pk>/', AddressDetailView.as_view(), name='address-detail'),  # Retrieve, update, delete a specific address

    path('orders/', OrdersListView.as_view(), name='orders-list'),
    path('restaurant/orders/', RestaurantOrdersView.as_view(), name='restaurant-orders-list'),
    path('restaurant/orders/<int:order_id>/status/', UpdateOrderStatusView.as_view(), name='update-order-status'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
  
