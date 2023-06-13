from django.urls import path

from . import views

app_name = 'patient'

urlpatterns = [
    path(
        'patients/',
        views.ListCreatePatientAPIView.as_view(),
        name='list_create_patient_view'
    ),
    path(
        'patients/<int:patient_id>/',
        views.RetrievePatientAPIView.as_view(),
        name='retrieve_patient_view'
    )
]
