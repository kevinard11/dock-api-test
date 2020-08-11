# from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag, Ingredient, Recipe
from recipe import serializers

# Create your views here.

class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base viewset for user owned recipe attribute"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated object only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)

class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredient in the database"""

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipe in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipe for the authenticated user"""
        return self.queryset.filter(user = self.request.user )
# class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
#     """Manage tags in the database"""
#
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#
#     queryset = Tag.objects.all()
#     serializer_class = serializers.TagSerializer
#
#     def get_queryset(self):
#         """Return objects for the current authenticated object only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')
#
#     def perform_create(self, serializer):
#         """Create a new tag"""
#         serializer.save(user=self.request.user)
#
# class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
#     """Manage ingredient in the database"""
#
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#
#     queryset = Ingredient.objects.all()
#     serializer_class = serializers.IngredientSerializer
#
#     def get_queryset(self):
#         """Return objects for the current authenticated user"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')
#
#     def perform_create(self, serializer):
#         """Create a new ingredient"""
#         serializer.save(user=self.request.user)
