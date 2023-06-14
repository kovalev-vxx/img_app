from django.db import models
from django.contrib.auth import get_user_model


class Photo(models.Model):
    photo_id = models.CharField(primary_key=True, max_length=100)
    photo_url = models.CharField(max_length=100)
    photo_image_url = models.CharField(max_length=100)
    photo_width = models.IntegerField()
    photo_height = models.IntegerField()
    photo_description = models.CharField(max_length=200)
    photographer_username = models.CharField(max_length=100)
    photographer_first_name = models.CharField(max_length=100)
    photographer_last_name = models.CharField(max_length=100)
    blur_hash = models.CharField(max_length=200)




class Keyword(models.Model):
    keyword = models.CharField(max_length=30)
    photos = models.ManyToManyField(Photo, related_name="keywords")

    def __str__(self):
        return self.keyword


class Tone(models.Model):
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE, primary_key=True)
    hex = models.CharField(max_length=6)
    white = models.FloatField()
    black = models.FloatField()
    red = models.FloatField()
    green = models.FloatField()
    blue = models.FloatField()
    cyan = models.FloatField()
    magenta = models.FloatField()
    yellow = models.FloatField()

    def __str__(self):
        return self.hex


class Color(models.Model):
    photos = models.ManyToManyField(Photo, related_name="colors")
    color = models.CharField(max_length=30)
    tone = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.tone


class LikedPhoto(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="likes")
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('photo', 'user',)


class Collection(models.Model):
    photos = models.ManyToManyField(Photo, blank=True)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="collections")

    class Meta:
        unique_together = ('title', 'user',)
