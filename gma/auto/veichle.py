#!/usr/bin/env python
#!/usr/bin/env python
import httplib

s = httplib.HTTPConnection('www.gcv4.net');
s.request('GET','/index/veichle/schedule/');
with open('cron.log','a') as f:
    f.write('veichle_action: '+str(s.getresponse().status)+'\n');
s.close();
