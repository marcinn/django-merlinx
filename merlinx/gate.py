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
        return ''.join(self.items())


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

    def __init__(self, agent, affiliate, gate='ep3', searchtype=None, baseurl=None):
        self.agent = agent
        self.affiliate = affiliate
        self.gate = gate
        self.searchtype = searchtype
        self.baseurl = baseurl

    def fetch(self, parts=None, plain=False, **opts):
        """
        returns PartialGateResult or StringGateResult instance
        """
        params = {
                'gate': self.gate,
                'rnd': random.randint(1, 100000),
                }
        if parts:
            params['gateparts'] = ','.join(parts)
        
        url  = '%s/%s/%s/%s?%s' % (self.IBEURL, self.agent, self.affiliate,
                self.searchtype or '', urllib.urlencode(params))
                       
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
            parts[pname] = content[30:plen+30]
            content = content[plen+30:]
        return parts


class Gate(object):
    """
    MerlinX Gate integreation API
    """

    def __init__(self, client):
        """
        instantiate Gate API with specified client instance
        """
        self.client = client

    def search(self):
        pass

    def search_hotels(self):
        pass

