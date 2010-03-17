from django.shortcuts import render_to_response
from django.template import RequestContext
from merlinx.gate import simple_gate
from merlinx import settings
import cgi

def _parse_gate_request(gate, request):
    params = request.GET.getlist('%s[]' % gate.ns)

    gate_params = {}
    for gate_rq in params:
        if gate_rq[1:]=='?':
            gate_rq = gate_rq[1:]
        gate_params.update(dict([(str(k),v[0]) for k, v in cgi.parse_qs(gate_rq).items()]))
    return gate_params


def generic_gate(request, method, template_name=None):
    gate = simple_gate(settings.AGENT_ID, settings.AFFILIATE)
    gate_params = _parse_gate_request(gate, request)

    ctx = {'gate': getattr(gate, method)(**gate_params),}

    return render_to_response(template_name or 'merlinx/gate/simple.html',
        context_instance=RequestContext(request, ctx))


def gate_hotels(request, **kw):
    return generic_gate(request, 'search_hotels', **kw)


def validate(request, template_name=None, gate=None):
    gate = gate or simple_gate(settings.AGENT_ID, settings.AFFILIATE)
    gate_params = _parse_gate_request(gate, request)
    ctx = {'gate_validation': gate.validate(gate_params)}
    return render_to_response(template_name or 'merlinx/gate/validate.html',
            RequestContext(request, ctx))
