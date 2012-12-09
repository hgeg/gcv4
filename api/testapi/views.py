#-*- coding: cp1254 -*-
# Create your views here.
from django.http import HttpResponseRedirect
from django.http import HttpResponse

def tasks(request):
    #WARNING: method stub.
    data = '{"data":[{"p":"alicanblbl","g":"saç kestirmece","l":"ankara", "t":"18:00","c":1,"k":2,"h":1},{"p":"alicanblbl","g":"evi yık","l":"ev", "t":"23:00","c":0,"k":4,"h":0},{"p":"alicanblbl","g":"web debug","l":"ofis", "t":"09:00","c":11,"k":4,"h":0}],"error":0}'
    return HttpResponse(data,mimetype='application/json')
