#-*- coding: cp1254 -*-
#TODO: add notification when ibox opened
#PENDING: Use proper states,
#PENDING: Implement long-polling


from __future__ import division
import datetime
import traceback
from django.contrib import *
from gma.game.models import *
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from random import randint
from itertools import chain
from django.core.mail import send_mail
from time import sleep
import sys

#helper methods:
def sysmsg(box,msg):
        box.message_box = box.message_box + msg + '\n'
        if box.message_box.count('\n')>9:
            box.message_box= "".join(box.message_box.splitlines(True)[1:])
        box.save()

def cs484(request):
    return render_to_response('cs484.html')

def gettime():    
    today=(datetime.datetime.today()).strftime("%d %m %Y %H")
    todaylist=today.split(" ")
    t_month=""
    Ch_year=""
    days_ch=""
    hours_approx=""
    if todaylist[1] == '01':
        t_month='Melian'
        days_ch=todaylist[0]
    elif todaylist[1] == '02':
        t_month='Melian'
        days_ch=str(int(todaylist[0])+31)
    elif todaylist[1] == '03':
        t_month='Melian'
        days_ch=str(int(todaylist[0])+60)
    elif todaylist[1] == '04':
        t_month='Yaestus'
        days_ch=todaylist[0]
    elif todaylist[1] == '05':
        t_month='Yaestus'
        days_ch=str(int(todaylist[0])+30)
    elif todaylist[1] == '06':
        t_month='Yaestus'
        days_ch=str(int(todaylist[0])+61)
    elif todaylist[1] == '07':
        t_month='Illia'
        days_ch=todaylist[0]
    elif todaylist[1] == '08':
        t_month='Illia'
        days_ch=str(int(todaylist[0])+31)
    elif todaylist[1] == '09':
        t_month='Illia'
        days_ch=str(int(todaylist[0])+61)
    elif todaylist[1] == '10':
        t_month='Frostus'
        days_ch=todaylist[0]
    elif todaylist[1] == '11':
        t_month='Frostus'
        days_ch=str(int(todaylist[0])+31)
    elif todaylist[1] == '12':
        t_month='Frostus'
        days_ch=str(int(todaylist[0])+61)
    Ch_year="2E"+str(int(todaylist[2])-1475)
    
    if   todaylist[3] in ['00','01','02']: hours_approx='Midnight'
    elif todaylist[3] in ['03','04','05']: hours_approx='Dusk'
    elif todaylist[3] in ['06','07','08']: hours_approx='Morning'
    elif todaylist[3] in ['09','10','11']: hours_approx='Late Morning'
    elif todaylist[3] in ['12','13','14']: hours_approx='Noon'
    elif todaylist[3] in ['15','16','17']: hours_approx='Afternoon'
    elif todaylist[3] in ['18','19','20']: hours_approx='Evening'
    elif todaylist[3] in ['21','22','23']: hours_approx='Night'
    
    today_h=Ch_year+" "+days_ch+" "+t_month+", "+hours_approx
    return (today_h,hours_approx)
    
def rule110(request,iters=255):
    rules = {u'\u2584\u2584\u2584':u' ',u'\u2584\u2584 ':u'\u2584',u'\u2584 \u2584':u'\u2584',u'\u2584  ':u' ',u' \u2584\u2584':u'\u2584',u' \u2584 ':u'\u2584',u'  \u2584':u'\u2584',u'   ':u' '}
    iter = 100000 if int(iters)>100000 else int(iters) if int(iters)>0 else 50
    line = (iter*' ')+u'\u2584'
    temp = ''  
    data =  line + '\n'
    for e in xrange(0,iter):
        line = ' '+line+' '
        for e in [line[i:i+3] for i in xrange(0,len(line))][:-2]:
            temp= temp+rules[e]
        data += temp+"\n"
        line=temp
        temp=''
    return HttpResponse('<html><head><title>I accidently a whole TM!</title></head><body><pre style="font-family: courier, monospace;font-size:6px;line-height:55%;">'+data+'</pre></body></html>')
                                                                                                                   
def construction(request):
    string = '''<html>
                    <head>
                        <title>Under Construction</title>
                    </head>
            <body style="font-family:Verdana;">
                <h2 align="center">Under Construction</h2>
                <div id="version" style="position: absolute; left: 52%; width:320px; margin-left:-160px; top:50px; font-family: Verdana, Arial, Helvetica, sans-serif;color: black; font-size: 12px;">
                    <span>
                           gcv4 v0.7.5.1 alpha 
                       </span>
                    <span>
                           | <a style="text-decoration: none;color: black;font-weight:bold;" href="http://gcv4.net/project/">project page</a>
                    </span>
                    <span>
                        | <a style="text-decoration: none;color: black;font-weight:bold;" href="http://gcv4.net/personal/">about</a>
                    </span>
                </div>
            </body>
                </html>'''
    return HttpResponse(string)


def project_page(request):
    string = '''<html>
                    <head>
                        <title>gcv4 project page</title>
                    </head>
                    <frameset>
                        <frame src="http://sites.google.com/site/alicanblbl/">
                    </frameset>
                </html>'''
    return HttpResponse(string)
    
def personal_page(request):
    string = '''<html>
                    <head>
                        <title>About me</title>
                    </head>
                    <frameset>
                        <frame src="http://ug.bcc.bilkent.edu.tr/~a_bulbul/">
                    </frameset>
                </html>'''
    return HttpResponse(string)
    
def rps_page(request):
    string = '''<html>
                    <head>
                        <title>Rock-Paper-Scissors</title>
                    </head>
                    <frameset>
                        <frame src="http://663517.appspot.com">
                    </frameset>
                </html>'''
    return HttpResponse(string)   
    
#login
def login(request):
    usr = request.POST["user"]
    pas = request.POST["pass"]
    user = auth.authenticate(username=usr, password=pas)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            UserProfile.objects.get(user=user).set_session_key(request.session.session_key)
            return HttpResponseRedirect("/index/")
        else:
            return render_to_response("login.html",{'message':'User is not activated'})
    else:
        return render_to_response("login.html",{'message':'Invalid username or password'})
#login redirection
def alogin(request):
#    usr = "ggm"
#    pas = "ggm"
#    user = auth.authenticate(username=usr, password=pas)
#    auth.login(request, user)
#    return HttpResponseRedirect('/index/')
    return render_to_response('login.html') 
 
#register
def register(request):
    usr = request.POST["user"]
    pas = request.POST["pass"]
    eml = request.POST["email"]
    
    #send_mail('Activation', 'The user %s waits for activation.'%usr, eml, ['alicanblbl@gmail.com'], fail_silently=True)
    aUser = User.objects.create_user(usr,eml,pas)
    aUser.is_active=False
    aUser.save()
    try:
        aUA = UserProfile.objects.create(user = aUser)
        aUA.save()
    except:
        return render_to_response("register.html",{'message':'This username exists.'})

    return render_to_response("login.html",{'message':'Your activation will be processed shortly...'})
    
#register redirection
def aregister(request):
    return render_to_response("register.html")

    
@login_required (redirect_field_name='')
def logout(request):
    if request.user.is_authenticated:
       auth.logout(request)
    return HttpResponseRedirect("/index/")

@login_required (redirect_field_name='')
def create_char(request):
    return render_to_response("create.html")

@login_required (redirect_field_name='')
def save_char(request):
    name = request.POST["name"]
    race = request.POST["race"]
    sex = request.POST["gender"]
    
    att1 = request.POST["attack1"]
    att2 = request.POST["attack2"]
    
    def1 = request.POST["defence1"]
    def2 = request.POST["defence2"]
    
    prd1 = request.POST["productive1"]
    prd2 = request.POST["productive2"]
    prd3 = request.POST["productive3"]
    
    hrv = request.POST["harvest"]
    
    msc1 = request.POST["misc1"]
    msc2 = request.POST["misc2"]
    msc3 = request.POST["misc3"]
    msc4 = request.POST["misc4"]
    
    flw1 = request.POST["flaw1"]
    flw2 = request.POST["flaw2"]
    
    trt1 = request.POST["trait1"]
    trt2 = request.POST["trait2"]
    
    hair = request.POST["hair"]
    face = request.POST["face"]
    beard = request.POST["beard"]
    
    str = request.POST["str"]
    int = request.POST["int"]
    dex = request.POST["dex"]
    wis = request.POST["wis"]
    sta = request.POST["sta"]
    luk = request.POST["luk"]
    
    stats = (str,int,dex,wis,sta,luk)
    appereance = (hair,face,beard)
    attacks = (att1,att2)
    defences = (def1,def2)
    productives = (prd1,prd2,prd3)
    miscs = (msc1,msc2,msc3,msc4)
    perks = (flw1,flw2,trt1,trt2)
    
    char = Character.init(request,name,race,sex,stats,appereance,attacks,defences,productives,hrv,miscs,perks)
    
    return HttpResponseRedirect("/index/")

 
@login_required (redirect_field_name='')
def notify(request):
    profile = UserProfile.objects.get(user=request.user)
    if profile.messages != '':
        messages = profile.messages
        profile.messages = ''
        profile.save()
        return HttpResponse(messages)
    else: return HttpResponse("null")


@login_required (redirect_field_name='')
def panel(request,tab=1):
    char = Character.objects.get(user=request.user)
    tabs=('char','skill','item','spell')
    try:
        return render_to_response("cpanel.html",{'tab':tabs[int(tab)-1]})
    except Character.DoesNotExist:
        return render_to_response("create.html")
    
    
@login_required (redirect_field_name='')
def char_panel(request):
    char = Character.objects.get(user=request.user)
    try:
        return render_to_response("char.html",char.return_all())
    except Character.DoesNotExist:
        return render_to_response("create.html")

@login_required (redirect_field_name='')
def shout(request):
    myself = Character.objects.get(user=request.user)
    if myself.state >-1:
        ashout=request.POST['shouted']
        if ashout=='': 
            if myself.counter < datetime.datetime.now():
                prd('render%d'%myself.current_place,simplejson.dumps({'action':'shout','id':myself.id,'data':ashout}))
                myself.shoutbox = ''
                myself.save()
            return HttpResponse()
        else: 
            prd('render%d'%myself.current_place,simplejson.dumps({'action':'shout','id':myself.id,'data':ashout}))
        if ashout[0] == '*':
            magi = ashout[1:]
            try: myself.readyspell = myself.spellbook.get(word=magi)
            except: return HttpResponse(status=200)
            myself.shoutbox = magi
            myself.counter = datetime.datetime.now() + datetime.timedelta(seconds=6)  
            prd('render%d'%myself.current_place,simplejson.dumps({'action':'shout','id':myself.id,'data':magi}))
        elif ashout =='.*':
            print "madafaak"
            try:
                print "zadafaak"
                attack(request,'s',myself.id,myself.id)
                print "kadafaak"
            except: return HttpResponse(status=200)
        else:
            myself.shoutbox = ashout
            myself.counter = datetime.datetime.now() + datetime.timedelta(seconds=3)  
            myself.cgrs()
    return HttpResponse(status=200)

