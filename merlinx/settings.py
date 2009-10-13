from django.conf import settings

try:
    from netwizard.registry.config import DatabaseRegistryConfig
    config = DatabaseRegistryConfig('merlinx.gate.config')
except ImportError:
    config = {}


AGENT_ID = getattr(settings, 'MERLINX_AGENT_ID', config.get('agent'))
AFFILIATE = getattr(settings, 'MERLINX_AFFILIATE', config.get('affiliate'))


