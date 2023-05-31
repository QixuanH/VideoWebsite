from rest_framework import serializers
from .models import *
import hashlib

def encrypt_password(password):
    md5_hash = hashlib.md5()
    md5_hash.update(password.encode('utf-8'))
    encrypted_password = md5_hash.hexdigest()
    return encrypted_password

def get_user_id_from_token(self, token):
    decoded_token = jwt.decode(token, 'secret_key', algorithms=['HS256'])
    user_id = decoded_token.get('user_id')
    return user_id

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['nickname','pwd','phone','email']
    
    def create(self, validated_data):
        password = validated_data.pop('pwd')
        hashed_password = encrypt_password(password=password)
        user = User.objects.create(pwd=hashed_password, **validated_data)
        return user

class AddVideoSerializer(serializers.ModelSerializer):
    labels = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Video
        fields = ('__all__')

    def create(self, validated_data):
        file = validated_data['file']
        title = validated_data['title']
        introduction = validated_data['introduction']
        token = validated_data['token']
        user_id = get_user_id_from_token(token)
        labels = validated_data['labels']
        
        video = Video.objects.create(
            title=title,
            introduction=introduction
        )

        file = File.objects.get(pk=file)
        video.file = file
        user = User.objects.get(pk=user_id)
        video.user = user
        for label_id in labels:
            label = Label.objects.get(id=label_id)
            video.labels.add(label)
        print(video)
        return video

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('id', 'name', 'introduction', 'status')

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True)  # 嵌套Label序列化器
    file = FileSerializer()  # 嵌套File序列化器
    class Meta:
        model = Video
        fields = ('__all__')


class BannerSerializer(serializers.ModelSerializer):
    video = VideoSerializer()
    class Meta: 
        model = Banner
        fields = ('__all__')

class RecommandSerializer(serializers.ModelSerializer):
    video = VideoSerializer()
    class Meta: 
        model = Recommend
        fields = ('__all__')