from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Author, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Author
        fields = ["id", "user", "bio"]


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "author",
            "content",
            "created_at",
        ]
        read_only_fields = ["author", "created_at", "post"]


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "comments_count",
        ]
        read_only_fields = [
            "author",
            "created_at",
            "comments_count",
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()
