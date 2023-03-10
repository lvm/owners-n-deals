from django.http import JsonResponse

from backend.utils.helpers import simple_serializer


class JSONResponseMixin:
    def render_to_json_response(self, context, **response_kwargs):
        response_kwargs.update({"safe": False})
        return JsonResponse(self.get_data(context), **response_kwargs)

    def get_data(self, context):
        return simple_serializer(context)
