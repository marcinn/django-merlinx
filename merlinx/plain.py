import re
from client import EP3Client


def parse_response(response):
    m = re.search(r'\n(SF@.+?)\n(.+?)\n', response, re.MULTILINE + re.DOTALL)
    if not m:
        raise ValueError('Invalid response')
    
    search_query = dict(zip(m.group(1).split('@')[1:], 
        m.group(2).split('@')[1:]))

    m = re.search(r'\n(V@.+?)\n(.+)\nJS\n', response, re.MULTILINE + re.DOTALL)
    result = []
    if m:
        cols = m.group(1).split('@')[1:]
        s = m.group(2)
        lines = [line.split('@') for line in s.split('\n')]
        for line in lines:
            if line[0]:
                break
            result.append(dict(zip(cols, line[1:])))
    return PlainResult(query=search_query, items=result)


class PlainResult(object):
    def __init__(self, **kwargs):
        self.query = kwargs.get('query', {})
        self.items = kwargs.get('items', [])
        self.page = None

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, k):
        return self.items[k]


class Query(object):

    def __init__(self, client):
        self.client = client
        self._args = {}
        self._result = None

    def filter(self, **kwargs):
        q = Query(self.client)
        q._args.update(self._args)
        q._args.update(kwargs)
        return q

    def __iter__(self):
        return self.result.__iter__()

    @property
    def result(self):
        if not self._result:
            self._result = parse_response(self.client.fetch(plain=True,
                **self._args))
        return self._result


class Plain(object):
    """
    MerlinX API
    """

    def __init__(self, client):
        self.client = client
        self.query = Query(client)

    def filter(self, **kwargs):
        return self.query.filter(**kwargs)


def simple_api(agent, affiliate, ns='ep3'):
    client = EP3Client(agent, affiliate, ns)
    plain = Plain(client)
    return plain


