# movies/urls.py

from django.urls import path
from .views import RegisterView, LoginView, MovieListView, CollectionListView, CollectionCreateView, CollectionUpdateView, CollectionDetailView, CollectionDeleteView

urlpatterns = [
    # 1. Register
    path('register/', RegisterView.as_view(), name='register'),

    # 2. Login
    path('login/', LoginView.as_view(), name='login'),

    # 3. Get Movies List
    path('movies/', MovieListView.as_view(), name='movie-list'),

    # 4. Create Collection
    path('collection/create/', CollectionCreateView.as_view(), name='collection-create'),
    
    # 5. Get Collection List and Top 3 Favorite Genres
    path('collection/list/', CollectionListView.as_view(), name='collection-list'),
    
    # 6. Update Collection Movies by ID (PUT request)
    path('collection/<uuid:uuid>/', CollectionUpdateView.as_view(), name='collection-update'),

    # 7. Get Collection Details by ID (GET request)
    path('collection/get/<uuid:uuid>/', CollectionDetailView.as_view(), name='collection-detail'),

    # 8. Delete Collection by ID (DELETE request)
    path('collection/delete/<uuid:uuid>/', CollectionDeleteView.as_view(), name='collection-delete'),
]