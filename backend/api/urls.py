from django.urls import path
from .views import UploadEventsView

urlpatterns = [
    path("upload/", UploadEventsView.as_view(), name="upload-events"),
]
