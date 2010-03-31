from django_widgets import Widget
from merlinx.plain import simple_api
from django.conf import settings

merlinx = simple_api(settings.MERLINX_AGENT_ID,
        settings.MERLINX_AFFILIATE)


class MerlinXQuery(Widget):
    def get_context(self, value, options):
        filter_args = dict(zip(map(str, options),
            options.values()))
        return {'result': merlinx.filter(**filter_args).result,}
