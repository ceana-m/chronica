from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(List)
admin.site.register(Review)
admin.site.register(Movie)
admin.site.register(Media)