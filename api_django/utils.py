from django.conf import settings
from geoserver.geoserver import create_layer_with_store , get_or_create_workspace , exist_layer
import os
from zipfile import ZipFile
import numpy as np
import rasterio as rio
import cv2
from os.path import basename
import requests
import ee
service_account = 'geo-test@geotest-317218.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, 'geotest-privkey.json')
ee.Initialize(credentials)

if not os.path.isdir(os.path.join(settings.BASE_DIR , 'images')):
    os.mkdir(os.path.join(settings.BASE_DIR , 'images'))

class GetImageCollection():
    def __init__(self, start=None, end=None, polygon=None):
        self.start = start
        self.end = end
        self.polygon = ee.Geometry.Polygon(polygon['features'][0]['geometry']['coordinates'])

    def get_dates(self):
        images = self.get_image_collection()
        dates = []
        data = []
        for item in images.getInfo()['features']:
            data.append(item['id'])
            DATE = item['id'].split('/')[2][:8]
            DATE = DATE[:4] + '-' + DATE[4:6] + '-' + DATE[6:]
            dates.append(DATE)
        return [data, dates]

    def get_image_collection(self):
        images = (ee.ImageCollection("COPERNICUS/S2_SR")
                  .filterDate(self.start, self.end)
                  .filterBounds(self.polygon))
        return images



class GetImageClass():
    def __init__(self , geom):
        self.polygon = ee.Geometry.Polygon(geom['features'][0]['geometry']['coordinates'])

    def get_image(self, image_name):
        image_by_name = ee.Image(image_name).clip(self.polygon).select(['TCI_R', 'TCI_G', 'TCI_B'])
        return image_by_name

    def turn_image_to_raster(self, image, title, folder=os.path.join(settings.BASE_DIR , 'images/')):
        # download image from google earth engine
        url = image.getDownloadURL(
            params={'name': title, 'scale': 10, 'region': self.polygon , 'crs': 'EPSG:4326', 'filePerBand': False,
                    'format': 'GEO_TIFF'})
        zipurl = url
        print(url)

        if not os.path.exists(folder):
            os.mkdir(folder)

        with requests.get(url) as resp:
            with open(folder + title + '.tif', 'wb') as fd:
                fd.write(resp.content)

        return None

# geom = {
#   "type": "FeatureCollection",
#   "features": [
#     {
#       "type": "Feature",
#       "properties": {},
#       "geometry": {
#         "type": "Polygon",
#         "coordinates": [
#           [
#             [
#               51.840362548828125,
#               35.74386509767359
#             ],
#             [
#               51.847829818725586,
#               35.74386509767359
#             ],
#             [
#               51.847829818725586,
#               35.74922899279072
#             ],
#             [
#               51.840362548828125,
#               35.74922899279072
#             ],
#             [
#               51.840362548828125,
#               35.74386509767359
#             ]
#           ]
#         ]
#       }
#     }
#   ]
# }
# order_id = '1'
# image_class = GetImage(start = '2020-01' , end = '2020-02' , polygon = geom)
# image_names , image_dates = image_class.get_dates()
# print(image_dates)
# for item in image_names:
#   image = image_class.get_image(item)
#   image_class.turn_image_to_raster(image,order_id + '_' + item,image_class.polygon,)







class LayerAdd():
    def __init__(self, filename):
        # self.workspace = get_or_create_workspace()
        self.layer_name = filename
        self.filename = filename+'.tif'
        self.store_name = self.layer_name
        self.path = settings.GEOSERVER.get('RASTER_URL')
        self.url = None
        self.layer = None

    def tif_add(self):
        self.url = os.path.join(self.path, self.filename)
        self.layer = self.layer_name
        if not exist_layer(self.layer,settings.GEOSERVER.get('WORKSPACE')):
            create_layer_with_store(data_type='tiff', url=self.url, layer_name=self.layer, store_name=self.layer )
            # self.input_transparent()
        return self.layer

    def input_transparent(self):
        user = settings.GEOSERVER.get('USERNAME')
        password = settings.GEOSERVER.get('PASSWORD')
        workspace = settings.GEOSERVER.get('WORKSPACE')
        host = settings.GEOSERVER.get('HOST')
        port = settings.GEOSERVER.get('PORT')
        headers = {
            'Content-Type': 'text/xml',
        }
        data = '<coverage><parameters><entry><string>InputTransparentColor</string><string>#000000</string></entry></parameters></coverage>'
        response = requests.put(f'http://{host}:{port}/geoserver/rest/workspaces/{workspace}/coveragestores/{self.layer}/coverages/{self.layer}.xml',
                                headers=headers, data=data, auth=(user, password))



def format_convert(path, filename, format):
    # path = os.path.join(settings.BASE_DIR , 'images')
    if format == 'tif':
        file_format = '.tif'
    else :
        # tif to jpeg
        source_file = cv2.imread(path + filename + '.tif')
        target_file = cv2.imwrite(path + filename + '.jpg' , source_file )
        file_format = '.jpg'

    target_file_path = path + filename + file_format

    target_file_path_zip = path + filename + '.zip'
    with ZipFile(target_file_path_zip , 'w') as zip_file:
        zip_file.write(target_file_path , basename(target_file_path))

    return target_file_path_zip