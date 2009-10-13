from django.shortcuts import render_to_response
from django.template import RequestContext
from merlinx.gate import simple_gate
from merlinx import settings
import cgi

def generic_gate(request, method, template_name=None):
    gate = simple_gate(settings.AGENT_ID, settings.AFFILIATE)

    gate_rq = request.GET.get('%s[]' % gate.ns)
    if gate_rq:
        gate_rq = gate_rq[1:]
        gate_params = dict([(str(k),v[0]) for k, v in cgi.parse_qs(gate_rq).items()])
    else:
        gate_params = {}

    ctx = {'gate': getattr(gate, method)(**gate_params),}

    return render_to_response(template_name or 'merlinx/gate/simple.html',
        context_instance=RequestContext(request, ctx))

def gate_hotels(request, **kw):
    return generic_gate(request, 'search_hotels', **kw)

