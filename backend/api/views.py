from django.shortcuts import render

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import os
import time


from .services.upload_service import handle_event_upload
from .services.search_service import PAGE_SIZE, search_dataset
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
        cursor = request.data.get("cursor") 
        limit = request.data.get("limit", PAGE_SIZE)

        if not dataset_id:
            return Response(
                {"error": "Uploaded file is not available. Please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not query and start_time is None and end_time is None:
            return Response(
                {"error": "At least one search criteria must be provided."},
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

        try:
            start_time = int(start_time) if start_time is not None else None
            end_time = int(end_time) if end_time is not None else None
            limit = min(int(limit), PAGE_SIZE)
        except ValueError:
            return Response(
                {"error": "start_time, end_time and limit must be integers"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        query = query or ""

        start = time.perf_counter()
        try:
            results, next_cursor, has_more = search_dataset(
                dataset_dir=dataset_dir,
                query=query,
                start_time=start_time,
                end_time=end_time,
                cursor=cursor,
                limit=limit,
            )
        except Exception as e:
            print("Search error:", e)
            return Response(
                {"error": "Error during search"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        duration = time.perf_counter() - start

        return Response(
            {
                "results": results,
                "next_cursor": next_cursor, 
                "has_more": has_more,     
                "search_time_seconds": round(duration, 4),
            },
            status=status.HTTP_200_OK,
        )