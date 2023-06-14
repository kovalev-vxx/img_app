from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from django.db.models import Count
import random
from rest_framework.permissions import IsAuthenticated

import images.serializers as serializers
import images.models as models


class PhotoListView(generics.ListAPIView):
    serializer_class = serializers.PhotoSerializer

    def get_queryset(self):
        queryset = models.Photo.objects.all()
        if self.request.query_params:
            width = self.request.query_params.get('width')
            color = self.request.query_params.get('color')
            keyword = self.request.query_params.get('keyword')
            height = self.request.query_params.get('height')
            random_seed = self.request.query_params.get('random')
            if keyword:
                keywords = models.Keyword.objects.all()
                keywords = keywords.filter(keyword__iregex=(r'\b' + keyword.lower() + r"\b"))
                photo_ids = keywords.values_list('photo', flat=True)
                queryset = queryset.filter(pk__in=photo_ids)
            if color:
                photo_ids = models.Color.objects.all().filter(keyword=str(color)).values_list("photo", flat=True)
                queryset = queryset.filter(pk__in=photo_ids)
            if width:
                queryset = queryset.filter(photo_width=int(width))
            if height:
                queryset = queryset.filter(photo_height=int(height))
            if random_seed:
                queryset = list(queryset)
                random.seed(int(random_seed))
                random.shuffle(queryset)

        return queryset


class SearchPhotoListView(generics.ListAPIView):
    serializer_class = serializers.PhotoSerializer

    def get_queryset(self):
        queryset = models.Photo.objects.all()
        if self.request.query_params:
            width = self.request.query_params.get('width')
            colors = self.request.query_params.getlist('colors[]')
            keywords = self.request.query_params.getlist('keywords[]')
            height = self.request.query_params.get('height')
            random_seed = self.request.query_params.get('random')
            tone = self.request.query_params.get('tone')
            if keywords:
                found_keywords = []
                for keyword in keywords:
                    keywords_q = models.Keyword.objects.filter(keyword__iregex=(r'\b' + keyword.lower() + r"\b"))
                    found_keywords.extend(keywords_q)
                queryset = queryset.filter(keywords__in=found_keywords).distinct()
            if colors:
                queryset = queryset.filter(colors__color__in=colors)
            if tone:
                queryset = queryset.order_by(f"-tone__{tone}")
                max_tone = getattr(queryset[0].tone, tone)
                diff = max_tone-max_tone*0.2
                queryset = queryset.filter(**{f"tone__{tone}__gt":diff})
            if width:
                queryset = queryset.filter(photo_width=int(width))
            if height:
                queryset = queryset.filter(photo_height=int(height))
            if random_seed and not tone:
                queryset = list(queryset)
                random.seed(int(random_seed))
                random.shuffle(queryset)

        return queryset


class ColorView(generics.ListAPIView):
    queryset = models.Color.objects.annotate(total=Count("photos")).order_by("-total")
    serializer_class = serializers.ColorSerializer
    pagination_class = None


class KeywordView(generics.ListAPIView):
    queryset = models.Keyword.objects.annotate(total=Count("photos")).order_by("-total")
    serializer_class = serializers.KeywordsSerializer


class UserView(APIView):
    def get(self, request):
        user = get_user_model().objects.get(username=self.request.user)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)


class LikePhotoCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.LikePhotoSerializer


class LikePhotoView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.LikePhotoSerializerExpanded
    pagination_class = None

    def get_queryset(self):
        return models.LikedPhoto.objects.all().filter(user=self.request.user)


class LikePhotoDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.LikePhotoSerializer

    def get_queryset(self):
        return models.LikedPhoto.objects.all().filter(user=self.request.user)


class CollectionView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CollectionSerializer
    pagination_class = None

    def get_queryset(self):
        return models.Collection.objects.all().filter(user=self.request.user)


class CollectionCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CollectionSerializer


class CollectionExpandedView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CollectionSerializerExpanded
    pagination_class = None

    def get_queryset(self):
        return models.Collection.objects.all().filter(user=self.request.user)


class CollectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CollectionSerializer

    def get_queryset(self):
        return models.Collection.objects.all().filter(user=self.request.user)
