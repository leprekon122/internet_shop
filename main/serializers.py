from rest_framework import serializers
from .models import *


class NothebooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotebooksList
        fields = ['id', 'brand', 'title', 'pic', 'description', 'price', 'in_out']


class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsUsers
        fields = ['id', 'rating', 'name_of_user', 'name_of_stuff', 'comment']


class CartApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCart
        fields = ['user_name', 'product_title']
