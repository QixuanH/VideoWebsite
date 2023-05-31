from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Video)
admin.site.register(Label)
admin.site.register(File)
admin.site.register(HistoryRecord)
admin.site.register(Recommend)
admin.site.register(Banner)
admin.site.register(Subscription)


