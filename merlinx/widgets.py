from django_widgets import Widget
from merlinx.plain import simple_api
from django.conf import settings

merlinx = simple_api(settings.MERLINX_AGENT_ID,
        settings.MERLINX_AFFILIATE)


class MerlinXQuery(Widget):
    def get_context(self, value, options):
        return {'result': merlinx.filter(**options).result,}
