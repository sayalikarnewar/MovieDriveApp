# movies/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie, Collection, MovieCollection

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

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'uuid']

class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ['uuid', 'title', 'description', 'movies']

    def create(self, validated_data):
        movies_data = validated_data.pop('movies')
        collection = Collection.objects.create(**validated_data)

        # Handle movies
        for movie_data in movies_data:
            # Check if 'uuid' is in movie_data
            if 'uuid' not in movie_data:
                raise serializers.ValidationError("Each movie must have a UUID.")
            
            movie_uuid = movie_data['uuid']
            movie, created = Movie.objects.get_or_create(
                uuid=movie_uuid,
                defaults={
                    'title': movie_data.get('title', ''),
                    'description': movie_data.get('description', ''),
                    'genres': movie_data.get('genres', '')
                }
            )
            MovieCollection.objects.create(collection=collection, movie=movie)
        
        return collection

    def update(self, instance, validated_data):
        movies_data = validated_data.pop('movies', [])
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Clear existing MovieCollection instances
        MovieCollection.objects.filter(collection=instance).delete()

        # Create new MovieCollection instances
        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(
                uuid=movie_data['uuid'],
                defaults={
                    'title': movie_data['title'],
                    'description': movie_data['description'],
                    'genres': movie_data['genres']
                }
            )
            MovieCollection.objects.create(collection=instance, movie=movie)

        return instance