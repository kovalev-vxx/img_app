from rest_framework import serializers
from images.models import *


class KeywordsSerializer(serializers.ModelSerializer):
    total = serializers.IntegerField(source="photos.count")

    class Meta:
        model = Keyword
        fields = ["keyword", "total"]


class PhotoSerializer(serializers.ModelSerializer):
    keywords = serializers.StringRelatedField(many=True)
    colors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Photo
        fields = "__all__"



class ColorSerializer(serializers.ModelSerializer):
    total = serializers.IntegerField(source="photos.count")

    class Meta:
        model = Color
        fields = ["color", "tone", "total"]


class LikePhotoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LikedPhoto
        fields = "__all__"


class LikePhotoSerializerExpanded(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    photo = PhotoSerializer(many=False)

    class Meta:
        model = LikedPhoto
        fields = "__all__"


class CollectionSerializerExpanded(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True)

    class Meta:
        model = Collection
        fields = ["id", "title", "photos"]


class CollectionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Collection
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    likes = LikePhotoSerializerExpanded(many=True)
    collections = CollectionSerializerExpanded(many=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "likes", "collections"]
