from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie, Collection, CollectionMovie

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class CollectionMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionMovie
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    movies = CollectionMovieSerializer(many=True, required=False)

    class Meta:
        model = Collection
        fields = ['uuid', 'title', 'description', 'movies']

    def create(self, validated_data):
        movies_data = validated_data.pop('movies')
        collection = Collection.objects.create(**validated_data)
        for movie_data in movies_data:
            movie, _ = Movie.objects.get_or_create(**movie_data)
            CollectionMovie.objects.create(collection=collection, movie=movie)
        return collection