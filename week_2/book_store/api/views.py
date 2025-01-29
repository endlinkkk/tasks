from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class BookView(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['get', 'post', 'head', 'options', 'put']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['author']
    pagination_class = PageNumberPagination

    @action(detail=True, methods=['post'])
    def book_buy(self, request: Request, id: int):
        with transaction.atomic():
            book = get_object_or_404(Book.objects.select_for_update(skip_locked=True), pk=id)
            if book.count > 0:
                book.count = F('count') - 1
                book.save()
                return Response({'message': 'Book purchased successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Not enough books available.'}, status=status.HTTP_400_BAD_REQUEST)


class AuthorView(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    http_method_names = ['get', 'post', 'head', 'options', 'put']
