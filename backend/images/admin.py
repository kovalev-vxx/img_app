from django.contrib import admin
from .models import *

admin.site.register(Photo)
admin.site.register(Keyword)
admin.site.register(Color)
admin.site.register(Collection)
admin.site.register(LikedPhoto)
admin.site.register(Tone)

