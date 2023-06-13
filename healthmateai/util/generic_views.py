from rest_framework.generics import GenericAPIView

from healthmateai.util.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin,
    UpdateModelMixin
)


class BaseAPIView(GenericAPIView):
    """
    Store serializer classes used by the view based on the request method
    This dict should take the request method type ("POST", ...) as key
    and a serializer class a value. eg.
    serializer_classes = {
        "POST": <serializer_class>
    }
    or
    serializer_classes = {
        "POST": {
                    "serializer_class": <serializer_class>,
                    "return_serializer_class": <return_serializer_class>,
                    "status_code": <status_code>
        }
    }
    """

    serializer_classes = {}

    def get_serializer_class(self):
        """
        `get_serializer_class` will first try to retrieve the serializer class
        from the `serializer_classes` dict based on the request method and if
        a serializer class is not set it will call the super.
        """
        try:
            return self.serializer_classes[self.request.method]
        except KeyError:
            return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        if isinstance(serializer_class, dict):
            serializer_class = serializer_class['serializer_class']
        kwargs.setdefault('context', self.get_serializer_context())

        return serializer_class(*args, **kwargs)

    def get_return_serializer(self):
        """
        Return the return_serializer.
        """
        serializer_class = self.get_serializer_class()

        return serializer_class['return_serializer_class'] if (
                isinstance(serializer_class, dict)
                and serializer_class.get('return_serializer_class')
        ) else None

    def get_status_code(self):
        """
        Return the specific status_code for specific request.
        """
        serializer_class = self.get_serializer_class()

        return serializer_class['status_code'] if (
                isinstance(serializer_class, dict)
                and serializer_class.get('status_code')
        ) else None


class CreateAPIView(CreateModelMixin, BaseAPIView):
    """
    Concrete view for creating a model instance.
    """

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListAPIView(ListModelMixin, BaseAPIView):
    """
    Concrete view for listing a queryset.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveAPIView(RetrieveModelMixin, BaseAPIView):
    """
    Concrete view for retrieving a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class DestroyAPIView(DestroyModelMixin, BaseAPIView):
    """
    Concrete view for deleting a model instance.
    """

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UpdateAPIView(UpdateModelMixin, BaseAPIView):
    """
    Concrete view for updating a model instance.
    """
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateAPIView(CreateAPIView, ListAPIView):
    pass


class RetrieveUpdateAPIView(RetrieveAPIView, UpdateAPIView):
    pass


class RetrieveDestroyAPIView(RetrieveAPIView, DestroyAPIView):
    pass
