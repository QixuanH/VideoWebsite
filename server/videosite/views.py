from django.shortcuts import render
from django.views import generic
from .models import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.hashers import check_password
import jwt
from datetime import datetime, timedelta
from rest_framework.parsers import FileUploadParser
import time
import os
import json
from django.core.paginator import Paginator, InvalidPage

def generate_jwt_token(user_id):
    # 设置过期时间为 1 小时
    expire_time = datetime.utcnow() + timedelta(hours=1)
    # 构建 JWT 载荷
    payload = {
        'user_id': user_id,
        'exp': expire_time
    }
    # 生成 JWT 令牌
    token = jwt.encode(payload, 'secret_key', algorithm='HS256')
    return token

def get_user_id_from_token(token):
    decoded_token = jwt.decode(token, 'secret_key', algorithms=['HS256'])
    user_id = decoded_token.get('user_id')
    return user_id
    
def encrypt_password(password):
    md5_hash = hashlib.md5()
    md5_hash.update(password.encode('utf-8'))
    encrypted_password = md5_hash.hexdigest()
    return encrypted_password


class LoginAPIView(APIView):
    def post(self, request):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = encrypt_password(request.POST.get('password'))
            print(password)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'message':'Invalid credentials'}, status=201)
            # 验证密码
            if password == user.pwd:
                # 登录成功，生成并返回登录令牌
                # 可以使用 JWT 库生成令牌
                token = generate_jwt_token(user.id)
                return Response({'token': token}, status=200)
            else:
                return Response({'message':'Wrong password.'}, status=200)
        else:
            return Response({'message': 'Please using POST method.'}, status=400)
 
        serializer = UserSerializer(data=request.data)
        
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # 创建新用户
            return Response({'message': 'User registered successfully.'}, status=200)
        else:
            return Response(serializer.errors, status=400)

class FileUploadView(APIView):    
    parser_classes = [FileUploadParser]
    def post(self, request, format = None):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        file_obj = request.FILES['file']
        file_name = encrypt_password(int(time.time())) 
        path = os.path.join(settings.STATIC_ROOT, file_name)
        print(file_name)
        with open(path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)   
        return Response({'message': 'File uploaded successfully'}, status=200)

class GetVideoDetailView(APIView):
    def get(self, request, format = None):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        video = Video.objects.get(pk=request.data['video'])
        print(type(video))
        serializer = VideoSerializer(instance=video)
        print(serializer.data)
        if serializer.data is not None:
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
        
class GetVideoList(APIView):
    def get(self, request, format = None):
        print(request.data)
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        keyword = request.data['keyword'] if 'keyword' in request.data else ''
        page = request.data['page'] if 'page' in request.data else 1

        # 进行关键词查询
        videos = Video.objects.filter(title__icontains=keyword)

        # 对查询结果进行分页
        paginator = Paginator(videos, 10)  # 每页显示10个结果
        try:
            page_videos = paginator.page(page)
        except InvalidPage:
            return Response({'message': 'Invalid page number.'}, status=400)

        # 序列化分页后的结果
        serializer = VideoSerializer(page_videos, many=True)

        # 返回序列化数据和分页信息
        response_data = {
            'results': serializer.data,
            'page': page_videos.number,
            'total_pages': paginator.num_pages,
            'total_results': paginator.count
        }
        return Response(response_data, status=200)        

class AddVideoView(APIView):
    def post(self, request, format = None):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        user = User.objects.get(pk=user_id)
        file = File.objects.get(pk=request.data['file'])
        video = Video.objects.create(
            title = request.data['title'],
            introduction = request.data['introduction'],
            user = user,
            file = file
        )
        labels = json.loads(request.data['labels']) 
        for label_id in labels:
            print(label_id)
            label = Label.objects.get(pk=label_id)
            video.labels.add(label)
        video.save()
        return Response({'message': 'Video created successfully.'}, status=200)

class RecommandListView(APIView):
    def get(self, request):
            try:
                token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
                user_id = get_user_id_from_token(token)
            except Exception:
                return Response({'error': 'Invalid Token'}, status=400)
            recommand = Recommend.objects.all()
            print(recommand)
            serializer = RecommandSerializer(recommand, many=True)
            return Response(serializer.data)

class BannerListView(APIView):
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        banner = Banner.objects.all()
        print(banner)
        serializer = BannerSerializer(banner, many=True)
        return Response(serializer.data)

class LabelListAPIView(APIView):
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            user_id = get_user_id_from_token(token)
        except Exception:
            return Response({'error': 'Invalid Token'}, status=400)
        labels = Label.objects.all()
        serializer = LabelSerializer(labels, many=True)
        return Response(serializer.data)
    
 
class UserApiTest(generics.ListCreateAPIView):
    queryset = User.objects.all()
    print(queryset)
    serializer_class = UserSerializer

