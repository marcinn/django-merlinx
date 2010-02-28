"""
MerlinX Gate integration module
Author: Marcin Nowak (marcin.j.nowak@gmail.com)
License: BSD
"""

import urllib
import random


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



class EP3Client(object):
    """
    EP3 client class
    """

    IBEURL = 'http://ibe01.merlinx.pl/easypax3/agent'

    def __init__(self, agent, affiliate, gate, baseurl=None):
        self.agent = agent
        self.affiliate = affiliate
        self.gate = gate
        self.baseurl = baseurl

    def fetch(self, parts=None, plain=False, searchtype=None, **params):
        """
        returns PartialGateResult or StringGateResult instance
        """
        params.update({
                'gate': self.gate,
                'rnd': random.randint(1, 100000),
                })
        if parts:
            params['gateparts'] = ','.join(parts)
        
        url  = '%s/%s/%s/%s?%s' % (self.IBEURL, self.agent, self.affiliate,
                searchtype or '', urllib.unquote(urllib.urlencode(params)))

        f = urllib.urlopen(url)
        contents = f.read()

        if not parts:
            return StringResult(contents)   

        return PartialResult(self._parse_parts(contents))

    def _parse_parts(self, content):
        """
        parse returned content
        returns dict of parts
        """
        parts = {}
        while content:
            plen, pname = int(content[:10]), content[10:30].strip()
            parts[pname] = content[30:plen+30].decode('utf8')
            content = content[plen+30:]
        return parts


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
        parts = self.client.fetch(searchtype=type, parts=self.default_parts + ['searchform'], **opts)
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

