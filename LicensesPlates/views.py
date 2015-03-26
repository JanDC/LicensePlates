from django.http import HttpResponse
from django.template import RequestContext, loader
from PlateReader import PlateReader
import json as libjson


def home(request):
    plate_reader = PlateReader()
    alpr_json, alpr_error = plate_reader.alpr_json_results()
    template = loader.get_template('home.html')
    results = alpr_json.get('results')
    context = RequestContext(request, {'json': alpr_json, 'error': alpr_error, 'results': results})
    return HttpResponse(template._render(context))