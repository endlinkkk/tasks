from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AuthorView, BookView

router = DefaultRouter()
router.register(r'books', BookView, basename='books')
router.register(r'authors', AuthorView, basename='authors')

urlpatterns = [
    path('books/<int:id>/buy', BookView.as_view({'post': 'book_buy'})),
]

urlpatterns += router.urls
