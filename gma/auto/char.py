#!/usr/bin/env python
import httplib

s = httplib.HTTPConnection('www.gcv4.net');
s.request('GET','/index/chars/handle');
with open('cron.log','a') as f:
    f.write('char_action: '+str(s.getresponse().status)+'\n');
s.close();
