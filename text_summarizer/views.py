from rest_framework.permissions import AllowAny

from healthmateai.util.generic_views import CreateAPIView, ListCreateAPIView
from text_summarizer.models import SummarizeRequest
from text_summarizer.serializers import (
    CreateTextSummarizerSerializer, TextSummarizerSerializer
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



