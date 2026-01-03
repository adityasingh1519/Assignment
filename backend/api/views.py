from django.shortcuts import render

import tarfile
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import os


# Create your views here.
class UploadEventsView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file", None)
        if not file_obj:
            return Response(
                {"error": "No file provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure the upload directory exists
        upload_dir = settings.EVENT_FILES_DIR
        os.makedirs(upload_dir, exist_ok=True)

        # Save the uploaded file temporarily
        temp_file_path = os.path.join(upload_dir, "temp_upload.tar.gz")
        with open(temp_file_path, "wb+") as temp_file:
            for chunk in file_obj.chunks():
                temp_file.write(chunk)

        # Extract the tar.gz file
        try:
            with tarfile.open(temp_file_path, "r:gz") as tar:
                tar.extractall(path=upload_dir)
        except tarfile.TarError as e:
            return Response(
                {"error": f"Failed to extract tar.gz file: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        finally:
            # Remove the temporary file
            os.remove(temp_file_path)

        return Response(
            {"message": "File uploaded and extracted successfully."},
            status=status.HTTP_200_OK,
        )
