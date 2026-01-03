from django.shortcuts import render

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import os

from .services.upload_service import handle_event_upload



class UploadEventsView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file', None)
        if not file_obj or file_obj.size == 0 or not file_obj.name.endswith('.tgz'):
            return Response({"error": "No file provided. or Invalid file format."}, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            dataset_id = handle_event_upload(file_obj)
            if dataset_id :
                return Response({
                    "message":'file Uploaded successfully',
                    "dataset_id": dataset_id,
                })
                
        except Exception as e:
            print(e)
            return Response({"message": "Failed to process file"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
