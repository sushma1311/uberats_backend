# backend/api/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomerSerializer,DishSerializer,RestaurantSerializer, CartSerializer,OrderSerializer , AddressSerializer
from api.serializers import RestaurantSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Customer,Restaurant,Dish,Cart,Order,Favorite, Address
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

class CustomerSignupView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RestaurantSignupView(APIView):
    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#from rest_framework_simplejwt.tokens import RefreshToken  # Optional for JWT

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            # If you use JWT
            refresh = RefreshToken.for_user(user)
            if hasattr(user, 'customer'):
                user_type = 'customer'
            elif hasattr(user, 'restaurant'):
                user_type = 'restaurant'
            else:
                user_type = 'unknown'
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful',
                'user_type': user_type,
                
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

class CustomerProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # To handle file uploads like profile picture

    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request):
        customer = get_object_or_404(Customer, user=request.user)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class RestaurantProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request):
        # Fetch restaurant profile
        restaurant = Restaurant.objects.get(user=request.user)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)

    def put(self, request):
        # Update restaurant profile
        restaurant = get_object_or_404(Restaurant, user=request.user)
        serializer = RestaurantSerializer(restaurant, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CountryListView(APIView):
    def get(self, request):
        countries = ["United States", "Canada", "United Kingdom", "Australia", 'France', 'India', 'China', 'Brazil', 'Japan', 'South Korea']  # Add your list here
        return Response(countries)
    

class RestaurantListView(APIView):
    def get(self, request):
        # Fetch all restaurants from the database
        restaurants = Restaurant.objects.all()
        # Serialize the data
        serializer = RestaurantSerializer(restaurants, many=True)
        # Return the serialized data
        return Response(serializer.data)
    
class RestaurantDetailView(APIView):
    def get(self, request, id):
        try:
            # Get the restaurant by its ID
            restaurant = Restaurant.objects.get(id=id)
            # Serialize the restaurant details
            restaurant_serializer = RestaurantSerializer(restaurant)

            # Fetch the dishes associated with the restaurant
            menu = Dish.objects.filter(restaurant=restaurant)

            if not menu.exists():
                return Response({
                    "restaurant": restaurant_serializer.data,
                    "menu": [],  # Empty menu
                    "message": "No menu available for this restaurant."
                }, status=status.HTTP_200_OK)

            # Serialize the menu
            menu_serializer = DishSerializer(menu, many=True)

            # Combine both the restaurant details and the menu in the response
            return Response({
                "restaurant": restaurant_serializer.data,  # Restaurant details
                "menu": menu_serializer.data               # Menu (dishes)
            }, status=status.HTTP_200_OK)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        
class AddDishView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        restaurant = Restaurant.objects.get(user=request.user)  # Get restaurant for logged-in user
        data = request.data
        data['restaurant'] = restaurant.id  # Assign restaurant ID to the dish
        serializer = DishSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditDishView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, dish_id):
        dish = get_object_or_404(Dish, id=dish_id, restaurant__user=request.user)  # Ensure the dish belongs to the restaurant
        serializer = DishSerializer(dish, data=request.data, partial=True)  # Allow partial updates

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CartView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         cart_items = Cart.objects.filter(user=user)

#         # If the cart is empty, return a relevant message
#         if not cart_items.exists():
#             return Response({"message": "Your cart is empty."}, status=status.HTTP_200_OK)

#         # Prepare the response data without using a serializer
#         cart_data = []
#         total_price = 0

#         for item in cart_items:
#             cart_data.append({
#                 'id': item.id,
#                 'dish_name': item.dish.name,  # Assuming the Cart model has a foreign key to Dish
#                 'quantity': item.quantity,
#                 'price': item.dish.price,  # Assuming the Dish model has a 'price' field
#             })
#             total_price += item.dish.price * item.quantity

