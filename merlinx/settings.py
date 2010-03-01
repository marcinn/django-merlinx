from django.conf import settings

try:
    import registry
    config = registry.open('merlinx.gate.config')
except ImportError:
    config = {}


AGENT_ID = getattr(settings, 'MERLINX_AGENT_ID', config.get('agent'))
AFFILIATE = getattr(settings, 'MERLINX_AFFILIATE', config.get('affiliate'))


