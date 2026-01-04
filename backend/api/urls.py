from django.urls import path
from .views import SearchEventsView, UploadEventsView

urlpatterns = [
    path("upload/", UploadEventsView.as_view(), name="upload-events"),
    path("search/", SearchEventsView.as_view(), name="search"),
]
