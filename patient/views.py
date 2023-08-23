from rest_framework import exceptions
from rest_framework.permissions import AllowAny

from healthmateai.util.generic_views import ListCreateAPIView, RetrieveAPIView
from patient.models import Patient
from patient.serializers import PatientSerializer


class ListCreatePatientAPIView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PatientSerializer

    def get_queryset(self):
        return Patient.objects.all()


class RetrievePatientAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PatientSerializer

    def get_object(self):
        try:
            return Patient.objects.get(id=self.kwargs.get('patient_id'))
        except Patient.DoesNotExist:
            raise exceptions.NotFound()
