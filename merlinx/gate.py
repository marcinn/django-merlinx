"""
MerlinX Gate integration module
Author: Marcin Nowak (marcin.j.nowak@gmail.com)
License: BSD
"""

import re
from client import EP3Client

def parse_response(response):
    """
    parse returned content
    returns dict of parts
    """
    parts = {}
    while response:
        plen, pname = int(response[:10]), response[10:30].strip()
        parts[pname] = response[30:plen+30].decode('utf8')
        response = response[plen+30:]
    return parts


class PartialResult(dict):
    """
    class that represents partial result
    """
    def __unicode__(self):
        return u''.join(self.values())


class StringResult(str):
    """
    class that represents string result
    """
    pass


class SimpleGate(object):
    """
    MerlinX Gate simple integreation API
    """

    default_parts = ['configcss', 'headercss', 'headerjs', 'content', 'menu', 'footer']

    def __init__(self, client):
        """
        instantiate Gate API with specified client instance
        """
        self.client = client
        self.stylesheets = ''
        self.javascripts = ''
        self.parts = {}

    def _search(self, type, **opts):
        parts = parse_response(self.client.fetch(searchtype=type,
            parts=self.default_parts + ['searchform'], **opts))
        self.stylesheets = parts['headercss']
        self.javascripts = parts['headerjs']
        self.parts = parts
        return self

    def search_tours(self, **opts):
        return self._search('rr', **opts)

    def search_hotels(self, **opts):
        return self._search('nh', **opts)

    def search_complete(self, **opts):
        return self._search('pa', **opts)

    def get_all(self):
        return u''.join(self.parts.values())

    def validate(self, opts):
        return self.client.fetch(**opts)

    def __getattr__(self, key):
        return self.parts.get(key)

    @property
    def ns(self):
        return self.client.gate

    @property
    def step(self):
        return self.parts.get('step', 1)



def simple_gate(agent, affiliate, ns='ep3'):
    client = EP3Client(agent, affiliate, ns)
    gate = SimpleGate(client)
    return gate