#         # Return the cart items and total price
#         return Response({
#             'items': cart_data,
#             'total_price': round(total_price, 2)
#         }, status=status.HTTP_200_OK)

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        print(cart_items) 

        if not cart_items.exists():
            return Response({"message": "Your cart is empty."}, status=status.HTTP_200_OK)

        # Use the CartSerializer to serialize the cart items
        serializer = CartSerializer(cart_items, many=True)
        total_price = sum(item.dish.price * item.quantity for item in cart_items)

        return Response({
            'items': serializer.data,  # This will include restaurant_name
            'total_price': round(total_price, 2)
        }, status=status.HTTP_200_OK)


class AddToCartView(APIView):
    def post(self, request):
        # Assuming the request data contains dish_id and quantity
        dish_id = request.data.get('dish_id')
        user = request.user
        #quantity = request.data.get('quantity', 1)  # Default to 1 if not provided

        try:
            # Get the dish by its ID
            dish = Dish.objects.get(id=dish_id)
            
            cart_item, created = Cart.objects.get_or_create(user=user, dish=dish)
            if created:
                print(f"New cart item created for dish: {dish.name}")
            else:
                print(f"Existing cart item updated for dish: {dish.name}")

            if not created:
                cart_item.quantity += 1  # Increment quantity if dish is already in the cart
                cart_item.save()
            return Response({"message": "Dish added to cart"}, status=status.HTTP_201_CREATED)
        except Dish.DoesNotExist:
            return Response({"error": "Dish not found"}, status=404)
        



# class FinalizeOrderView(APIView):
#     def post(self, request):
#         user = request.user
#         cart_items = Cart.objects.filter(user=user)
        
#         print(request.data.get('checkout_items'))


#         if not cart_items.exists():
#             return Response({"error": "No items in cart"}, status=400)
        
#         total_price = sum(item.dish.price * item.quantity for item in cart_items)

#         # Get delivery address from the request
#         address_id = request.data.get('address_id')
#         new_address_data = request.data.get('new_address')
#         ordered_items = request.data.get('checkout_items')
        

#         if address_id:
#             try:
#                 delivery_address = Address.objects.get(id=address_id, user=user)
#             except Address.DoesNotExist:
#                 return Response({"error": "Address not found"}, status=404)
#         elif new_address_data:
#             delivery_address = Address.objects.create(user=user, **new_address_data)
#         else:
#             return Response({"error": "No delivery address provided"}, status=400)

#         # Ensure all items are from the same restaurant
#         first_restaurant = cart_items.first().dish.restaurant
#         if not all(item.dish.restaurant == first_restaurant for item in cart_items):
#             return Response({"error": "You cannot order from multiple restaurants at once."}, status=400)

#         # Create the order
#         order = Order.objects.create(
#             user=user,
#             total_price=total_price,
#             delivery_address=delivery_address,
#             restaurant=first_restaurant,
#             items=ordered_items,
#             order_status='New'
#         )

#         order.save()
       

#         # Clear the cart after the order is finalized
#         cart_items.delete()

#         return Response({"message": "Order finalized", "total_price": total_price}, status=status.HTTP_201_CREATED)
class FinalizeOrderView(APIView):
    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"error": "No items in cart"}, status=400)
        
        total_price = sum(item.dish.price * item.quantity for item in cart_items)

        # Get delivery option from the request (default to 'delivery' if not provided)
        delivery_option = request.data.get('delivery_type', 'delivery')

        # Get delivery address or allow address to be null for pickup
        address_id = request.data.get('address_id') if delivery_option == 'delivery' else None
        new_address_data = request.data.get('new_address') if delivery_option == 'delivery' else None
        ordered_items = request.data.get('checkout_items')

        if delivery_option == 'delivery':
            if address_id:
                try:
                    delivery_address = Address.objects.get(id=address_id, user=user)
                except Address.DoesNotExist:
                    return Response({"error": "Address not found"}, status=404)
            elif new_address_data:
                delivery_address = Address.objects.create(user=user, **new_address_data)
            else:
                return Response({"error": "No delivery address provided"}, status=400)
        else:
            # Set delivery_address to None for pickup orders
            delivery_address = None

        # Ensure all items are from the same restaurant
        first_restaurant = cart_items.first().dish.restaurant
        if not all(item.dish.restaurant == first_restaurant for item in cart_items):
            return Response({"error": "You cannot order from multiple restaurants at once."}, status=400)

        # Create the order
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            delivery_address=delivery_address,
            restaurant=first_restaurant,
            items=ordered_items,
            order_status='New',
            delivery_option=delivery_option,  # Store the delivery option (pickup or delivery)
            order_delivery_status = 'order received'
        )

        order.save()

        # Clear the cart after the order is finalized
        cart_items.delete()

        return Response({"message": "Order finalized", "total_price": total_price}, status=status.HTTP_201_CREATED)

    

class OrdersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user).order_by('-created_at')  # Fetch user's orders
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RestaurantOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get the restaurant for the logged-in user
            restaurant = Restaurant.objects.get(user=request.user)
            
            # Get status filter from request
            status_filter = request.query_params.get('status')
            
            # Fetch the orders for this restaurant
            orders = Order.objects.filter(restaurant=restaurant)

            # Filter by order status if a filter is applied
            if status_filter:
                orders = orders.filter(order_status=status_filter)

            # Serialize the orders
            serializer = OrderSerializer(orders, many=True)

            # Return the serialized data with HTTP 200 OK status
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            new_status = request.data.get('order_status')
            order_delivery_status = request.data.get('delivery_status')
            
            # if new_status not in dict(Order.STATUS_CHOICES).keys():
            #     return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

            order.order_delivery_status=order_delivery_status
            order.order_status = new_status
            order.save()
            return Response({"message": "Order status updated successfully"}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


    

class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        try:
            cart_item = Cart.objects.get(id=item_id, user=request.user)
            cart_item.delete()
            return Response({"message": "Item removed from cart"}, status=200)
        except Cart.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=404)
        
class CartUpdateView(APIView):
    permission_classes = [IsAuthenticated]


    def put(self, request, item_id):
        try:
            cart_item = Cart.objects.get(id=item_id, user=request.user)
            new_quantity = request.data.get('quantity')


            if new_quantity is not None and int(new_quantity) > 0:
                cart_item.quantity = new_quantity
                cart_item.save()
                return Response({"message": "Quantity updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

    
#-----------------##---------------###-----------------####--------------#####--------------######-------------#######----------------########

class AddFavoriteView(APIView):
    def post(self, request):
        user = request.user
        restaurant_id = request.data.get('restaurant_id')

        # Check what's being received in request.data
        print("Received data:", request.data)

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            if Favorite.objects.filter(user=user, restaurant=restaurant).exists():
                return Response({"message": "Restaurant is already marked as favorite"}, status=400)

            favorite, created = Favorite.objects.get_or_create(user=user, restaurant=restaurant)
            return Response({"message": "Restaurant added to favorites!"}, status=status.HTTP_200_OK)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

        


class RemoveFavoriteView(APIView):
    def post(self, request):
        user = request.user
        restaurant_id = request.data.get('restaurant_id')
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            favorite = Favorite.objects.get(user=user, restaurant=restaurant)
            favorite.delete()
            return Response({"message": "Restaurant removed from favorites!"}, status=status.HTTP_200_OK)
        except (Restaurant.DoesNotExist, Favorite.DoesNotExist):
            return Response({"error": "Restaurant not found in favorites"}, status=status.HTTP_404_NOT_FOUND)
        



class FavoriteListView(APIView):
    def get(self, request):
        user = request.user
        favorites = Favorite.objects.filter(user=user)
        serializer = RestaurantSerializer([fav.restaurant for fav in favorites], many=True)
        return Response(serializer.data)  
   


class AddressListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def put(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)