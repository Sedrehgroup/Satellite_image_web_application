from django.urls import path , re_path
from .views import GetImageCollectionAPI , GetImage , DownloadImage

urlpatterns = [
    path('get-image-collection/' , GetImageCollectionAPI.as_view() ),
    path('get-image/' , GetImage.as_view() ),
    re_path(r'^download-image/(?P<data>.+)/$' , DownloadImage.as_view() ),
    # path('download-image/<str:format>' , DownloadImage.as_view() ),
]