from collections import OrderedDict

from drf_yasg import openapi
from drf_yasg.errors import SwaggerGenerationError
from drf_yasg.inspectors import NotHandled, ReferencingSerializerInspector
from drf_yasg.openapi import SchemaRef
from drf_yasg.utils import get_serializer_class, filter_none
from rest_framework import serializers


class NestedSerializerReadOnlyInspector(ReferencingSerializerInspector):
    """
    This inspector is for supporting the readonly attribute for the nested
    serializers.

    This inspector solves the issue of
    `https://github.com/axnsan12/drf-yasg/issues/343`
    """

    def field_to_swagger_object(self, field, swagger_object_type,
                                use_references, **kwargs):
        SwaggerType, ChildSwaggerType = self._get_partial_types(
            field,
            swagger_object_type,
            use_references,
            **kwargs
        )
        if isinstance(field, serializers.Serializer):
            if swagger_object_type != openapi.Schema:
                raise SwaggerGenerationError(
                    "cannot instantiate nested serializer as " +
                    swagger_object_type.__name__
                )

            ref_name = self.get_serializer_ref_name(field)

            def make_schema_definition(serializer=field):
                properties = OrderedDict()
                required = []
                for property_name, child in serializer.fields.items():
                    property_name = self.get_property_name(property_name)
                    prop_kwargs = {
                        'read_only': bool(child.read_only) or None
                    }
                    prop_kwargs = filter_none(prop_kwargs)
                    child_schema = self.probe_field_inspectors(
                        child, ChildSwaggerType, use_references, **prop_kwargs
                    )
                    # NOTE: This is the part of the code that was modified from
                    # the original. This change resolves a drf-yasg issue where
                    # read-only nested serailizers as not correctly treated as
                    # read-only in the swagger schema.
                    if isinstance(child_schema, SchemaRef) and child.read_only:
                        # Here we need to add the readOnly attribute again.
                        child_schema = OrderedDict(
                            readOnly=True,
                            allOf=[child_schema]
                        )
                    properties[property_name] = child_schema

                    if child.required and not getattr(child_schema, 'read_only',
                                                      False):
                        required.append(property_name)

                result = SwaggerType(
                    # the title is derived from the field name and is better to
                    # be omitted from models
                    use_field_title=False,
                    type=openapi.TYPE_OBJECT,
                    properties=properties,
                    required=required or None,
                )

                setattr(result, '_NP_serializer',
                        get_serializer_class(serializer))
                return result

            if not ref_name or not use_references:
                return make_schema_definition()

            definitions = self.components.with_scope(openapi.SCHEMA_DEFINITIONS)
            actual_schema = definitions.setdefault(ref_name,
                                                   make_schema_definition)
            actual_schema._remove_read_only()

            actual_serializer = getattr(actual_schema, '_NP_serializer', None)
            this_serializer = get_serializer_class(field)
            if actual_serializer and actual_serializer != this_serializer:
                explicit_refs = self._has_ref_name(
                    actual_serializer) and self._has_ref_name(this_serializer)
                if not explicit_refs:
                    raise SwaggerGenerationError(
                        "Schema for %s would override distinct serializer %s "
                        "because they implicitly share the same ref_name; "
                        "explicitly set the ref_name attribute on both "
                        "serializers' Meta classes"
                        % (actual_serializer, this_serializer))

            return openapi.SchemaRef(definitions, ref_name)

        return NotHandled
