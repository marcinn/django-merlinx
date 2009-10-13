import urllib
import random

class PartialGateResult(dict):
    def __unicode__(self):
        return ''.join(self.items())

    def __getattr__(self, key):
        return self[key]

    @property
    def javascripts(self):
        return self.headerjs

    @property
    def stylesheets(self):
        return self.headercss


class StringGateResult(str):
    pass



class EP3Gate(object):

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
            return StringGateResult(contents)   

        return PartialGateResult(self._parse_parts(contents))

    def _parse_parts(self, content):
        parts = {}
        while content:
            plen, pname = int(content[:10]), content[10:30].strip()
            parts[pname] = content[30:plen+30]
            content = content[plen+30:]
        return parts



if __name__ == '__main__':

    gate = EP3Gate(4078, 'test')
    r = gate.fetch()
    print r.stylesheets

