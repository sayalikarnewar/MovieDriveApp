# movies/views.py

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .models import Collection
from .serializers import UserSerializer, MovieSerializer, CollectionSerializer
import requests
from collections import Counter

# 1. Register User
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

# 2. Login User - Obtain JWT Token
class LoginView(TokenObtainPairView):
    pass

# 3. Get Movies List (from third-party API)
class MovieListView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = request.query_params.get('page', 1)
        response = requests.get(f'https://demo.credy.in/api/v1/maya/movies/?page={page}', verify=False)
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response({'error': 'Failed to fetch movies'}, status=status.HTTP_400_BAD_REQUEST)

# 4. Get Collection List and Top 3 Favorite Genres
class CollectionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CollectionSerializer

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        collections = self.get_queryset()
        serializer = self.get_serializer(collections, many=True)

        genres = []
        for collection in collections:
            for movie in collection.movies.all():
                genres.extend(movie.genres.split(','))

        top_genres = [genre for genre, _ in Counter(genres).most_common(3)]

        return Response({
            "is_success": True,
            "data": {
                "collections": serializer.data,
                "favourite_genres": ", ".join(top_genres)
            }
        }, status=status.HTTP_200_OK)

# 5. Create Collection
class CollectionDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    lookup_field = 'uuid'

class CollectionCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CollectionUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    lookup_field = 'uuid'

# 8. Delete Collection by ID
class CollectionDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Collection.objects.all()
    lookup_field = 'uuid'
