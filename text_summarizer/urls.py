from django.urls import path

from . import views

app_name = 'search'

urlpatterns = [
    path(
        'summarizes/',
        views.ListCreateSummarizeAPIView.as_view(),
        name='list_create_summarize_view'
    ),
    path(
        'summarizes/<int:patient_id>/',
        views.ListPatientSummarizeAPIView.as_view(),
        name='list_patient_summarize_view'
    )
]
