#!/usr/bin/env python
import httplib

s = httplib.HTTPConnection('www.gcv4.net');
s.request('GET','/index/npc/action/');
with open('cron.log','a') as f:
    f.write('npc_action: '+str(s.getresponse().status)+'\n');
s.close();
