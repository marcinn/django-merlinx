import urllib
import random


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

        if plain and parts:
            raise ArgumentError('Cannot mix plain and parts arguments')

        if parts:
            params['gateparts'] = ','.join(parts)

        if plain:
            params['ep3_plaindata'] = 1

        params2 = dict([(k,v.encode('utf-8', 'ignore')) for k, v in params.items() if isinstance(v,unicode)])
        params.update(params2)
        
        if searchtype:
            url  = '%s/%s/%s/%s/?%s' % (self.IBEURL, self.agent, self.affiliate,
                    searchtype or '', urllib.unquote(urllib.urlencode(params)))
        else:
            url  = '%s/%s/%s/?%s' % (self.IBEURL, self.agent, self.affiliate,
                    urllib.unquote(urllib.urlencode(params)))

        f = urllib.urlopen(url)
        return f.read()

