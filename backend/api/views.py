from django.shortcuts import render

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import os
import time


from .services.upload_service import handle_event_upload
from .services.search_service import search_dataset
from .utils.event_parser import parse_event_line



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
        


class SearchEventsView(APIView):
    def post(self, request):
        query = request.data.get("query", "")
        start_time = request.data.get("start_time")
        end_time = request.data.get("end_time")
        dataset_id = request.data.get("dataset_id")

        if not dataset_id or start_time is None or end_time is None:
            return Response(
                {"error": "dataset_id, start_time and end_time are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        dataset_dir = os.path.join(
            settings.EVENT_FILES_DIR,
            "datasets",
            dataset_id,
        )

        if not os.path.isdir(dataset_dir):
            return Response(
                {"error": "Invalid dataset_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        start_time = int(start_time)
        end_time = int(end_time)

        start = time.perf_counter()
        try:
            results = search_dataset(
                dataset_dir,
                query,
                start_time,
                end_time,
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": "Error during search"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        duration = time.perf_counter() - start

        return Response(
            {
                "results": results,
                "search_time_seconds": round(duration, 4),
            },
            status=status.HTTP_200_OK,
        )
