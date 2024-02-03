import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList

class SrcJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    object_label_plural = 'objects'

    def render(self, data, media_type=None, renderer_context=None):
        if renderer_context:
            view = renderer_context['view']
            if view.request.method == 'DELETE':
                return status.HTTP_200_OK


        if isinstance(data, ReturnList):
            _data = json.loads(
                super(SrcJSONRenderer, self).render(data).decode('utf-8')
            )

            return json.dumps({
                self.object_label_plural: _data
            })

        else:
            errors = data.get('errors', None)

            if errors is not None:
                return super(SrcJSONRenderer, self).render(data)

            return json.dumps({
                self.object_label: data
            })
