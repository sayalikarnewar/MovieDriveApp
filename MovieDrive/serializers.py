# movies/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie, Collection

# User Serializer for registration
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

# Movie Serializer
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'uuid']

class MovieUUIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "uuid",
        ]
class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)
    class Meta:
        model = Collection
        fields = [
            "title",
            "description",
            "movies",
            "uuid",
        ]
    
    def create(self, validated_data):
        movies_data = validated_data.pop('movies', [])
        collection = Collection.objects.create(**validated_data)
        print(f"Created collection: {collection.title} with UUID: {collection.uuid}")

        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(uuid=movie_data['uuid'], defaults=movie_data)
            collection.movies.add(movie)

        return collection

    def update(self, instance, validated_data):
        movies_data = validated_data.pop('movies', None)
        if movies_data is not None:
            instance.movies.clear()  # Remove existing movies
            for movie_data in movies_data:
                movie, created = Movie.objects.get_or_create(uuid=movie_data['uuid'], defaults=movie_data)
                instance.movies.add(movie)
        
        # Update title and description if provided
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance