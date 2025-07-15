from django.urls import path
from . import views
urlpatterns = [
    path("batches_list/",       views.BatchesView.as_view(),  name="batches_list"),
    path("add_batches/",        views.AddBatchesView.as_view(), name="add_batches"),
    path(
        "batch-detail/<str:uuid>/",
        views.BatchDetailView.as_view(),
        name="batch-detail",
    ),
    path(
        "batch-delete/<str:uuid>/",
        views.BatchDeleteView.as_view(),
        name="batch-delete",
    ),
    path(
        "batch-update/<str:uuid>/",
        views.BatchUpdateView.as_view(),
        name="batch-update",
    ),
]
