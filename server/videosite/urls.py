from . import views
from django.urls import path

urlpatterns = [
    path('test/', views.UserApiTest.as_view()),
    path('register/', views.RegisterAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('uploadfile/', views.FileUploadView.as_view()),
    path('labels/', views.LabelListAPIView.as_view(), name='label-list'),
    path('addvideo/', views.AddVideoView.as_view()),
    path('getvideodetail/', views.GetVideoDetailView.as_view()),
    path('getbannerlist/', views.BannerListView.as_view()),
    path('getrecommandlist/', views.RecommandListView.as_view()),
    path('getvideolist/', views.GetVideoList.as_view()) 
]
