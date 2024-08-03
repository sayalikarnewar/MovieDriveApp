# movies/urls.py

from django.urls import path
from .views import LoginView, RegisterView, MovieListView, CollectionListView, CollectionCreateView, CollectionUpdateView, CollectionDetailView, CollectionDeleteView

urlpatterns = [
    # 1. Register
    path('register/', RegisterView.as_view(), name='register'),

    # 1.1 Login
    path('login/', LoginView.as_view(), name='login'),

    # 2. Get Movies List
    path('movies/', MovieListView.as_view(), name='movie-list'),

    # 4. Create Collection
    path('collection/', CollectionCreateView.as_view(), name='collection-create'),

    # 3. Get Collection List and Top 3 Favorite Genres
    path('collection/', CollectionListView.as_view(), name='collection-list'),

    # 5. Update Collection Movies by ID
    path('collection/<uuid:uuid>/', CollectionUpdateView.as_view(), name='collection-update'),

    # 6. Get Collection Details by ID
    path('collection/<uuid:uuid>/', CollectionDetailView.as_view(), name='collection-detail'),

    # 7. Delete Collection by ID
    path('collection/<uuid:uuid>/', CollectionDeleteView.as_view(), name='collection-delete'),
]
