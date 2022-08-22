from utils import format_convert
import os
from django.conf import settings

path = os.path.join(settings.BASE_DIR , 'images/')
filename = '274053155435407292852088396216608776298_COPERNICUS_S2_SR_20200113T072249_20200113T072323_T39SWV'
format = 'jpg'
format_convert(path,filename,format)