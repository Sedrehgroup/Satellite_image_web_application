import os.path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils import GetImageCollection, LayerAdd, GetImageClass, format_convert
from uuid import uuid4
from django.contrib.gis.geos import GEOSGeometry
import datetime
from django.views.static import serve
from os.path import exists
from django.conf import settings

# Create your views here.
file_name = "2743382997156288450086115630723756161_COPERNICUS_S2_20210102T072311_20210102T072312_T39SWV"


class GetImageCollectionAPI(APIView):
    def post(self, request):

        start_date = request.data.get('start')
        end_date = request.data.get('end')
        geom = request.data.get('geom')

        # check dates
        if not isinstance(start_date, str) or not isinstance(end_date, str):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"fail": "dates not correct!"})
        try:
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
            datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"fail": "Incorrect date format! must be YYYY-mm-dd"})

        # check geom
        try:
            polygon_type = GEOSGeometry(str(geom['features'][0]['geometry']))
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"fail": "Incorrect polygon format!"})

        # get image names and dates
        image_class = GetImageCollection(start=start_date, end=end_date, polygon=geom)
        image_names, image_dates = image_class.get_dates()

        # data = {}
        # for name, date in zip(image_names,image_dates):
        #     data[date] = name

        data = []
        for name, date in zip(image_names, image_dates):
            data.append({"name": name, "date": date})

        return Response(status=status.HTTP_200_OK , data=data)


class GetImage(APIView):
    def post(self, request):
        # render random order id
        order_id = uuid4().int

        # get image_name and geom
        image_name = request.data.get('image_name')
        geom = request.data.get('geom')

        # check geom
        try:
            polygon_type = GEOSGeometry(str(geom['features'][0]['geometry']))
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"fail": "Incorrect polygon format!"})

        # get image
        image_class = GetImageClass(geom)
        image = image_class.get_image(image_name)

        # prepare for download and geoserver
        image_name = image_name.replace('/', '_')
        order_name_replaced = str(order_id) + '_' + image_name

        # download image
        image_class.turn_image_to_raster(image, order_name_replaced)

        # add image to geoserver
        LayerAdd(order_name_replaced).tif_add()

        return Response(status=status.HTTP_200_OK , data=f'sedreh:{order_name_replaced}')

# class DownloadImage(APIView):
#     def get(self , request):
#
#         # file_name = request.data.get('file')
#         # check file_name
#         if not isinstance(file_name, str):
#             return Response(status=status.HTTP_400_BAD_REQUEST, data={"fail": "file name not correct!"})
#
#         path = '/api_django/images/'
#         file_path = path + file_name + '.tif'
#         if not exists(file_path):
#             return Response(status=status.HTTP_404_NOT_FOUND , data= {"fail" : "file not found!"})
#         return serve(request , os.path.basename(file_path) , os.path.dirname(file_path))
#



class DownloadImage(APIView):
    def get(self, request , data  ):
        # get format and filename from URL
        format , filename = data.split('&')

        # check file_name
        if not isinstance(filename, str):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"fail": "file name not correct!"})

        path = os.path.join(settings.BASE_DIR , 'images/')

        # get file path and check exists
        file_path = path + file_name + '.tif'
        if not exists(file_path):
            return Response(status=status.HTTP_404_NOT_FOUND , data= {"fail" : "file not found!"})

        target_file_path = format_convert(path, filename, format)

        return serve(request , os.path.basename(target_file_path) , os.path.dirname(target_file_path))
