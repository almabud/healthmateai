from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework import status, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from healthmateai.util.pagination import PageNumberPagination, CursorPagination


class CreateModelMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        """
        Generates a Response object with create status and response data.
        Accepts optional `return_serializer` and return_status_code` kwargs
        or from the serializer_classes dict that will be used if set to override
        the serializer used in the response data and response status code.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return_serializer = (
                kwargs.get('return_serializer') or self.get_return_serializer()
        )
        data = return_serializer(
            serializer.instance, context=self.get_serializer_context()
        ).data if return_serializer else serializer.data

        return Response(
            data,
            status=(
                kwargs.get('return_status_code')
                or self.get_status_code()
                or status.HTTP_201_CREATED
            ),
            headers=headers
        )


class ListModelMixin(mixins.ListModelMixin):
    pagination_class = PageNumberPagination

    def get_pagination_class(self):
        paginator_name = self.request.GET.get('pagination')

        try:
            return {
                "page": PageNumberPagination,
                "cursor": CursorPagination
            }[paginator_name]
        except KeyError:
            return self.pagination_class

    @property
    def paginator(self):
        """
        Allow pagination to be overided via query params.
        """

        if not hasattr(self, '_paginator'):
            pagination_class = self.get_pagination_class()
            if pagination_class is None:
                self._paginator = None
            else:
                self._paginator = pagination_class()

        return self._paginator

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            serializer.data,
            status=(
                    kwargs.get('return_status_code')
                    or self.get_status_code() or status.HTTP_200_OK
            )
        )


class RetrieveModelMixin:
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            serializer.data,
            status=(
                    kwargs.get('return_status_code')
                    or self.get_status_code() or status.HTTP_200_OK
            )
        )


class UpdateModelMixin(mixins.UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        """
        Generates a Response object with response data.
        Accepts optional `return_serializer` and return_status_code` kwargs
        or from the serializer_classes dict that will be used if set to override
        the serializer used in the response data and response status code.
        """

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return_serializer = (
                kwargs.get('return_serializer') or self.get_return_serializer()
        )
        data = return_serializer(
            serializer.instance, context=self.get_serializer_context()
        ).data if return_serializer else serializer.data

        return Response(
            data,
            status=(
                    kwargs.get('return_status_code')
                    or self.get_status_code() or status.HTTP_200_OK
            )
        )


class DestroyModelMixin(mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        self.perform_destroy(serializer)

        return Response(
            data={'status': 'success'},
            status=(
                    kwargs.get('return_status_code')
                    or self.get_status_code() or status.HTTP_200_OK
            )
        )

    def perform_destroy(self, serializer):
        serializer.destroy()
