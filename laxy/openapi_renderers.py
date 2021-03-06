import yaml
from http.client import responses as response_code_messages
from rest_framework import status
from rest_framework_swagger.renderers import OpenAPIRenderer as _OpenAPIRenderer
from rest_framework.renderers import JSONRenderer
from openapi_codec import OpenAPICodec as _OpenAPICodec
from coreapi import Document
from drf_openapi.codec import _generate_openapi_object, SwaggerUIRenderer
from coreapi.compat import force_bytes
from collections import OrderedDict


# https://stackoverflow.com/a/21912744/77990
def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    """
    Dumps as YAML, dealing gracefully with OrderedDicts (no !!python tag cruft).
    """
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


class OpenAPICodec(_OpenAPICodec):
    def encode(self, document, extra=None, **options):
        if not isinstance(document, Document):
            raise TypeError('Expected a `coreapi.Document` instance')

        data = _generate_openapi_object(document)
        if isinstance(extra, dict):
            data.update(extra)

        # out = yaml.dump(data)
        out = ordered_dump(data, Dumper=yaml.SafeDumper)
        return force_bytes(out)


class OpenAPIYamlRenderer(_OpenAPIRenderer):
    format = 'yaml-openapi'
    media_type = 'text/yaml'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context['response'].status_code != status.HTTP_200_OK:
            return JSONRenderer().render(data)
        extra = self.get_customizations()

        return OpenAPICodec().encode(data, extra=extra)


# TODO: This was the beginnings of trying to allow custom success codes (eg
#       201 for POST instead of 200) in the Swagger docs, via attaching
#       a success_status_code attribute to the serializer Meta class.
#       **WIP**
# class LaxySwaggerUIRenderer(SwaggerUIRenderer):
#
#     def _get_responses(link):
#         """ Returns an OpenApi-compliant response
#         """
#         # status = 200
#         status = link.success_status_code
#         template = link.response_schema
#         template.update({'description': response_code_messages[status]})
#         res = {status: template}
#         res.update(link.error_status_codes)
#         return res
