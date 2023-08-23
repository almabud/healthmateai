from rest_framework.permissions import AllowAny

from healthmateai.util.generic_views import (
    CreateAPIView, ListCreateAPIView, ListAPIView
)
from text_summarizer.models import SummarizeRequest
from text_summarizer.serializers import (
    CreateTextSummarizerSerializer, TextSummarizerSerializer,
    PatientTextSummarizeSerializer
)


class ListCreateSummarizeAPIView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TextSummarizerSerializer
    serializer_classes = {
        'POST': {
                "serializer_class": CreateTextSummarizerSerializer,
                "return_serializer_class": TextSummarizerSerializer,
        }
    }

    def get_queryset(self):
        return SummarizeRequest.objects.all()


class ListPatientSummarizeAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_classes = PatientTextSummarizeSerializer

    def get_queryset(self):
        return SummarizeRequest.objects.filter(
            patient__id=self.kwargs.get('patient_id')
        ).order_by('-id')
