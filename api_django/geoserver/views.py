from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status
from .geoserver import create_layer_with_store, get_or_create_workspace
from django.conf import settings
# Create your views here.


class Index(APIView):
    def get(self, request):
        layer_add()
        return Response(status=status.HTTP_200_OK, data={"message": "done"})