@login_required (redirect_field_name='')
def relocate(request):
    myself = Character.objects.get(user=request.user)
    if myself.state in [0,-1]:
        myself.action = "move"
        myself.save()
    return HttpResponse(status=200)

@login_required (redirect_field_name='')
def rest(request):
    myself = Character.objects.get(user=request.user)
    if myself.state==0:
        myself.action = 'rest' if myself.action=='idle' else 'idle'
        myself.save()
        prd('render%d'%myself.current_place,simplejson.dumps({'action':'put','data':myself.render(myself.current_place,myself.id,myself.state),'id':myself.id}))
    return HttpResponse(status=200)
 
@login_required (redirect_field_name='')
def skill_panel(request):
    char = Character.objects.get(user=request.user)
    try:
        return render_to_response("skill.html",{'skills':char.return_skills()})
    except Character.DoesNotExist:
        return render_to_response("create.html")

def edit_blueprint(request):
    materials = Item.objects.filter(typeclass__in=['material','tool']).values('name').distinct() 
    return render_to_response("blueprint_editor.html",{'materials':materials,"cells":Place.objects.all(),'items':Item.objects.order_by('name').filter(~Q(type='blueprint')).values('name').distinct()})

def save_blueprint(request):
    name=request.POST["name"]
    value=request.POST["value"]
    number=request.POST["number"]
    cell=request.POST["cells"]
    skill=request.POST["skill"]
    crafted=request.POST["crafted"]
    items = str({request.POST["i1"]:int(request.POST["c1"]),request.POST["i2"]:int(request.POST["c2"]),request.POST["i3"]:int(request.POST["c3"]),request.POST["i4"]:int(request.POST["c4"]),request.POST["i5"]:int(request.POST["c5"]),'result':int(number)})
    bp = Blueprint.objects.create(name=name,type='item',category='blueprint',typeclass='document',subtype=skill,value=value,power=0,x=randint(100,550),y=randint(330,390),marked=False,h=25,w=50,DP=99999,a_maxdp=999999,req_skill_type=skill,req_skill_amount=int(value)+int(number)//2,materials=items,item=Item.objects.filter(name=crafted)[0])
    bp.save()
    Place.objects.get(id=cell).people.add(bp)
    return HttpResponse('Succesful!');

def edit_cell(request):
    return render_to_response("celleditor.html",{"cells":Place.objects.all()})

def save_cell(request):
    name=request.POST["name"]
    category=request.POST["group"]
    p=Place.objects.create(name=name,category=category)
    lnames = ['linksn','linkss','linkse','linksw']
    links =[]
    for link in lnames:
        try: links.append(request.POST[link])
        except: pass
    for link in links:
        try:p.connection.add(Place.objects.get(name=link))
        except: pass
    p.save()
    return HttpResponseRedirect("/index/")
    
@login_required (redirect_field_name='')
def edit_item(request):
    return render_to_response("itemeditor.html",{'cells':Place.objects.all()})
    
@login_required (redirect_field_name='')
def save_item(request):
    name=request.POST["name"]
    category=request.POST["category"]
    value=request.POST["value"]
    wx,hx=request.POST["size"].split()
    power=request.POST["power"]
    number=request.POST["number"]
    cell=request.POST["cells"]
    #Item classification := [subcategory] [category] | NONE [category]
    cat,typec,sub = category.split(' ')
    p=Place.objects.get(name=cell)
    if not typec == 'material':
        for e in xrange(0,int(number)):
            i=Item.objects.create(name=name,type='item',category=cat,typeclass=typec,subtype=sub,value=value,power=power,x=randint(100,550),y=randint(330,390),marked=False,h=27,w=50,DP=10000,a_maxdp=10000)
            p.people.add(i)
    else:
        i=Item.objects.create(name=name,type='item',category=cat,typeclass=typec,subtype=sub,value=value,power=power,x=randint(100,550),y=randint(330,390),marked=False,h=hx,w=wx,DP=number,a_maxdp=number)
        i.save()
        p.people.add(i)
    return HttpResponseRedirect("/index/")
    
@login_required (redirect_field_name='')
def main_page(request):
    c=Character.objects.get(user=request.user)
    return HttpResponseRedirect("/index/")

def getlist_without_response(request,p_id): #TODO:get rid of unused parts
    up = UserProfile.objects.get(user=request.user).set_session_key(request.session.session_key)
    try: char=Character.objects.get(user=request.user)
    except: return render_to_response('render.html');
    cell=Place.objects.get(id=char.current_place)
    people=cell.people.all()
    real = people.filter(type__contains='char')
    data = '<img src="/index/files/blank.gif" onload="pageLoad();return false;">'
    data += ''.join([e.render(cell,char.id,char.state) for e in people])
    return unicode(data).replace('\n','').replace('    ','').replace('\'','&#39;')

def getlist_json(request):
    char=Character.objects.select_related().get(user=request.user)
    data = serializers.serialize('json', char)
    return HttpResponse(data)

def render_json(request):
    return render_to_response('json_test.html')

def getData(request,target=None):
   myself = Character.objects.get(user=request.user)
   if not target: target = myself
   to_json = {'action':'self','id':myself.id,'data':target.render(myself.current_place,myself.id,myself.state)}
   return simplejson.dumps(to_json)

@login_required (redirect_field_name='')
def processPosInfo(request,x,y):
    myself = Character.objects.get(user=request.user)
    place = Place.objects.get(id=myself.current_place)
    if myself.action=="idle": pass
    elif myself.action=="move":
        if myself.state in [0,-1]:
            if 600>int(x)>100: myself.x = int(x)
            else: myself.x = 100 if int(x)<100 else 600
            if (place.horizon+place.depth*2/3)>int(y)>place.horizon+50: myself.y = int(y)
            else: myself.y = place.horizon+50 if int(y)<place.horizon+50 else place.horizon+place.depth*2/3
            myself.action='idle';
            myself.save();
            prd('render%d'%myself.current_place,getData(request))
            return HttpResponse()
    elif myself.action=="place":
        item = myself.hand
        item.x = int(x)
        if (place.horizon+place.depth*2/3)>int(y)>place.horizon+50:
            item.y = int(y)
        else: 
            item.y = place.horizon+50 if int(y)<place.horizon+50 else place.horizon+place.depth*2/3
        item.in_use=False
        item.save()
        myself.hand = None
        prd('render%d'%myself.current_place,simplejson.dumps({'action':'put','data':item.render(myself.current_place,myself.id,myself.state)}))
        place.people.add(item)
    myself.action="idle"
    myself.save()
    place.save()
    return HttpResponse(status=200)
       
@login_required (redirect_field_name='')
def travel(request,cell):
    today_h,hours_approx=gettime()
    if hours_approx in ['Midnight','Night']: luminance=0.6
    elif hours_approx in ['Evening','Dusk']: luminance=0.3
    elif hours_approx in ['Morning','Adternoon']: luminance=0.2
    elif hours_approx in ['Late Morning','Afternoon']: luminance=0.1
    else: luminance=0.0 
    
    #fetch the character
    try: c=Character.objects.get(user=request.user)
    except Character.DoesNotExist: return render_to_response("create.html")
    p1=Place.objects.get(id=c.current_place)
    
    if c.action=="travel":
        now = datetime.datetime.now()
        then = c.time_left
        if now>=then: 
          print "nov>=then"
          return arrive(request)
        diff = then-now
        t_amount = int(diff.seconds)
        if t_amount<=0: 
          print "t_amount<=0"
          return arrive(request) #failsafe 
        p1=Place.objects.get(id=c.current_place)
        p2=Place.objects.get(id=c.destination_place)
        prd('render%d'%p1.id,simplejson.dumps({'action':'travel','destination':p2.id,'id':c.id}))
        return render_to_response("travel.html",{"current_time":hours_approx,"dest":p2,"current":p1,"today":today_h,'distance':t_amount})
    
    #basic check
    if c.current_place == cell:
        peole = getlist_without_response(request,p1.id)
        return render_to_response("render.html",{"current_time":hours_approx,"current":p1,"luminance":luminance,"lpercent":int(luminance*100),"today":today_h,"p_inner":peole,'state':c.state,'my_id':c.id})
    #fetch the destination
    try:
        p2=Place.objects.get(id=cell)
    except:
        peole = getlist_without_response(request,p1.id)
        return render_to_response("render.html",{"current_time":hours_approx,"current":p1,"luminance":luminance,"lpercent":int(luminance*100),"today":today_h,"p_inner":peole,'state':c.state,'my_id':c.id})
    #advanced check
    #if these two cells are connected
    if c.state>0:c.state=0 #set the character free
    try:
        try: distance = Path.objects.filter(cell0=p1).filter(cell1=p2)[0].distance
        except: distance = Path.objects.filter(cell0=p2).filter(cell1=p1)[0].distance
    except: distance = 100
    if p2 in p1.connection.all() and c.FP >= distance/100:
        if not c.travel_check(p2):
            return render(request)
        p1.people.remove(c)
        p1.save()
        c.destination_place=p2.id
        c.action = 'travel'
        c.use_skill('Athletics')
        t_amount = int(distance/c.get_skill('Athletics'))
        c.time_left = datetime.datetime.now() + datetime.timedelta(seconds=t_amount)
        c.cgrs()
        c.save()
        prd('render%d'%p1.id,simplejson.dumps({'action':'travel','destination':p2.id,'id':c.id}))
        return render_to_response("travel.html",{"current_time":hours_approx,"dest":p2,"current":p1,"today":today_h,'distance':t_amount})
    else: return render(request)
    
@login_required (redirect_field_name='')
def arrive(request):
    c=Character.objects.get(user=request.user)
    if c.time_left==None: 
        c.time_left=datetime.datetime.now()
        c.save()
    if c.action=="travel" and c.time_left<=datetime.datetime.now():
        p=Place.objects.get(id=c.destination_place)
        c.travel(p)
        p.save()
        if not 600>c.x>100: c.x = 100 if c.x<100 else 600
        if not (p.horizon+p.depth*2/3)>c.y>p.horizon+50: c.y = p.horizon+50 if c.y<p.horizon+50 else p.horizon+p.depth*2/3
        c.save()
        c.end_turn()
        c.cgrs()
    return render(request) 
    
@login_required (redirect_field_name='')
def render(request):
    user = UserProfile.objects.get(user=request.user)
    today_h,hours_approx=gettime()
    if hours_approx in ['Midnight','Night']: luminance=0.6
    elif hours_approx in ['Evening','Dusk']: luminance=0.3
    elif hours_approx in ['Morning','Adternoon']: luminance=0.2
    elif hours_approx in ['Late Morning','Afternoon']: luminance=0.1
    else: luminance=0.0
    try: c=Character.objects.get(user=request.user)
    except Character.DoesNotExist: return render_to_response("create.html")
    p2=Place.objects.get(id=c.current_place)
    if c.action=="travel":  
        p1=Place.objects.get(id=c.destination_place)
        now = datetime.datetime.now()
        then = c.time_left
        if now>=then: 
            return arrive(request)
        diff = then-now
        t_amount = int(diff.seconds)
        if t_amount<=0: return arrive(request) #failsafe 
        return render_to_response("travel.html",{"current_time":hours_approx,"current":p2,'dest':p1,"today":today_h,'distance':t_amount})
    peole = getlist_without_response(request,p2.id)
    if p2.category=='inner':
        try:
         if p2.veichle.is_veichle: visual = Gate.objects.get(route=p2.id).image
        except: visual = p2.name
    else: visual = p2.name
    return render_to_response("render.html",{"current_time":_(hours_approx),"luminance":luminance,"lpercent":int(luminance*100),"current":p2,"visual":visual,"my":c.name,'my_id':c.id,"today":today_h,'p_inner':peole,'state':c.state})

def getstatus(request):
    myself = Character.objects.get(user=request.user)
    if myself.action=='rest':
        if myself.a_maxfp<=myself.FP or myself.HP<=1: myself.action='idle'
        else:
            myself.FP+=100 if myself.a_maxfp>myself.FP else 0
            myself.HP-=1 if myself.FP % 400 == 0 else 0
        myself.save() 
    data = '''
<span class="verdana100FFFFFFtb">HP: </span><span class="red">%d/%d</span><br/>
<span class="verdana100FFFFFFtb">MP: </span><span class="blue">%d/%d</span><br/>
<span class="verdana100FFFFFFtb">FP: </span><span class="green">%d/%d</span><br/>    
    '''%(myself.HP,myself.a_maxhp,myself.MP,myself.a_maxmp,int(myself.FP/100),int(myself.a_maxfp/100))
    return HttpResponse(data)

def check_place(request,p_name,time):
    char=Character.objects.get(user=request.user)
    p = Place.objects.get(id=char.current_place).name
    today_h,hours_approx=gettime()
    if not p_name == p: return HttpResponse(status=410)
    if not hours_approx == time: return HttpResponse(hours_approx)
    return HttpResponse(status=204)

def handle_chars(request):
    char = Character.objects.get(user=request.user)
    if char.action=='rest':
        if char.a_maxfp<=char.FP or char.HP<=1: char.action='idle'
        else:
            char.FP+=11 if char.a_maxfp>char.FP else 0
            char.HP-=1 if char.FP % 40 == 0 else 0
        char.save() 
    now = datetime.datetime.now()
    if not char.shoutbox=='' and char.counter<now:
        char.shoutbox=''
        char.cgrs()
    if char.empty >=10:
        char.empty =3
        char.level +=1
        ua = UserProfile.objects.get(user=char.user)
        ua.messages = 'You have advanced to level %d!' %char.level
        prd('notification%d'%char.id)
        ua.save()

    if char.state==90 and char.counter<now:
        char.state=0
        char.cgrs()
    npcs = Character.objects.filter(type='npcChar').filter(current_place=char.current_place)
    for npc in npcs:
        if npc.action=='travel' and npc.time_left<now:
            npc.action='idle'
            npc.save()
            cell.save()  
        if npc.counter<now and (npc.shoutbox!='' or npc.state==90):
            npc.shoutbox=''
            if npc.state==90:npc.state=0
            npc.save()
            cell.save()
    return HttpResponse()

def getlist(request,p_id):
    try: 
        char=Character.objects.get(user=request.user)
    except: return HttpResponse(status=401)
    if (not int(char.current_place) == int(p_id)) or char.action=='travel':
        return HttpResponse("%d != %d "%(int(char.current_place),int(p_id)),status=4123)
    req=0 
    cell=Place.objects.get(id=char.current_place)
    #while char.rrs() and req<10:
    #    sleep(1)    
    #    req+=1
    now = datetime.datetime.now()
    if not char.shoutbox=='' and char.counter<now:
        char.shoutbox=''
        char.cgrs()
    if char.rrs():
        
        if char.empty >=10:
            char.empty =3
            char.level +=1
            ua = UserProfile.objects.get(user=char.user)
            ua.messages = 'You have advanced to level %d!' %char.level
            char.crs()
            ua.save()

        if char.state==90 and char.counter<now:
            char.state=0
            char.cgrs()
        npcs = cell.people.filter(type='npcChar')
        for gen in npcs:
            npc = gen.character
            if npc.action=='travel' and npc.time_left<now:
                npc.action='idle'
                npc.save()
                cell.save()  
            if npc.counter<now and (npc.shoutbox!='' or npc.state==90):
                npc.shoutbox=''
                if npc.state==90:npc.state=0
                npc.save()
                cell.save()  

        return HttpResponse(status=204)
    
    char.crs()
    people=cell.people.all()
    real = people.filter(type__contains='char')
    slist = "registered = " + str([int(e.id) for e in real]) + ";"
    rcount = str(len(real))
    data = '<img src="/index/files/blank.gif" onload="pageLoad();">'
    data += ''.join([e.render(cell,char.id,char.state) for e in people])
    if not char.message=='':   
        char.message=''
        char.save()
    return HttpResponse(unicode(data).replace('\n','').replace('    ','').replace('\t',''))

@login_required (redirect_field_name='')
def interact_return(request):
    myself = Character.objects.get(user=request.user)
    box = (InteractionBox.objects.filter(first=myself) or InteractionBox.objects.filter(second=myself)) or GenericBox.objects.filter(first=myself) or ContainerBox.objects.filter(first=myself)
    if(box[0].type=='iBox'):
        return interact(request,box[0].first.id,box[0].second.id)
    elif(box[0].type=='cBox'):
        return render_to_response('chest.html',{"inventory":myself.inventory.all(),'otherbox':box[0].second.items.all(),'d_id':box[0].second.id})
    else: return open_workbench(request,box[0].id)
    
        
@login_required (redirect_field_name='')
def interact(request,first,other):
    #try:
        myself = Character.objects.get(user=request.user)
        
        otherone = Character.objects.get(id=other)
        if otherone.x>600:
            firstone = Character.objects.get(id=other)
            otherone = Character.objects.get(id=first)
        else: firstone = Character.objects.get(id=first)
        place=Place.objects.get(id=firstone.current_place)
        
        if(firstone.state == 0 and otherone.state == 0):
            firstone.state=1
            otherone.state=1
            if(firstone.current_place==otherone.current_place):
                try:
                    user = UserProfile.objects.get(user=otherone.user)
                    user.messages = '%s has contacted you!'%(myself.name)
                    user.save() 
                except: pass
                iBox = InteractionBox.objects.create(name='%s and %s'%(firstone.name,otherone.name),type='iBox',first=firstone,second=otherone,current_place=firstone.current_place,x=otherone.x*0.77,y=otherone.y,w=121,h=110)
                firstone.x, firstone.y = otherone.x + otherone.w + 10, otherone.y
                iBox.save()
                firstone.save()
                otherone.save()
                place.people.remove(firstone)
                place.people.remove(otherone)
                place.people.add(iBox)
                prd('render%d'%place.id,simplejson.dumps({'action':'put','id1':firstone.id,'id2':otherone.id,'id':'iBox.*16#xuPC','data':iBox.render(place,myself.id,myself.state)}))
                prd('notification%d'%myself.id,'%s has contacted you.\n'%myself.name)
            else: return render_to_response('close.html')
        else:
                iBox = InteractionBox.objects.get(first=firstone)
        if(otherone.type=='char'):
            return render_to_response('interact.html',{'messages':iBox.message_box,'iid': iBox.id,"s1":myself.state-1,"s2":otherone.state-1,"inventory":myself.inventory.order_by('category'),"box":myself.share_box.all()})
        else:
            npc = NPC.objects.get(char=otherone)
            d = npc.disposition
            try: ddict = eval(d)
            except: ddict = {}
            try:
                dsp = ddict[myself.id]
            except:
                dsp = 20
                if myself.race==otherone.race: dsp+=10
                dsp += myself.get_skill('Merchantile')/4 + myself.get_skill('Merchantile')/8 + myself.a_luk-2 
                ddict[myself.id] = dsp
                npc.disposition = str(ddict)
            npc.save()

            return render_to_response('npcinteract.html',{'messages':iBox, "inventory":myself.inventory.all(),'balance':iBox.balance,'topics':NPC.objects.get(char=iBox.second).topics.all(),'otherbox':iBox.second.inventory.all(),'disposition':dsp})
    #except: return render_to_response('interact.html',{'messages':'An error occured','box':'An error ocuured'})
    
@login_required (redirect_field_name='')
def interrupt(request): 
    myself = Character.objects.get(user=request.user)
    if myself.state>-1:
        try:
            try:
                box = InteractionBox.objects.get(first=myself)
            except:
                box = InteractionBox.objects.get(second=myself)
        except: pass

        try:
            box = ContainerBox.objects.get(first=myself)
        except: pass

        try:
            box = GenericBox.objects.get(first=myself)
        except: pass
        firstone = box.first
        otherone = box.second
        pid = firstone.current_place
        place = Place.objects.get(id=pid)
        place.people.add(firstone)
        place.people.add(otherone)
        if not box==None:box.decompose()
        prd('render%d'%pid,simplejson.dumps({'action':'put','id':firstone.id,'data':firstone.render(place,myself.id,myself.state)}))
        prd('render%d'%pid,simplejson.dumps({'action':'put','id':otherone.id,'data':otherone.render(place,myself.id,myself.state)}))
    return render_to_response('close.html')

@login_required (redirect_field_name='')    
def other_box(request):
    myself = Character.objects.get(user=request.user)
    if myself.action=='complete':
        myself.action='idle'
        myself.save()
        return HttpResponse(status=204)
    try: 
        iBox = InteractionBox.objects.get(first=myself)
        items= iBox.second.share_box.all()
    except: 
        iBox =InteractionBox.objects.get(second=myself)
        items= iBox.first.share_box.all()
    
    data=''
    for item in items:
        data += '<span>'+item.get_name()+'</span><br/>'
    return HttpResponse(data)
    

@login_required (redirect_field_name='')
def exchange_signal(request):
    intact = 1
    ready = 2
    myself = Character.objects.get(user=request.user)
    try:
        try: 
            iBox = InteractionBox.objects.get(first=myself)
            other = iBox.second
        except: 
            iBox =InteractionBox.objects.get(second=myself)
            other = iBox.first
    except: 
        status = '<img src="/index/files/blank.gif" onload="end_session();"></img>'  
        return HttpResponse(status)
    if myself.state == ready and other.state == ready:
        status = '''<div id="wb_Text2" style="margin:0;padding:0;position:absolute;left:0px;top:0px;width:110px;height:14px;text-align:left;z-index:7;">
<font style="font-size:11px"  color="#00fa00" face="Arial"> You are ready! </font></div>
<div id="wb_Text1" style="margin:0;padding:0;position:absolute;left:2px;top:20px;width:90px;height:28px;text-align:left;z-index:8;">
<font style="font-size:11px" color="#00ff00" face="Arial">%s is ready!</font></div>'''%other.name

    elif myself.state == ready and other.state == intact:
        status = '''<div id="wb_Text2" style="margin:0;padding:0;position:absolute;left:0px;top:0px;width:110px;height:14px;text-align:left;z-index:7;">
<font style="font-size:11px"  color="#00fa00" face="Arial"> You are ready! </font></div>
<div id="wb_Text1" style="margin:0;padding:0;position:absolute;left:2px;top:20px;width:90px;height:28px;text-align:left;z-index:8;">
<font style="font-size:11px" color="#000000" face="Arial">Waiting for %s</font></div>'''%other.name

    elif myself.state == intact and other.state == ready:
        status = '''<div id="wb_Text2" style="margin:0;padding:0;position:absolute;left:0px;top:0px;width:110px;height:14px;text-align:left;z-index:7;">
<font style="font-size:11px"  color="#fa0000" face="Arial">You are not ready!</font></div>
<div id="wb_Text1" style="margin:0;padding:0;position:absolute;left:2px;top:20px;width:90px;height:28px;text-align:left;z-index:8;">
<font style="font-size:11px" color="#00fa00" face="Arial">%s is ready!</font></div>'''%other.name

    elif  myself.state == intact and other.state == intact:
        status = '''<div id="wb_Text2" style="margin:0;padding:0;position:absolute;left:0px;top:0px;width:110px;height:14px;text-align:left;z-index:7;">
<font style="font-size:11px"  color="#fa0000" face="Arial">You are not ready!</font></div>
<div id="wb_Text1" style="margin:0;padding:0;position:absolute;left:2px;top:20px;width:90px;height:28px;text-align:left;z-index:8;">
<font style="font-size:11px" color="#fa0000" face="Arial">%s is not ready!</font></div>'''%other.name
    else: status = '''<div id="wb_Text2" style="margin:0;padding:0;position:absolute;left:0px;top:0px;width:110px;height:14px;text-align:left;z-index:7;">
<font style="font-size:11px"  color="#fa0000" face="Arial">An Exception Occured %d %d</font></div>'''%(myself.state,other.state)
    return HttpResponse(status)

@login_required (redirect_field_name='')
def interact_action(request):
    #local constants
    intact = 1
    ready = 2
    #fetch the character
    myself = Character.objects.get(user=request.user)
    #find the current interaction box
    try: 
        iBox = InteractionBox.objects.get(first=myself)
        other = iBox.second
    except: 
        try:
            iBox =InteractionBox.objects.get(second=myself)
            other = iBox.first
        except:
            return render_to_response('interact.html')
    option = request.POST["benjamin"]
    option = option.strip()
    try: 
        item_id = request.POST["inventory"]
        item = Item.objects.get(id=item_id)
        try: amount = int(request.POST["amount"])
        except: amount = item.DP
        if option == 'Give':
            if item.category == 'edible':
                item.transfer(myself.inventory,myself.share_box,amount)
            else: 
                myself.inventory.remove(item)
                myself.share_box.add(item)
            s1 = False
    except: 
        try: 
            item_id = request.POST["mybox"]
            item = Item.objects.get(id=item_id)
            try: amount = int(request.POST["amount"])
            except: amount = item.DP
            if option == 'Take':
                if item.category == 'edible':
                    item.transfer(myself.share_box,myself.inventory,amount)
                else: 
                    myself.share_box.remove(item)
                    myself.inventory.add(item)
                s1 = False
        except:
            if option == 'Ready':
                if not other.state==ready: 
                    myself.action='waiting'
                myself.state = ready
                myself.save()
            elif option == 'Break':
                    myself.state = intact
                    myself.save()
            elif option == 'Confirm':
                  if myself.state == ready and other.state == ready and myself.action=='waiting':
                    for item in iBox.second.share_box.all():
                        iBox.second.share_box.remove(item)
                        iBox.first.inventory.add(item)
                    for item in iBox.first.share_box.all():
                        iBox.first.share_box.remove(item)
                        iBox.second.inventory.add(item)
                    myself.state = intact
                    myself.action = 'complete'
                    myself.save()
                    other.state = intact
                    other.action = 'complete'
                    other.save()
                    placing = 1 if iBox.first.id == myself.id else 2
            elif option == 'Interrupt': return interrupt(request)
    prd('box'+str(int(iBox.id)))
    prd('sgn'+str(int(iBox.id)))
    return render_to_response('interact.html',{'iid':iBox.id,"s1":myself.state-1,"s2":other.state-1,"inventory":myself.inventory.all(),'balance':iBox.balance,"box":myself.share_box.all()})

#TODO: Whole merchantile system should be revamped.
#    1. better usage of skills and disposition
#    2. regulations on escrows, items with no physical value
@login_required (redirect_field_name='')
def npc_interact_action(request):
    #fetch the character
    myself = Character.objects.get(user=request.user)
    #find the current interaction box
    iBox = InteractionBox.objects.get(first=myself)
    other = iBox.second
    npc = NPC.objects.get(char=other)
    ddict = eval(npc.disposition)
    dsp = int(ddict[myself.id])
    #set the places of the boxes
    other_box = other.inventory
    option = request.POST["benjamin"]
    option = option.strip()
    try:
        item_id = request.POST["inventory"]
        item = Item.objects.get(id=item_id)
        try: amount = int(request.POST["amount"])
        except: amount = item.DP
        if option == 'Give':
            item.transfer(myself.inventory,other_box,amount)
            if not item.marked:
                item.owner = other
                item.marked = True
            if item.type == 'bag' or (item.marked and item.owner==other): 
                    iBox.balance += item.value
            else: 
                    iBox.balance += (item.value*int(amount) if item.typeclass=="material" else item.value)*myself.use_skill('Merchantile')
    except: 
        try: 
            item_id = request.POST["otherbox"]
            item = Item.objects.get(id=item_id)
            try: amount = int(request.POST["amount"])
            except: amount = item.DP
            if option == 'Take':
                if not item.marked or item.owner == myself or item.owner == other or item.owner.state==-1:
                    item.transfer(other_box,myself.inventory,amount)
                    if item.type == 'bag' or (item.marked and item.owner==other):
                            iBox.balance -= item.value
                    else: 
                            iBox.balance -= (item.value*int(amount) if item.typeclass=="material" else item.value)*myself.use_skill('Merchantile')
        except:
            if option == 'Interrupt' and (iBox.balance>0 or (iBox.balance<=0 and other.bag.total()>=iBox.balance)):
                if iBox.balance>0:
                    other.bag.sub(iBox.balance//100,iBox.balance%100)
                    myself.bag.add(iBox.balance//100,iBox.balance%100)
                    ddict[myself.id] += iBox.balance/10
                elif iBox.balance<0:
                    myself.bag.sub(iBox.balance//100,iBox.balance%100)
                    other.bag.add(iBox.balance//100,iBox.balance%100)
                    ddict[myself.id] -= iBox.balance/10
                npc.disposition = str(ddict)
                npc.save()
                for item in other.inventory.all():
                    item.marked = True
                    item.owner = other
                    if item.type=='bag': other.bag.merge(item.moneybag)
                return interrupt(request)
            if other.bag.total()<iBox.balance:
                sysmsg(iBox,'%s: I cannot afford this transaction.'%other.name)
    iBox.save()       
    return render_to_response('npcinteract.html',{'messages':iBox.message_box, 'inventory':myself.inventory.all(),'balance':iBox.balance,'topics':NPC.objects.get(char=iBox.second).topics.all(),"otherbox":other_box.all(),'disposition':dsp})

   
@login_required (redirect_field_name='')#TODO: some possible glitches in money transaction. Also merchant skill seems exploitable by mass tweaking.
def tweak_balance(request,amount):
    #fetch the character
    myself = Character.objects.get(user=request.user)
    #find the current interaction box
    iBox = InteractionBox.objects.get(first=myself)
    other = iBox.second
    npc = NPC.objects.get(char=other)
    ddict = eval(npc.disposition)
    dsp = ddict[myself.id]
    other=iBox.second
    iBox.save()
    return HttpResponse(iBox.balance)  
    
@login_required (redirect_field_name='')
def show_inventory(request):
    myself = Character.objects.get(user=request.user)
    if myself.hand:
        myself.inventory.add(myself.hand)
        myself.hand = None
    inventory = myself.inventory.all()
    return render_to_response("inventory.html",{"inventory":inventory,'Volans':myself.bag.Volans, 'Orns':myself.bag.Orns,'state':myself.state})
    
@login_required (redirect_field_name='')
def item_action(request):
    char = Character.objects.get(user=request.user)
    inventory = char.inventory.all()
    try:
        item_id = request.POST["inventory"]
    except: return render_to_response("inventory.html",{"inventory":inventory,'Volans':char.bag.Volans, 'Orns':char.bag.Orns,'state':char.state})
    item = Item.objects.get(id=item_id)
    pressed = request.POST["Btn"]
    if pressed in ('Use', 'Equip', 'Pocket', 'Read', 'Write','Learn','Open'):
        if item.typeclass=='document':
            if item.category=='TheBook':
                return HttpResponse('{"action":"open", "data":%d,"id":%d}'%(231,item.id))
                return render_to_response("inventory.html",{"inventory":inventory, 'open':231, 'd_id':item.id})
            elif item.category=='blank':
                return HttpResponse('{"action":"open", "data":%d,"id":%d}'%(232,item.id))
                return render_to_response("inventory.html",{"inventory":inventory, 'open':232, 'd_id':item.id})
            elif item.category=='scroll':
                item.use(char)
            else:
                return HttpResponse('{"action":"open", "data":%d,"id":%d}'%(687,item.id))
                return render_to_response("inventory.html",{"inventory":inventory, 'open':687, 'd_id':item.id})
        elif item.type=='bag':
            char.bag.merge(item.moneybag)
            return HttpResponse('{"action":"pocket", "data":[%d,%d]}'%(char.bag.Volans,char.bag.Orns))
        elif item.type=='container':
            char.save()
            prd('render'+str(int(char.current_place)),getData(request))
            return HttpResponse('{"action":"open", "data":%d,"id":%d}'%(338,item.id))
            return render_to_response("inventory.html",{"inventory":inventory, 'open':338, 'd_id':item.id})
        elif item.type=='material':
            item.use(char)
            char.save()
            #prd('render'+str(int(char.current_place)),getData(request))
            if(item):
              return HttpResponse('{"action":"decrease", "data":%d}'%item.DP)
            else:
              return HttpResponse('{"action":"remove", "data":%d}'%item.id)
            return render_to_response('inventory.html',{'inventory':inventory, 'open':False, 'd_id':-1, 'Volans':char.bag.Volans, 'Orns':char.bag.Orns,'state':char.state})
        else:
            data,rid = item.use(char)
            char.save()
            prd('render'+str(int(char.current_place)),getData(request))
            if(data == ''):
              return HttpResponse('{"action":"remove", "data":%d}'%item.id)
            else:
              return HttpResponse('{"action":"replace", "data":"%s", "id":%d}'%(data,rid))

 
    elif pressed in('Mark','Unmark'):
        if item.marked:
            if item.owner == char or item.owner == None: 
                item.marked = False
                item.owner = None
        else:
            item.owner = char
            item.marked = True
        item.save()
        return HttpResponse('{"action":"rename", "data":"%s"}'%item.get_name())
     
    return render_to_response('inventory.html',{'inventory':inventory, 'open':False, 'd_id':-1, 'Volans':char.bag.Volans, 'Orns':char.bag.Orns,'state':char.state})
    
    
@login_required (redirect_field_name='')
def show_spellbook(request):
    myself = Character.objects.get(user=request.user)
    spellbook = myself.spellbook.all()
    return render_to_response("spellbook.html",{"spellbook":spellbook,'state':myself.state})
    
@login_required (redirect_field_name='')
def spell_action(request):
    char = Character.objects.get(user=request.user)
    inventory = char.inventory.all()
    try:
        item_id = request.POST["spells"]
    except: return render_to_response("inventory.html",{"inventory":inventory,'Volans':char.bag.Volans, 'Orns':char.bag.Orns,'state':char.state})
    item = Item.objects.get(id=item_id)
    pressed = request.POST["Btn"]
    if pressed in ('Use', 'Equip', 'Pocket', 'Read', 'Write') :
        if item.typeclass=='document':
            if item.category=='TheBook':
                return render_to_response("inventory.html",{"inventory":inventory, 'open':231, 'd_id':item.id})
            elif item.category=='blank':
                return render_to_response("inventory.html",{"inventory":inventory, 'open':232, 'd_id':item.id})
            else:
                return render_to_response("inventory.html",{"inventory":inventory, 'open':687, 'd_id':item.id})
        elif item.type=='bag':
            char.bag.merge(item.moneybag)
        else: 
            item.use(char)
            char.cgrs()
        
    elif pressed == "Toss":
        cell=Place.objects.get(id=char.current_place)
        char.inventory.remove(item)
        item.y=char.y+5
        item.x=char.x+randint(-10,10)
        item.w=50
        item.h=25
        item.in_use=False
        cell.people.add(item)
        
    elif pressed in('Mark','Unmark'):
        if item.marked:
            if item.owner == char or item.owner == None: 
                item.marked = False
                item.owner = None
        else:
            item.owner = char
            item.marked = True
    
    item.save()
    char.save()
    return render_to_response('inventory.html',{'inventory':inventory, 'open':False, 'd_id':-1, 'Volans':char.bag.Volans, 'Orns':char.bag.Orns,'state':char.state})

@login_required (redirect_field_name='')
def harvest(request,h_id):
    mychar = Character.objects.get(user = request.user)
    harvest = Harvest.objects.get(id=h_id)
    result = harvest.start_harvest(mychar)
    try:count = mychar.inventory.filter(name=harvest.container.name)[0].DP
    except: count = 0
    if result[0]:
        return render_to_response('harvest.html',{'interval':result[1],'count':count,'message':'%s %s'%(harvest.handler,harvest.container.name),'name':harvest.container.name,'id':h_id})   
    else:
        if result[2]==0:
            return render_to_response('harvest.html',{'interval':-1,'count':count,'message':'No harvestable left!','name':harvest.container.name})   
        if result[2]==1:
            return render_to_response('harvest.html',{'interval':-1,'count':count,'message':'You don\'t have the right tool!','name':harvest.container.name})   
        if result[2]==2:
            return render_to_response('harvest.html',{'interval':-1,'count':count,'message':'You are exhausted!','name':harvest.container.name})   

def collect(request,h_id):
    mychar = Character.objects.get(user = request.user)
    harvest = Harvest.objects.get(id=h_id)
    result = harvest.start_harvest(mychar)
    item = mychar.inventory.filter(name=harvest.container.name)
    if len(item)>0:item=item[0]
    else: item=None
    if result[0]:
        if item:
            item.DP+=1
            item.save()
            count = item.DP
        else:    
            new = harvest.container.copy()
            new.save()
            mychar.inventory.add(new)
            count=1
        mychar.use_skill(harvest.handler)
        mychar.FP -=harvest.interval/4
        mychar.save()
        return render_to_response('harvest.html',{'interval':result[1],'count':count,'message':'%s %s'%(harvest.handler,harvest.container.name),'name':harvest.container.name,'id':h_id})   
    else:
        count = item.DP
        if result[2]==0:
            return render_to_response('harvest.html',{'interval':-1,'count':count,'message':'No harvestable left!','name':harvest.container.name})   
        if result[2]==1:
            return render_to_response('harvest.html',{'interval':-1,'count':count,'message':'You don\'t have the right tool!','name':harvest.container.name})   
        if result[2]==2:
            return render_to_response('harvest.html',{'interval':-1,'count':count,'message':'You are exhausted!','name':harvest.container.name})        

@login_required (redirect_field_name='')
def attack(request,action,first,other):
    myself = Character.objects.get(id=first)
    if first==other:
        other=myself
    else:
        other = Character.objects.get(id=other)
    if myself.current_place==other.current_place and other.state==0:
        if action=='s':
            if myself.readyspell: 
                es = myself.readyspell.parse(other,myself)
                myself.shoutbox=myself.readyspell.word
                myself.counter = datetime.datetime.now() + datetime.timedelta(seconds=6)  
                myself.save()
                if es=='': return HttpResponse()
                other.state=90
                other.counter = datetime.datetime.now() + datetime.timedelta(seconds=5)
                other.shoutbox='HP %s'%es
                prd('notification%d'%other.id,'%s casts %s. It hits your %s, causing %s HP effect.\n'%(myself.name, myself.readyspell.name,res[0], res[2]))
        elif action=='m':
            res = myself.attack(other)
            other.shoutbox='HP -%d'%res[2]
            other.counter = datetime.datetime.now() + datetime.timedelta(seconds=5)
            other.save()
            if(res[2]!=0.5):
              prd('notification%d'%myself.id,'%s %s your %s with %s, causing %s HP damage.\n'%(myself.name,res[3],res[0],res[1],res[2]))
            else:
              prd('notification%d'%myself.id,'%s swings %s, but misses.\n'%(myself.name,res[1]))
        other.save()
        myself.cgrs()
    return HttpResponse('%d %d %d %s'%(myself.current_place,other.current_place,other.state,action))

@login_required (redirect_field_name='')
def put_money(request):
    return render_to_response('money_amount.html',{'message':'Choose the amount:'})

@login_required (redirect_field_name='')
def return_money(request):
    mychar = Character.objects.get(user = request.user)
    try: volans = int(request.POST['volans'])
    except: volans = 0
    
    try: orns = int(request.POST['orns'])
    except: orns = 0
    
    if(volans <= mychar.bag.Volans and orns <= mychar.bag.Orns) and (volans >= 0 and orns >= 0)  and (volans is not 0 or orns is not 0):
        n = str(orns)+(' Orn'+('s' if orns is not 1 else '')) if volans is 0 else str(volans)+(' Volan'+('s' if volans is not 1 else '')) if orns is 0 else str(volans)+' Volan'+('s' if volans is not 1 else '')+' and '+ str(orns)+' Orn'+('s' if orns is not 1 else '')
        abag = MoneyBag.objects.create(Volans=volans,Orns=orns,x=0,y=0,name=n,type='bag',typeclass='bag',category='bag',value=100*volans+orns,DP=2,a_maxdp=2,h=25,w=40)
        abag.save()
        mychar.bag.sub(volans,orns)
        mychar.bag.save()
        mychar.inventory.add(abag)
        mychar.save()
        return HttpResponse('<img onload="parent.jQuery.fn.colorbox({width:\'350\', height:\'320\', iframe:true, href:\'/index/cpanel/3/\'});" src="/index/files/blank.gif">')
    elif volans is  0 and orns is  0: return HttpResponse('<img onload="parent.jQuery.fn.colorbox({width:\'350\', height:\'320\', iframe:true, href:\'/index/cpanel/3/\'});" src="/index/files/blank.gif">')
    else: return render_to_response('money_amount.html',{'message':'Invalid amount:'})

@login_required(redirect_field_name='')
def take_amount(request,i):
    char = Character.objects.get(user=request.user)
    try: amount = int(request.POST['amount'])
    except: amount = 0

    item = char.inventory.get(id=i)
    if amount>0:
        if amount < item.DP:
            new = item.copy()
            new.DP = amount
            new.save()
            item.DP -=amount
            item.save()
        if amount == item.DP:
            new = item
            char.inventory.remove(item)
        if char.hand: char.inventory.add(char.hand)
        char.hand = new
        char.action = 'place'
        char.save()
        return HttpResponse('<html><body onload="parent.jQuery.fn.colorbox.close();"></body></html>')
    else: return render_to_response('item_amount.html',{'message':'Invalid amount:','id':i})

@login_required(redirect_field_name='')
def choose_amount(request,i):
    item = Item.objects.get(id=i)
    char = Character.objects.get(user=request.user)
    if not item.typeclass=='material' or item.DP==1: 
        if char.hand: char.inventory.add(char.hand)
        char.hand = item
        char.inventory.remove(item)
        char.action="place"
        char.save()
        return HttpResponse('<html><head></head><body onload="parent.setAction(\'place\');parent.jQuery.fn.colorbox.close();"></img></body></html>')    
        
    return render_to_response('item_amount.html',{'message':'Choose the amount:','id':i})


login_required(redirect_field_name='')
def look_chest(request,c_id):
        myself = Character.objects.get(user=request.user)
        place=Place.objects.get(id=myself.current_place)
        if(myself.state == 0):
            otherone = Container.objects.get(id=c_id)
            try: ContainerBox.objects.get(first=myself).decompose()
            except: pass
            cBox = ContainerBox(name='cBox',type='cBox',first=myself,second=otherone,current_place=myself.current_place,x=0,y=0,w=30,h=30,image='wine and cheese')         
            cBox.save()
            myself.save()
        else:
                cBox = ContainerBox.objects.get(first=myself)
        return render_to_response('chest.html',{"inventory":myself.inventory.all(),'otherbox':cBox.second.items.all(),'d_id':cBox.second.id})

@login_required(redirect_field_name='')
def open_chest(request,c_id):
        myself = Character.objects.get(user=request.user)
        place=Place.objects.get(id=myself.current_place)
        if(myself.state == 0):
            otherone  = Container.objects.get(id=c_id)
            myself.state=26
            try: ContainerBox.objects.get(first=myself).decompose()
            except: pass
            cBox = ContainerBox(name='cBox',type='cBox',first=myself,second=otherone,current_place=myself.current_place,x=otherone.x,y=otherone.y,w=30,h=30,image='wine and cheese')              
            place.people.remove(myself)
            myself.x = otherone.x + 10
            myself.y = otherone.y - otherone.h/5+ myself.h/3
            place.people.remove(otherone)
            place.save()
            cBox.save()
            place.people.add(cBox)
            myself.save()
            prd('render%d'%myself.current_place,getData(request))
        else:
            cBox = ContainerBox.objects.get(first=myself)
        return render_to_response('chest.html',{"inventory":myself.inventory.all(),'otherbox':cBox.second.items.all(),'d_id':cBox.second.id,'m':True})

@login_required (redirect_field_name='')
def chest_return(request):
    myself = Character.objects.get(user=request.user)
    cBox = ContainerBox.objects.get(first=myself)
    if myself.state == 26: return open_chest(request,cBox.second.id)
    else: return look_chest(request,cBox.second.id)
        
@login_required(redirect_field_name='')
def chest_action(request,type):
    #fetch the character
    myself = Character.objects.get(user=request.user)
    #find the current container box 
    cBox = ContainerBox.objects.get(first=myself)
    other = Container.objects.get(id=cBox.second.id)
    option = request.POST["benjamin"]
    option = option.strip()
    
    if type=="True": m=True
    else: m=False
    
    if option == 'Close': 
        return interrupt(request)
    elif option in ['Close.','Carry']:
        p=Place.objects.get(id=myself.current_place) 
        m = interrupt(request)
        try:p.people.remove(other)
        except: pass
        myself.inventory.add(other)
        myself.state=0
        myself.cgrs()
        return m
    else:
                    
        if option == 'Give':
            try: 
               item_id = request.POST["inventory"]
               item = Item.objects.get(id=item_id)
            except: return render_to_response('chest.html',{"inventory":myself.inventory.all(),'otherbox':other.items.all(),'d_id':other.id,'m':m})        
            try: amount = int(request.POST["amount"])
            except: amount = item.DP 
            item.transfer(myself.inventory,other.items,amount)
        elif option == 'Take':
            try: 
                item_id = request.POST["otherbox"]
                item = Item.objects.get(id=item_id)
            except: return render_to_response('chest.html',{"inventory":myself.inventory.all(),'otherbox':other.items.all(),'d_id':other.id,'m':m})
            try: amount = int(request.POST["amount"])
            except: amount = item.DP 
            item.transfer(other.items,myself.inventory,amount)
        elif option == 'Give All':
            for item in myself.inventory.all():
                item.transfer(myself.inventory,other.items,item.DP)
        elif option == 'Take All':
            for item in other.items.all():
                item.transfer(other.items,myself.inventory,item.DP)
    return render_to_response('chest.html',{"inventory":myself.inventory.all(),'otherbox':other.items.all(),'d_id':other.id,'m':m})

@login_required(redirect_field_name='')
def open_workbench(request,c_id):
        myself = Character.objects.get(user=request.user)
        place=Place.objects.get(id=myself.current_place)
        if(myself.state == 0):
            otherone  = Workbench.objects.get(id=c_id)
            myself.state=26
            gBox = GenericBox.objects.create(name='gBox',type='gBox',first=myself,second=otherone,current_place=myself.current_place,x=otherone.x,y=otherone.y,w=30,h=30,image='wine and cheese')              
            place.people.remove(myself)
            myself.x = otherone.x+(otherone.w-myself.w)/2
            myself.y = otherone.y-(myself.h/10)
            place.people.remove(otherone)
            place.save()
            gBox.save()
            place.people.add(gBox)
            myself.save()
            prd('render%d'%myself.current_place,getData(request))
        else:
                gBox = GenericBox.objects.get(first=myself)
        if gBox.second.workbench.skill_type == "Blacksmithing":
            return render_to_response('smithing.html',{"blueprints":list(chain(myself.inventory.filter(subtype='Blacksmithing'),myself.blueprints.filter(req_skill_type='Blacksmithing'))),'d_id':gBox.second.id,'m':True})
        elif gBox.second.workbench.skill_type == "Tailoring":
            return render_to_response('smithing.html',{"blueprints":list(chain(myself.inventory.filter(subtype='Tailoring') , myself.blueprints.filter(req_skill_type='Tailoring'))),'d_id':gBox.second.id,'m':True})
        elif gBox.second.workbench.skill_type == "Carpentry":
            return render_to_response('smithing.html',{"blueprints":list(chain(myself.inventory.filter(subtype='Carpentry'),myself.blueprints.filter(req_skill_type='Carpentry'))),'d_id':gBox.second.id,'m':True})
        elif gBox.second.workbench.skill_type == "Cooking":
            return render_to_response('cooking.html',{"blueprints":Blueprint.objects.filter(id__in=myself.inventory.filter(subtype='Cooking').values('id'))|myself.blueprints.filter(req_skill_type='Cooking'),'d_id':gBox.second.id,'m':True})
        
@login_required(redirect_field_name='')
def bench_action(request):
    #fetch the character
    myself = Character.objects.get(user=request.user)
    #find the current container box 
    gBox = GenericBox.objects.get(first=myself)
    other = Workbench.objects.get(id=gBox.second.id)
    option = request.POST["benjamin"]
    option = option.strip()
    
    if option == 'Close':
        return interrupt(request)
    else:
        try: 
            message = 'The item has been crafted!'
            item_id = request.POST["inventory"]
            item = Item.objects.get(id=item_id)
            if option in ('Craft','Cook'):
              s=item.blueprint.create_project(myself,other)
            elif option == 'Tinker':
                item.repair(myself)
            if(s[0]==-1):message = 'Skill level is not enough!'
            elif(s[0]==-2):message = 'Insufficent resources!'
        except: message = 'There is something wrong!'
    if gBox.second.workbench.skill_type == "Blacksmithing":
       return render_to_response('smithing.html',{"blueprints":myself.inventory.filter(subtype='Blacksmith'),'d_id':gBox.second.id,'msg':message})
    elif gBox.second.workbench.skill_type == "Tailoring":
        return render_to_response('smithing.html',{"blueprints":myself.inventory.filter(subtype='Tailor'),'d_id':gBox.second.id,'msg':message})
    elif gBox.second.workbench.skill_type == "Carpentry":
            return render_to_response('smithing.html',{"blueprints":myself.inventory.filter(subtype='Carpentry'),'d_id':gBox.second.id,'msg':message})
    elif gBox.second.workbench.skill_type == "Cooking":
        return render_to_response('cooking.html',{"blueprints":myself.inventory.filter(subtype='Cook'),'d_id':gBox.second.id,'msg':message})

@login_required(redirect_field_name='')
def take_item(request,id,proc):
    char = Character.objects.get(user=request.user)
    if char.state>-1:
        item = Item.objects.get(id=id)
        cell = Place.objects.get(id=char.current_place)
        if proc == "ground":
            if not item.in_use:
                item.in_use=True
                item.save()
            else: return HttpResponse()
            prd('render%d'%char.current_place,simplejson.dumps({'action':'take','id':item.id}))
            if item.typeclass == 'material':
                item.transfer(cell.people,char.inventory,item.DP)
            else: 
                cell.people.remove(item)
                char.inventory.add(item)
            if item.type=="document":
                return render_to_response("close.html")
            else:
                return render_to_response("close.html")
        elif proc == "hand":
            char.inventory.add(item)
            return render_to_response("close.html")
        else:
            if item.category in ('blade','blunt','ranged','key','pen') : char.weapon=None
            elif item.category in ('hat','mask'): char.hat=None
            else: setattr(char,item.category,None)
            exec(item.script)
            onUnequip(item,char);
            char.inventory.add(item)
            char.save()
            prd('render%d'%char.current_place,simplejson.dumps({'action':'self','id':char.id,'data':char.render(cell,char.id,char.state)}))
    return HttpResponse(200)     
        
@login_required (redirect_field_name='')
def send_msg(request):
    myself = Character.objects.get(user=request.user)
    try:
        iBox= InteractionBox.objects.get(first=myself)
    except InteractionBox.DoesNotExist:
        iBox= InteractionBox.objects.get(second=myself)
    
    submit = request.POST["msg_submit"]
    message = request.POST["msg_content"]
    if(submit!='npcSubmit'):
        def splits(string):
            if len(string)>65:
                return string[:65]+'\n'+splits(string[65:]) 
            else: return string
            
        message = splits(message)
        iBox.message_box = iBox.message_box + str(myself.name) + ": " + message + '\n'
        if iBox.message_box.count('\n')>9:
            iBox.message_box= "".join(iBox.message_box.splitlines(True)[-11:])
        iBox.save()
        if -1 in [iBox.first.state,iBox.second.state]: iBox.decompose()
        prd('msg'+str(int(iBox.id)))
        return HttpResponse(200)
    
    else:#TODO: auto scrolldown
        npc=iBox.second.name
        topic = Topic.objects.get(id=int(message))
        iBox.message_box = iBox.message_box + '\n' + str(myself.name) + ": " + topic.request
        if iBox.message_box.count('\n')>11:
            iBox.message_box= "".join(iBox.message_box.splitlines(True)[:-12])
        iBox.message_box = iBox.message_box + '\n' + str(npc) + ": " + topic.response
        if iBox.message_box.count('\n')>11:
            iBox.message_box= "".join(iBox.message_box.splitlines(True)[:-12])
        iBox.save()
        return get_msg_list(request)
        
def get_msg_list(request):
    myself = Character.objects.get(user=request.user)
    try:
        try:
            iBox= InteractionBox.objects.get(first=myself)
        except InteractionBox.DoesNotExist:
            iBox= InteractionBox.objects.get(second=myself)
    except InteractionBox.DoesNotExist: return HttpResponse("Closing Down...")
    return HttpResponse(iBox.message_box)
    
def npc_action(request):
    all = NPC.objects.all()
    errors = []
    for char in all: errors.append(char.operate_char())
    return HttpResponse(errors)

def veichle(request):
    a=Veichle.objects.all()
    for e in a:e.move()
    return HttpResponse()

def lock(request,g_id):
    g = Gate.objects.get(id=g_id)
    gm = Gate.objects.get(id=g.mirror)
    myself = Character.objects.get(user=request.user)
    if myself.weapon and myself.weapon.category == 'key' and myself.weapon.key.gate_id == g.id*g.mirror and myself.weapon.key.persistent:
        g.locked = not g.locked
        g.save()
        gm.locked = g.locked
        gm.save()
        myself.cgrs()
    return HttpResponse(status=200 if g.locked else 201)
    
def enter(request,g_id):
    g = Gate.objects.get(id=g_id)
    myself = Character.objects.get(user=request.user)
    if g.locked == False or (myself.weapon and myself.weapon.category == 'key' and myself.weapon.key.gate_id == g.id*g.mirror):
        if myself.travel_check(g_id):
            p=Place.objects.get(id=g.route)
            myself.destination_place = g.route
            myself.save()
            myself.travel(p)
            c=myself
            if not 600>c.x>100: c.x = 100 if int(c.x)<100 else 600
            if not (p.horizon+p.depth*2/3)>c.y>p.horizon+50: c.y = p.horizon+50 if c.y<p.horizon+50 else p.horizon+p.depth*2/3
            c.save()
            if myself.weapon and myself.weapon.category == 'key' and not myself.weapon.key.persistent and myself.weapon.key.DP<=0: myself.weapon.key.delete()
    return render(request)
    
def view_document(request,d_id,whr):
    char=Character.objects.get(user=request.user)
    mydoc=Item.objects.get(id=d_id)
    address = mydoc.use(char)
    ground=bool(int(whr))
    if mydoc.category=='blueprint':
        return render_to_response('viewdoc.html',{'title':mydoc.name,'content':address,'id':d_id,'ground':ground,'blueprint':True})
    else: return render_to_response('viewdoc.html',{'addr':address,'id':d_id,'ground':ground})

def write_document(request,d_id):
    char = Character.objects.get(user = request.user)
    mydoc=Item.objects.get(id=d_id)
    if char.weapon and char.weapon.category == 'pen' and mydoc.category=='blank':
        return render_to_response('writedoc.html',{'id':d_id})
    else: return HttpResponse('''
<!doctype html>
<html>
    <head>
        <script language="javascript" type="text/javascript">
            function get_back() {parent.jQuery.fn.colorbox({width:"350", height:"320", iframe:true, href:'/index/cpanel/3/'});return false;}
        </script>
    </head>
    <body>
        <span style="font-size:25px;" align="center">You don't have a pen!</span>
        <br/><br/><br/>
        <a src="/index/files/blank.gif" onclick="get_back();">
            <span style="font-size:12px;" align="center">Return</span>
        </a>
    </body>
</html>
                              ''')
    
def save_document(request,d_id):
    doc_title = unicode(request.POST['title'])
    doc_body = unicode(request.POST['body'])
    
    mydoc=Item.objects.get(id=d_id)
    mydoc.name = doc_title
    length = len(doc_body)
    mydoc.category = 'usr_doc_%d.html'%mydoc.id
    mydoc.save()
    
    with open('public/documents/custom/%s'%mydoc.category,'w') as doc:
        doc.write(u'''
        <!--
        '''+doc_title+'''
        -->
        <!doctype html>
        <html>
            <head>
                <link href='http://fonts.googleapis.com/css?family=Dr+Sugiyama&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
                <title>'''+doc_title+'''</title>
            </head>
                <body>
                    <pre style="font-family: 'Dr Sugiyama', cursive; font-size:18px; font-weight: 400;width:350px;white-space:pre-wrap;word-wrap:break-word;">
                       '''+doc_body+'''
                    </pre>
                </body>
        </html>
        ''')
        
    return HttpResponse('''
<!doctype html>
<html>
    <head>
        <script language="javascript" type="text/javascript">
            window.onload = function get_back() {parent.jQuery.fn.colorbox({width:"350", height:"320", iframe:true, href:'/index/cpanel/3/'});return false;}
        </script>
    </head>
</html>
                        ''')
    
def view_the_book(request,d_id,whr):
    char=Character.objects.get(user=request.user)
    mydoc=Item.objects.get(id=d_id)
    address = mydoc.use(char)
    ground=bool(int(whr))
    allplaces=Place.objects.all()
    allchars=Character.objects.all()
    return render_to_response('theBook.html',{'addr':address,'id':d_id,'ground':ground,'ppp':allplaces,'ccc':allchars})

#World Initalization    
def init_world(request):
    #Create Cells
    Marnaw = Place.objects.create(name='Marnaw',category='outer',depth=300,horizon=200)
    Marnaw_thaedus = Place.objects.create(name='Marnaw - The Ruins of Thaedus',category='outer',depth=320,horizon=220)
    Marnaw_west = Place.objects.create(name='Marnaw - West',category='outer',depth=300,horizon=200)
    Marnaw_moltsis = Place.objects.create(name='Marnaw - Moltsis Plateu',category='outer',depth=330,horizon=210)
    Marnaw_warehouse= Place.objects.create(name='Marnaw - Warehouse',category='inner',depth=330,horizon=210)
    Marnaw_main_street = Place.objects.create(name='Marnaw - Main St.',category='outer',depth=330,horizon=210)
    Marnaw_moltsis_north = Place.objects.create(name='Marnaw - Moltsis Plateu North',category='outer',depth=300,horizon=200)
    Marnaw_mardaun = Place.objects.create(name='Marnaw - Mardaun Estate',category='outer',depth=300,horizon=200)
    Marnaw_mardaun_manor = Place.objects.create(name='Mardaun Manor',category='inner',depth=320,horizon=180)
    Marnaw_mardaun_manor_west_hall = Place.objects.create(name='Mardaun Manor - East Wing Hall',category='inner',depth=280,horizon=220)   
    Marnaw_docks = Place.objects.create(name='Marnaw - Docks',category='outer',depth=300,horizon=200)
    
    Farman_docks = Place.objects.create(name='Farman - Docks',category='outer',depth=300,horizon=225)
    Farman_market = Place.objects.create(name='Farman - Market District',category='outer',depth=300,horizon=200)
    Farman_thelion = Place.objects.create(name='Farman - Thelion Plaza',category='outer',depth=300,horizon=200)
    Farman_council = Place.objects.create(name='Farman - Council District',category='outer',depth=385,horizon=235)
    Farman_council_hall = Place.objects.create(name='Great Council Hall',category='inner',depth=280,horizon=190)
       
    Savada = Place.objects.create(name='Savada',category='outer',depth=300,horizon=200)
    
    Void = Place.objects.create(name='The Void',category='outer',depth=300,horizon=200)
    
    
    #Create connections
    Marnaw.connect(Marnaw_west,2300)
    Marnaw.connect(Marnaw_main_street,150)
    Marnaw_main_street.insert(Marnaw_warehouse.id,'The Warehouse', 'door2',305,265,65,100,20,-175,85,130)
    Marnaw.connect(Marnaw_docks,400)
    Marnaw.connect(Marnaw_thaedus,700)
    Marnaw.connect(Marnaw_mardaun,3900)
    Marnaw_west.connect(Savada,2300)
    Marnaw_west.connect(Marnaw_moltsis,1000)
    Marnaw_moltsis.connect(Marnaw_moltsis_north,450)
    Marnaw_west.connect(Marnaw_thaedus,1900)
    Marnaw_mardaun.insert(Marnaw_mardaun_manor.id,'Mardaun Manor - Main Hall', 'Mardaun Manor',281,138,212,130,397,238,70,135)
    Marnaw_mardaun_manor.insert(Marnaw_mardaun_manor_west_hall.id,'Mardaun Manor - East Wing Hall', 'door',167,285,18,113,165,290,22,126)
    Farman_market.connect(Farman_thelion,250)   
    Farman_council.connect(Farman_thelion,350) 
    Farman_council.insert(Farman_council_hall.id,'Great Council Hall', 'door',605,265,65,100,20,-175,85,130)
     
    #Dynamic connections
    Mermaid = Veichle.objects.create(name='Mermaid at Farman - Docks',category='inner',depth=258,horizon=170,route=Marnaw_docks.id)
    Farman_docks.insert(Farman_docks.id,'Mermaid', 'Galland Ship',360,135,100,200,30,-130,80,100)
    
    #Add generic topics
    t1=Topic.objects.create(request="Hello.",response="Hi.",title="greet")
    t2=Topic.objects.create(request="Who are you?",response="I am %name the %race.",title="background")
    t3=Topic.objects.create(request="Do you have a work for me?",response="No, not for now.",title="work")
    
    #Workbenches
    anvil1 = Workbench.objects.create(name='anvil',image='anvil',type='workbench',x=120,y=140,w=60,h=55,size=18,skill_type='Blacksmithing',power=60)
    jbench1 = Workbench.objects.create(name='joiner bench',image='joiner bench',x=320,y=140,w=128,h=74,size=18,skill_type='Carpentry',power=60)
    loom1 = Workbench.objects.create(name='loom',image='loom',type='workbench',x=120,y=240,w=64,h=64,size=18,skill_type='Tailoring',power=70)
    campfire1 = Workbench.objects.create(name='campfire',image='campfire',type='workbench',x=320,y=240,w=44,h=44,size=18,skill_type='Cooking',power=20)
    cooking_set1 = Workbench.objects.create(name='cooking set',image='cooking set',type='workbench',x=320,y=340,w=51,h=134,size=18,skill_type='Cooking',power=70)
    anvil2 = Workbench.objects.create(name='anvil',image='anvil',type='workbench',x=320,y=340,w=60,h=55,size=18,skill_type='Blacksmithing',power=60)
    jbench2 = Workbench.objects.create(name='joiner bench',image='joiner bench',type='workbench',x=120,y=440,w=128,h=74,size=18,skill_type='Carpentry',power=60)
    loom2 = Workbench.objects.create(name='loom',image='loom',type='workbench',x=320,y=440,w=64,h=64,size=18,skill_type='Tailoring',power=70)
    campfire2 = Workbench.objects.create(name='campfire',image='campfire',type='workbench',x=120,y=540,w=44,h=44,size=18,skill_type='Cooking',power=20)
    cooking_set2 = Workbench.objects.create(name='cooking set',image='cooking set',type='workbench',x=320,y=540,w=51,h=134,size=18,skill_type='Cooking',power=70)
    
    anvil1.save()
    jbench1.save()
    loom1.save()
    campfire1.save()
    cooking_set1.save()
    anvil2.save()
    jbench2.save()
    loom2.save()
    campfire2.save()
    cooking_set2.save()
    
    Marnaw_warehouse.people.add(anvil1)
    Marnaw_warehouse.people.add(anvil2)
    Marnaw_warehouse.people.add(loom1)
    Marnaw_warehouse.people.add(loom2)
    Marnaw_warehouse.people.add(jbench1)
    Marnaw_warehouse.people.add(jbench2)
    Marnaw_warehouse.people.add(cooking_set1)
    Marnaw_warehouse.people.add(cooking_set2)
    Marnaw_west.people.add(campfire1)
    Marnaw_moltsis.people.add(campfire2)
    
    #Special items
    fbook=Item.objects.create(name='a fragment of paper',type='item',category='TheBook',typeclass='document',subtype='read',marked=False,value=50,x=randint(100,550),y=randint(330,390),DP=10000,a_maxdp=10000,w=50,h=20)
    Savada.people.add(fbook)
    #Raw items
    s_ore = Item.objects.create(name='silver ore',type='item',category='edible',typeclass='material',subtype='metal',value=55,power=-45,w=32,h=32,size=1800)
    s_ore.save()
    i_ore = Item.objects.create(name='iron ore',type='item',category='edible',typeclass='material',subtype='metal',value=35,power=-45,w=32,h=32,size=2700)
    i_ore.save()
    s_ing = Item.objects.create(name='silver ingot',type='item',category='proc',typeclass='material',subtype='metal',value=95,power=-45,w=32,h=32,size=1000)
    s_ing.save()
    i_ing = Item.objects.create(name='iron ingot',type='item',category='proc',typeclass='material',subtype='metal',value=70,power=-45,w=32,h=32,size=1400)
    i_ing.save()
    
    tomato = Item.objects.create(name='tomato',type='item',category='edible',typeclass='material',subtype='vegetable',value=2,power=4,w=24,h=24,size=12)
    tomato.save()
    apple = Item.objects.create(name='apple',type='item',category='edible',typeclass='material',subtype='fruit',value=2,power=5,w=24,h=24,size=12)
    apple.save()
    sugar = Item.objects.create(name='sugar',type='item',category='edible',typeclass='material',subtype='grain',value=4,power=6,w=24,h=24,size=12)
    sugar.save()
    cocoa = Item.objects.create(name='cocoa',type='item',category='edible',typeclass='material',subtype='grain',value=14,power=3,w=24,h=24,size=12)
    cocoa.save()
    onion = Item.objects.create(name='onion',type='item',category='edible',typeclass='material',subtype='vegetable',value=1,power=2,w=24,h=24,size=18)
    onion.save()
    wheat = Item.objects.create(name='wheat',type='item',category='edible',typeclass='material',subtype='grains',value=1,power=2,w=24,h=24,size=18)
    wheat.save()
    eggplant = Item.objects.create(name='eggplant',type='item',category='edible',typeclass='material',subtype='vegetable',value=2,power=2,w=24,h=24,size=18)
    eggplant.save()
    egg = Item.objects.create(name='egg',type='item',category='edible',typeclass='material',subtype='protein',value=1,power=5,w=24,h=24,size=18)
    egg.save()
    cabbage = Item.objects.create(name='cabbage',type='item',category='edible',typeclass='material',subtype='vegetable',value=1,power=2,w=24,h=24,size=18)
    cabbage.save()
    oliveoil = Item.objects.create(name='olive oil',type='item',category='edible',typeclass='material',subtype='liquid',value=12,power=5,w=24,h=24,size=18)
    oliveoil.save()
    milk = Item.objects.create(name='milk',type='item',category='edible',typeclass='material',subtype='liquid',value=8,power=5,w=24,h=24,size=18)
    milk.save()
    water = Item.objects.create(name='water',type='item',category='edible',typeclass='material',subtype='liquid',value=1,power=4,w=24,h=24,size=18)
    water.save()
    trout = Item.objects.create(name='trout',type='item',category='edible',typeclass='material',subtype='fish',value=1,power=3,w=24,h=24,size=25)
    trout.save()
    cotton= Item.objects.create(name='cotton ball',type='item',category='raw',typeclass='material',subtype='cotton',value=5,power=0,w=24,h=24,size=25)
    cotton.save()
    
    wood = Item.objects.create(name='wood log',type='item',category='raw',typeclass='material',subtype='wood',value=4,power=-1,w=24,h=24,size=25)
    wood.save()
    woodstick= Item.objects.create(name='wooden stick',type='item',category='blunt',typeclass='tool',subtype='wood',value=2,power=2,w=50,h=25,size=25)
    woodstick.save()
    woodpanel= Item.objects.create(name='wooden panel',type='item',category='proc',typeclass='material',subtype='wood',value=5,power=-1,w=24,h=24,size=25)
    woodpanel.save()
    cloth= Item.objects.create(name='cloth',type='item',category='proc',typeclass='material',subtype='cotton',value=8,power=-1,w=24,h=24,size=25)
    cloth.save()
    leather= Item.objects.create(name='leather',type='item',category='proc',typeclass='material',subtype='skin',value=20,power=0,w=24,h=24,size=25)
    leather.save()
    lstrips= Item.objects.create(name='leather strips',type='item',category='proc',typeclass='material',subtype='skin',value=6,power=0,w=24,h=24,size=25)
    lstrips.save()
    yarn= Item.objects.create(name='yarn',type='item',category='proc',typeclass='material',subtype='cotton',value=3,power=0,w=24,h=24,size=25)
    yarn.save()
    
    #Add harvestings
    h0=Harvest.objects.create(name="tomato fields",container=tomato,interval=42,handler='Gardening')
    h0.save()
    h1=Harvest.objects.create(name="onion fields",container=onion,interval=40,handler='Gardening')
    h1.save()
    h9=Harvest.objects.create(name="apple trees",container=apple,interval=50,handler='Gardening')
    h9.save()
    Marnaw_west.harvests.add(h0)
    Marnaw_west.harvests.add(h1)
    Marnaw_west.harvests.add(h9)
    
    h2=Harvest.objects.create(name="silver mine",container=s_ore,interval=320,amount=2000,handler='Mining')
    h2.save()
    Savada.harvests.add(h2)
    
    h3=Harvest.objects.create(name="iron mine",container=i_ore,interval=270,handler='Mining')
    h3.save()
    h4=Harvest.objects.create(name="wheat fields",container=wheat,interval=40,handler='Gardening')
    h4.save()
    Marnaw_moltsis_north.harvests.add(h3)
    Marnaw_moltsis_north.harvests.add(h4)
    
    
    h5=Harvest.objects.create(name="cotton fields",container=cotton,interval=35,handler='Gardening')
    h5.save()
    h6=Harvest.objects.create(name="eggplant farm",container=eggplant,interval=42,handler='Gardening')
    h6.save()
    h10=Harvest.objects.create(name="cabbage farm",container=eggplant,interval=32,handler='Gardening')
    h10.save()
    Marnaw_mardaun.harvests.add(h5)
    Marnaw_mardaun.harvests.add(h6)
    Marnaw_mardaun.harvests.add(h10)
    
    h7=Harvest.objects.create(name="Moltsis Forest",container=wood,interval=40,handler='Lumberjack')
    h7.save()
    Marnaw_moltsis.harvests.add(h7)
    
    h8=Harvest.objects.create(name="Pelonic Cove",container=trout,interval=60,handler='Fishing')
    h8.save()
    Marnaw_docks.harvests.add(h8)
    
    #save
    Marnaw.save()
    Marnaw_docks.save()
    Marnaw_thaedus.save()
    Marnaw_moltsis.save()
    Marnaw_moltsis_north.save()
    Marnaw_mardaun.save()
    Marnaw_mardaun_manor.save()
    Marnaw_mardaun_manor_west_hall.save()
    Marnaw_west.save()
    Marnaw_warehouse.save()
    Marnaw_main_street.save()
    
    Farman_docks.save()
    Farman_thelion.save()
    Farman_market.save()
    Farman_council.save()
    Farman_council_hall.save()
    
    Savada.save()
    
    Void.save()
    
    Mermaid.save()
    
    t1.save()
    t2.save()
    t3.save()
    
    #Knowledge from previous creations
    import os
    path = '/home/gma/www/gma/public/documents/custom/'
    listing = os.listdir(path)
    for e in listing:
        try:
            f = open("%s%s"%(path,e),'r')
            doc_name = f.readlines()[1]
            f.close()
            c_docs=Item.objects.create(name=doc_name,type='item',category=e,typeclass='document',subtype='read',marked=False,value=15,x=randint(100,550),y=randint(330,390),DP=10000,a_maxdp=10000,w=50,h=20)
            c_docs.save()
            Void.people.add(c_docs)
        except:pass
    return HttpResponseRedirect("/index/")
    
#WARNING: This method is highly experimental.    
def add_topic(request):
    req=str(request.POST['req'])
    rsp=str(request.POST['rsp'])
    ttl=str(request.POST['ttl'])
    npc=int(request.POST['npc'])
    try: 
        n=NPC.objects.get(id=npc)
        n.add_topic(req,rsp,ttl)
    except: print 'Something is wrong with the id'
    return HttpResponse(200)
 
#WARNING: This method is highly experimental. 
@login_required (redirect_field_name='')    
def the_book(request):
    what=request.POST['what']
    
    if(what=='go'):
        where=Place.objects.get(id=int(request.POST['where']))
        Character.objects.get(user=request.user).move(where)
    elif(what=='kil'):
        who=int(request.POST['who'])
        char=Character.objects.get(id=who)
        char.HP=-1
        char.save()
        char.end_turn()
    elif(what=='tel'):
        who=int(request.POST['who'])
        where=Place.objects.get(id=int(request.POST['where']))
        char=Character.objects.get(id=who)
        if char.state>-1:
            if char.travel_check(where):
                char.move(where)    
    elif(what=='res'):
        who=int(request.POST['who'])
        where=Place.objects.get(id=int(request.POST['where']))
        char=Character.objects.get(id=who)
        if char.state<0:
            char.HP=1
            char.state=0
            char.save()
            char.move(where)
    elif(what=='cur'):
        where=Place.objects.get(id=int(request.POST['where']))
        c=Creature.init_creature('Werewolf','Werewolf','m')
        s = Spawner.objects.create(x=0,y=0,w=0,h=0,image=0,type='spawn',interval=10,max=10)
        s.bind_creature(c)
        s.save()
        where.people.add(s)
    elif(what=='cre'):
        npc=NPC.objects.create(char=Character.init(request),is_shopkeeper=not bool(randint(0,3)))
        for e in [1,2,3]:
            npc.add_existing_topic(e)
        npc.operate_char()      
    return HttpResponseRedirect("/index/")
