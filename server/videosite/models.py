#PhoneReview/models.py
# Create your models here.
from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class File(models.Model):
    path = models.CharField(max_length=255)
    status = models.IntegerField(default=1)
    def __str__(self):
        return str(self.id)

class Label(models.Model):
    name = models.CharField(max_length=255)
    introduction = models.CharField(max_length=255)
    status = models.IntegerField(default=1)
    def __str__(self):
        return str(self.id)
    

class HistoryRecord(models.Model):
    video = models.IntegerField()
    crate_time = models.DateField()
    status = models.IntegerField(default=1)
    def __str__(self):
        return str(self.id)
    
class User(models.Model):
    nickname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pwd = models.CharField(max_length=255)
    history_record = models.ManyToManyField(HistoryRecord,related_name= 'record_by_user' )
    status = models.IntegerField(default=1)
    def __str__(self):
        return str(self.id)
    
class Video(models.Model):
    title = models.CharField(max_length=255)
    introduction = models.CharField(max_length=255)
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='videos_label')
    labels = models.ManyToManyField(Label)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos_created')
    status = models.IntegerField(default=1)
    def __str__(self):
        return str(self.id)
    
class Recommend(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    sort = models.IntegerField()
    def __str__(self):
        return str(self.id)
    
class Banner(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)
    
class Subscription(models.Model):
    user_id = models.IntegerField()
    creator_id = models.IntegerField()
    status = models.IntegerField(default=1)
    def __str__(self):
        return str(self.id)

