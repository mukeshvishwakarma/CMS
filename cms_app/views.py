from rest_framework import generics, permissions, status
from .models import User, ContentItem
from .serializers import UserSerializer, ContentItemSerializer, ContentItemSearchSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .permissions import IsAuthorOrAdmin
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

# View for creating a new user
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user to create a new account

# View for user login
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            # Validate login data and return token if successful
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle any exceptions during login
            return Response({'error': f'Login failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

# View for listing and creating content items
class ContentItemListCreateView(generics.ListCreateAPIView):
    queryset = ContentItem.objects.all()
    serializer_class = ContentItemSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    def perform_create(self, serializer):
        try:
            # Set the author of the content item to the current user
            serializer.save(author=self.request.user)
        except Exception as e:
            # Handle any exceptions during content creation
            return Response({'error': f'Content creation failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        try:
            # Admin can see all content items, while other users can see only their own
            user = self.request.user
            if user.user_role == 'Admin':
                return ContentItem.objects.all()
            return ContentItem.objects.filter(author=user)
        except Exception as e:
            # Return an empty queryset if an error occurs
            return ContentItem.objects.none()

# View for retrieving, updating, and deleting a specific content item
class ContentItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContentItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdmin]  # Ensure the user is authenticated and has proper permissions

    def get_queryset(self):
        try:
            # Admin can access all content items, while other users can access only their own
            user = self.request.user
            if user.user_role == 'Admin':
                return ContentItem.objects.all()
            return ContentItem.objects.filter(author=user)
        except Exception as e:
            # Return an empty queryset if an error occurs
            return ContentItem.objects.none()

    def get_object(self):
        try:
            # Retrieve the specific content item
            return super().get_object()
        except ObjectDoesNotExist:
            # Handle the case where the content item does not exist
            return Response({'error': 'Content item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle any other exceptions
            return Response({'error': f'Error retrieving content item: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

# Custom view for obtaining JWT tokens
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]  # Allow any user to obtain JWT tokens

# View for searching content items
class ContentItemSearchView(generics.GenericAPIView):
    serializer_class = ContentItemSearchSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request, *args, **kwargs):
        try:
            # Validate the search query
            serializer = self.get_serializer(data=request.query_params)
            serializer.is_valid(raise_exception=True)
            query = serializer.validated_data['query']
            
            # Perform the search across title, body, summary, and categories
            results = ContentItem.objects.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query) |
                Q(summary__icontains=query) |
                Q(categories__icontains=query)
            )

            # Serialize the search results and return them
            results_serializer = ContentItemSerializer(results, many=True)
            return Response(results_serializer.data)
        except Exception as e:
            # Handle any exceptions during the search process
            return Response({'error': f'Search failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
