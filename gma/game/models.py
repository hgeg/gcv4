#-*- coding: cp1254 -*-

#/############################################
#
#    Model definitions of gcv4.
#    Author:             Ali Can Bulbul
#    Last Update:        21.02.2012 00:47
#    Current Version:    Rev8 0.8.4.3
#                                                
#/############################################

from __future__ import division
import string
from django.utils import simplejson
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from random import randint,randrange,choice
from copy import deepcopy
import datetime
from math import log,e

import site
site.addsitedir('/home/gma/modules')

import pusher
pusher.app_id = '20374'
pusher.key = '2db61f16f86947ae603e'
pusher.secret = '491bf979f3b0da949aef'

p = pusher.Pusher()

#FIXED: Add Container model.
#REV3: Make Spell model functional.
#REV1: Lychantrophy

#name list for npc generation
dem_names = ('Abetatas', 'Aledil', 'Esalutin', 'Etkan', 'Hitozeyh', 'Ivixen', 'Iyenoral', 'Kened', 'Liteb', 'Odiroveh', 'Ranozaba', 'Rela', 'Rerobub', 'Rikda', 'Risared', 'Riye', 'Rotra', 'Senakina', 'Vakidrir', 'Anean', 'Anzid', 'Axatoz', 'Bovareot', 'Turafmor', 'Undat', 'Xolidedi', 'Xuzan', 'Yraba')
def_names = ('Erissare', 'Termanin', 'Irinde', 'Estird', 'Ardarume', 'Elanin', 'Taarum', 'Viranirn', 'Nalcarum', 'Estirdar', 'Celria', 'Calmanin', 'Elaninde', 'Erissa' )
hum_names = ('Nia', 'Adrogde', 'Arejand', 'Altdon', 'Erarm', 'Thom', 'Eobne', 'Lar', 'Starlert', 'Ivatd', 'Edarew', 'Anarny', 'Edantopher', 'Taew', 'Aliatopher', 'Nicny', 'Sogvid', 'Edaew', 'Ju', 'Alle')
orm_names = ('Largasha Bashnag', 'Mashag Rush', 'Rulfim Yak', 'Yadba', 'Ulamul Ghashn', 'Gakkenfe Lumbakh', 'Shakh Bogadb', 'Uramulg Lumbuk', 'Yadbaam Shadbu', 'Bugdul Shadbu', 'Mashagam Yagadbu', 'Bagamu Ugruma', 'Bogamul Khazor', 'Guaron Shagrak', 'Uramul Kharz', 'Lugdul Murgol', 'Ugdul Glorku', 'Lugdul Shamub', 'Shakh Shadbuk', 'Atulg Olorku' )
hef_names = ('Culumani', 'Elaninde', 'Erissa', 'Calmanin', 'Anirne', 'Termanin', 'Erissare', 'Calman', 'Estirdar', 'Elanin', 'Viranirn', 'Fistirne', 'Imarume', 'Estird', 'Ardaru' )

#default script declarations
script_default = '''
def onUse(self,target=None):pass
def onUnequip(self,target=None):pass
def onAdd(self,target=None):pass
def onRemove(self,target=None):pass
def onEnter(self,target=None):pass
def onExit(self,target=None):pass
def onMention(self,target=None):pass
def onInteract(self,target=None):pass
'''

#colorbox window codes
box_link = { 0 : 'href="/index/cpanel/" class="cBox"',
            -1 : 'href="#" class="cBox"',
            26 : 'href="/index/interact:return/" class="tBox"',
            27 : 'href="/index/interact:return/" class="tBox"',
             1 : 'href="/index/interact:return/" class="iBox"',
             2 : 'href="/index/interact:return/" class="iBox"',
             3 : 'href="/index/interact:return/" class="iBox"',
             4 : 'href="/index/interact:return/" class="iBox"'
           }
                

def prd(channel='render',data=''):
    p[channel].trigger('update',data)
    print 'message passed to %s'%channel
    return True

#Wrapper class for user for session tracking
#TODO: issues in double tabs
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    last_session_key = models.CharField(blank=True, null=True, max_length=40)
    messages = models.TextField()
    
    #setting session per user limit
    #author: JackLeo
    #http://stackoverflow.com/questions/5470210/
    def set_session_key(self, key):
        if self.last_session_key and not self.last_session_key == key:
            try:Session.objects.get(session_key=self.last_session_key).delete()
            except: pass
        self.last_session_key = key
        self.save()

#Predecessor of all classes existed in a cell
#all primary attributes of models should be here
class GenericObject(models.Model): 
    x=models.IntegerField(default=0)#x position
    y=models.IntegerField(default=0)#y position
    w=models.IntegerField()#width
    h=models.IntegerField()#height
    size=models.IntegerField(default=0)#weight
    image = models.CharField(max_length=50)#image
    name = models.CharField(max_length=150,blank=True)#name
    type = models.CharField(max_length=10)#type can be char, npcChar, item, iBox, npcBox, place, container, gate, mob or spawn
    message = models.CharField(max_length=100,blank=True)#message of a genericobject
    counter = models.DateTimeField(default=datetime.datetime.now())#counter for messaging facility
    script = models.TextField(default=script_default)#object's script for implementing event-driven use.
    
    #generic render method
    #renders image of a GO 
    def render(self,place,mychar_id,mychar_state,flip=False,interacted=None):
        try: assert(place.id!=-1)
        except: place = Place.objects.get(id=place)
        c = 180 #perspective constant
        h_=self.h*1.5*c/(place.depth*2.0-self.y) #display height
        w_=self.w*1.5*c/(place.depth*2.0-self.y) #display width
        y_= (self.y*1.2*c/place.depth)+place.horizon-(h_*12/11) #y position on screen
        x_= self.x-w_/2 #x position on screen
        w_large = (14*w_/(self.w+25))+w_ #increase width if a weapon is hold.
        n_pos = (w_/2-len(self.name)*3,(-h_/10)-2) #current coordinates of GO's name
        ischar= self.type in ['char','npcChar']
        ismychar = self.id == mychar_id
        data=''
        #if the object is a character
        if ischar:    
          if self.character.counter < datetime.datetime.now():
                self.character.shoutbox = ''
                self.character.save()
          if self.character.type=='npcChar' and self.character.action=="travel":
            if self.character.time_left>datetime.datetime.now(): return ''
          else:
            params = {'h_':h_, 'w_':w_, 'y_':y_, 'x_':x_, 'z_':self.y, 'z_control': self.y+500, 'w_large':w_large if self.character.weapon and self.character.weapon.message=='large' else w_, 'n_pos_x': n_pos[0],'n_pos_y': n_pos[1],
                'st_': h_*92/100,
                'sl_': w_*1/7,
                'sw_': w_*4/6,
                'sh_': h_*1/10,
                'id':self.id,'mychar':mychar_id,'name':self.name,'action':self.character.action,
                'gender':self.character.gender,
                'hair':self.character.hair if not self.character.hat else '6',
                'face':self.character.face,
                'beard':self.character.facial,
                'image':'%s/%s/%s'%('char' if ischar else self.type,self.image,self.character.gender),
                'shader':'onload="darken(this,lum,false);',
                'shirt':self.character.shirt.name if self.character.shirt else 'blank',
                'pants':self.character.pants.name if self.character.pants else 'blank',
                'armor':self.character.armor.name if self.character.armor else 'blank',
                'boots':self.character.boots.name if self.character.boots else 'blank',
                'gloves':self.character.gloves.name if self.character.gloves else 'blank',
                'greaves':self.character.greaves.name if self.character.greaves else 'blank',
                'pauldrons':self.character.pauldrons.name if self.character.pauldrons else 'blank',
                'weapon':('key' if self.character.weapon.category=='key' else self.character.weapon.name) if self.character.weapon else 'blank',
                'mask':self.character.mask.name if self.character.mask else 'blank',
                'hat':self.character.hat.name if self.character.hat else 'blank',
                'cape':self.character.cape.name if self.character.cape else 'blank',
                'flip': 'true' if flip else 'false',
                'state': '<img style="position:absolute;left:%dpx;top:%dpx;" src="http://gcv4.s3.amazonaws.com/files/char/zzz.gif" border="0"></img>'%(w_/2,-h_/3) if self.character.action=='rest' else '',
                'p': '%',
                'menu': box_link[mychar_state],
                'linkb': '<a href="/index/interact:return">' if interacted==mychar_id else '',
                'linke': '</a>' if interacted==mychar_id else '',
                'pauldrons':self.character.pauldrons.name if self.character.pauldrons else 'blank',
                'weapon':('key' if self.character.weapon.category=='key' else self.character.weapon.name) if self.character.weapon else 'blank',
                'hat':self.character.hat.name if self.character.hat else 'blank',
                'shoutbox':'<span class="shoutbox" id="shout%d" style="position: absolute;left:%d;top:%dpx;"> %s </span>'%(self.id,w_/2,n_pos[1]-25,self.character.shoutbox),
                'options':'' if (mychar_state or self.character.state) else '''
<div id="options%(id)d" onmouseover="$('#options%(id)d').css({visibility:'visible','z-index':999999});"  onmouseout="$('#options%(id)d').css({visibility:'hidden','z-index':-1});" style="position:absolute;left:0px;top:0px;width:%(w_)dpx;height:%(h_)dpx;visibility:hidden;z-index:%(z_control)d;">
    <a class="iBox" href="/index/interact/%(mychar)d/%(id)d/">
        <img style="position:absolute;top:0px;height:27px;"  src="/index/files/item/icon_talk.gif" border="0"></img>
    </a>
    <a onclick="ajaxReq('/index/attack:m/%(mychar)d/%(id)d/');">
        <img style="position:absolute;top:27px;height:27px" src="/index/files/item/icon_attack.gif" border="0"></img>
    </a>
    <a onclick="ajaxReq('/index/attack:s/%(mychar)d/%(id)d/');">
        <img style="position:absolute;top:54px;height:27px" src="/index/files/item/icon_spell.gif" border="0"></img>
    </a>
</div>
                          '''%{'id':self.id, 'z_control': self.y+122500,'mychar':mychar_id,'h_':h_, 'w_':w_, 'y_':y_, 'x_':x_}}
            #if this character  belongs to the user:
            if ismychar:
                    data =  ''' 
    <div id="gObj%(id)d" onfocus="if(this.blur)this.blur()"  style="position:absolute;left:%(x_)dpx;top:%(y_)dpx;position:absolute;width:%(w_)dpx;height:%(h_)dpx;z-index:%(z_)d;"align="left" ondragenter="return false;" ondragover="event.preventDefault()" ondrop="drop(event);">
     %(state)s                
    %(shoutbox)s                
    <span style="position:absolute;left:%(n_pos_x)d;top:%(n_pos_y)d;color:#ffffff;font-family:Verdana,'DejaVu Sans';font-size:12px;background-color:#24507b;white-space: nowrap;">
        %(name)s
    </span>

      <div id="shadow%(id)d" style="position:absolute;width:%(sw_)dpx;height:%(sh_)dpx;background-color:transparent;box-shadow:%(sl_)dpx %(st_)dpx 4px rgba(0,0,0,0.7); border-radius:10px;" align="left"></div>
   
        <img id="cape%(id)d" class="imgeq" src="/index/files/%(image)s/%(cape)s.gif" onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="char%(id)d" name="%(action)s" class="imgeq" src="/index/files/%(image)s/char.gif/" onload="darken(this,lum,%(flip)s);" border="0"></img>
        
        <img id="face%(id)d" class="imgeq" src="/index/files/%(image)s/appereance/f%(face)s.gif" onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="mask%(id)d" class="imgeq" src="/index/files/%(image)s/%(mask)s.gif" onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="hair%(id)d" class="imgeq" src="/index/files/%(image)s/appereance/h%(hair)s.gif" onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="beard%(id)d" class="imgeq" src="/index/files/%(image)s/appereance/b%(beard)s.gif" onload="darken(this,lum,%(flip)s);" border="0"></img>  
        
        <img id="pants%(id)d"     class="imgeq"  src="/index/files/%(image)s/%(pants)s.gif"     onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="boots%(id)d"     class="imgeq"  src="/index/files/%(image)s/%(boots)s.gif"     onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="greaves%(id)d"   class="imgeq"  src="/index/files/%(image)s/%(greaves)s.gif"   onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="shirt%(id)d"     class="imgeq"  src="/index/files/%(image)s/%(shirt)s.gif"     onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="armor%(id)d"     class="imgeq"  src="/index/files/%(image)s/%(armor)s.gif"     onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="pauldrons%(id)d" class="imgeq"  src="/index/files/%(image)s/%(pauldrons)s.gif" onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="hat%(id)d"       class="imgeq"  src="/index/files/%(image)s/%(hat)s.gif"       onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="gloves%(id)d"    class="imgeq"  src="/index/files/%(image)s/%(gloves)s.gif"    onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="weapon%(id)d"    class="imgeq"  src="/index/files/%(image)s/%(weapon)s.gif"    onload="darken(this,lum,%(flip)s);" border="0"></img>
    </div>                    
                            '''%params
                
            else:
                if (mychar_state<0 and self.character.state<0) or (mychar_state>=0 and self.character.state>=0):  
                    data = '''
    %(linkb)s
    <div id="gObj%(id)d" onmouseover="jQuery($('#options%(id)d')).css({visibility:'visible','z-index':999999});"  onmouseout="jQuery($('#options%(id)d')).css({visibility:'hidden','z-index':-1});" style="position:absolute;left:%(x_)dpx;top:%(y_)dpx;z-index:%(z_)d;width:%(w_)dpx;height:%(h_)dpx;" align="left">  
        %(state)s                
        %(shoutbox)s
        <span style="position:absolute;left:%(n_pos_x)d;top:%(n_pos_y)d;color:#ffffff;font-family:Verdana,'DejaVu Sans';font-size:12px;background-color:#24507b;white-space: nowrap;">
            %(name)s
        </span>
      
        <div id="shadow%(id)d" style="position:absolute;width:%(sw_)dpx;height:%(sh_)dpx;background-color:transparent;box-shadow:%(sl_)dpx %(st_)dpx 4px rgba(0,0,0,0.7); border-radius:10px;" align="left"></div>
          
        <img id="cape%(id)d" class="imgeq" src="/index/files/%(image)s/%(cape)s.gif" onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="char%(id)d" name="%(action)s" class="imgeq" src="/index/files/%(image)s/char.gif/" onload="darken(this,lum,%(flip)s);" border="0"></img>
        
        <img id="face%(id)d" class="imgeq" src="/index/files/%(image)s/appereance/f%(face)s.gif" onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="mask%(id)d" class="imgeq" src="/index/files/%(image)s/%(mask)s.gif" onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="hair%(id)d" class="imgeq" src="/index/files/%(image)s/appereance/h%(hair)s.gif" onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="beard%(id)d" class="imgeq" src="/index/files/%(image)s/appereance/b%(beard)s.gif" onload="darken(this,lum,%(flip)s);" border="0"></img>  
        
           
        <img id="pants%(id)d"     class="imgeq"  src="/index/files/%(image)s/%(pants)s.gif"     onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="boots%(id)d"     class="imgeq"  src="/index/files/%(image)s/%(boots)s.gif"     onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="greaves%(id)d"   class="imgeq"  src="/index/files/%(image)s/%(greaves)s.gif"   onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="shirt%(id)d"     class="imgeq"  src="/index/files/%(image)s/%(shirt)s.gif"     onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="armor%(id)d"     class="imgeq"  src="/index/files/%(image)s/%(armor)s.gif"     onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="pauldrons%(id)d" class="imgeq"  src="/index/files/%(image)s/%(pauldrons)s.gif" onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="hat%(id)d"       class="imgeq"  src="/index/files/%(image)s/%(hat)s.gif"       onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="gloves%(id)d"    class="imgeq"  src="/index/files/%(image)s/%(gloves)s.gif"    onload="darken(this,lum,%(flip)s);" border="0"></img>
        <img id="weapon%(id)d"    class="imgeq"  src="/index/files/%(image)s/%(weapon)s.gif"    onload="darken(this,lum,%(flip)s);" border="0"></img>
      
    %(options)s
        
    </div> 
    %(linke)s                    
                            '''%params
                else: data=''
                        
        elif self.type=='item':
            if mychar_state == -1:
                data = '' 
            else:
                params = {'h_':h_, 'w_':w_, 'y_':y_-h_/4, 'x_':x_, 'z_':y_, 'name':self.name, 'name_d':self.item.get_name(),'id':self.id,'shader':'onload="darken(this,lum,false);' if self.message!='light' else '','image':self.item.typeclass, 'lum': 'lum' if place.category=="outer" else 0,'DP': self.item.DP/self.item.a_maxdp*100,'amount':self.item.DP,'value':self.item.value}
                if self.item.typeclass=='document':
                    if self.item.category=='TheBook': data =  ''' 
                    
    <div id="gObj%(id)d" class="tooltip" title="%(name)s<br/>Value:%(value)d" style="position:absolute;left:%(x_)dpx;top:%(y_)dpx;z-index:%(z_)d;" align="left">  
        <a draggable="true" ondragstart="drag(event,%(id)d);" href="/index/viewdocx/%(id)d/1/" class="dBox">         
            <img width="%(w_)d" height="%(h_)d" src="/index/files/item/%(image)s.gif" border="0" %(shader)s">
        </a>
    </div>                                                          '''%params
                    elif self.item.category=='scroll': data =  ''' 
        <div id="gObj%(id)d" class="tooltip" title="%(name)s<br/>Value:%(value)d" onclick="sendCursorPos();" style="position:absolute;left:%(x_)d;top:%(y_)d" width="%(w_)d" height="%(h_)d" draggable="true" ondragstart="return drag(event,%(id)d);">              
            <img src="/index/files/item/%(image)s.gif" border="0" %(shader)s">
        </div>
                                                              '''%params
                    else: data =  ''' 
                    
    <div id="gObj%(id)d" class="tooltip" title="%(name)s<br/>Value:%(value)d" style="position:absolute;left:%(x_)dpx;top:%(y_)dpx;z-index:%(z_)d;" align="left">  
        <a draggable="true" ondragstart="drag(event,%(id)d);" title="%(name_d)s" href="/index/viewdoc/%(id)s/1/" class="dBox">            
            <img width="%(w_)d" height="%(h_)d" src="/index/files/item/%(image)s.gif" border="0">
        </a>
    </div>                
                                  '''%params
                              
                elif self.item.typeclass in ['tool','material']:
                    if self.item.category == 'key': data =  '''    

    <div id="gObj%(id)d" class="tooltip" title="%(name)s<br/>DP: %(DP)s%%<br/>Base Value:%(value)d" style="position:absolute;left:%(x_)dpx;top:%(y_)dpx;z-index:%(z_)d;" align="left">  
        <a  draggable="true"  ondragstart="drag(event,%(id)d);" onclick="sendCursorPos();">            
            <img style="position:absolute;left:%(x_)d;top:%(y_)d" width="%(w_)d" height="%(h_)d" src="/index/files/item/keys.gif" border="0" %(shader)s">
        </a>        
    </div>                                                                     '''%params
                    elif self.item.typeclass == 'material': data =  '''    
    <div id="gObj%(id)d" class="tooltip" title="%(name)s<br/>Amount: %(amount)s<br/>Unit Value:%(value)d" style="position:absolute;left:%(x_)dpx;top:%(y_)dpx;z-index:%(z_)dpx;"align="left">  
        <a draggable="true"  ondragstart="drag(event,%(id)d);" onclick="sendCursorPos();">                  
            <img width="%(w_)d" height="%(h_)d" src="/index/files/item/%(name)s.gif" border="0" %(shader)s">
        </a>        
    </div>                                                                     '''%params
                    else: data =  '''    
    <div id="gObj%(id)d" class="tooltip" title="%(name)s<br/>DP: %(DP)s%%<br/>Base Value:%(value)d" style="position:absolute;left:%(x_)dpx;top:%(y_)dpx;z-index:%(z_)dpx;"align="left">  
        <a draggable="true" ondragstart="drag(event,%(id)d);" onclick="sendCursorPos();">                  
            <img width="%(w_)d" height="%(h_)d" src="/index/files/item/item.gif" border="0" %(shader)s">
        </a>        
    </div>                                                                     '''%params
                              
                          
        elif self.type=='gate': 
            if mychar_state == -1:
                data = ''
            else:
                params = {'h_':h_ if self.y>0 else 48, 'w_':w_ if self.y>0 else 32, 'y_':y_, 'x_':x_, 'z_':self.y if self.y>0 else 1000,'name':self.name,'id':self.gate.id,'shader':'onload="darken(this,lum,false);' if self.message!='light' else '','image':self.image, 'lum': 'lum' if place.category=="outer" else 0, 'lock':'unlock' if self.gate.locked else 'lock'}
                data = ''' 
    <div onmouseover="$('#g_options%(id)d').css({visibility:'visible','z-index':999999});" onmouseout="$('#g_options%(id)d').css({visibility:'visible','z-index':-1});" >            
    <div id="gObj%(id)d" style="position:absolute;left:%(x_)dpx;top:%(y_)dpx;z-index:%(z_)d;" align="left">  
        <a title="%(name)s">            
            <img width="%(w_)d" height="%(h_)d" src="/index/files/item/%(image)s.gif" border="0" %(shader)s">
        </a>
    </div>
        <div id="g_options%(id)d" style="position:absolute;left:%(x_)d;top:%(y_)d;visibility:hidden;">
            <a href="/index/gate/enter:%(id)d/">
                <img style="position:absolute;left:0px;top:0px;" height="20" src="/index/files/item/icon_enter.gif" border="0"></img>
            </a>
            <a onclick="lock(%(id)d);">
                <img style="position:absolute;left:0px;top:21px;" height="20" src="/index/files/item/icon_%(lock)s.gif" border="0"></img>
            </a>
        </div>
    </div>
                       '''%params
        
        elif self.type=='bag':
            if mychar_state == -1:
                data = ''
            else:
                params = {'h_':h_, 'w_':w_, 'y_':y_, 'x_':x_, 'z_':self.y,'name':self.name,'shader':'onload="darken(this,lum,false);' if self.message!='light' else '','id':self.id,'image':'bag', 'lum': 'lum'}
                data = ''' 
    <div id="gObj%(id)d" style="position:absolute;left:%(x_)d;top:%(y_)d;z-index:%(z_)d" draggable="true" ondragstart="drag(event,%(id)d);" onclick="sendCursorPos();"> 
        <img style="position:absolute;left:0;top:0" width="%(w_)d" height="%(h_)d" src="/index/files/item/%(image)s.gif" %(shader)s">
    </div>
                       '''%params
        
        elif self.type=='container': 
            if mychar_state == -1:
                data = ''
            else:
                params = {'h_':h_, 'w_':w_, 'y_':y_, 'x_':x_, 'z_':self.y,'name':self.name,'shader':'onload="darken(this,lum,false);' if self.message!='light' else '','id':self.id,'image':self.image}
                if not flip:
                    data = ''' 
    <div id="gObj%(id)d" draggable="false" ondragstart="event.preventDefault();" style="position:absolute;left:%(x_)d;top:%(y_)d;z-index:%(z_)dpx;">
        <a href="/index/open/%(id)d/" class="tBox">             
            <img width="%(w_)d" height="%(h_)d" src="/index/files/item/%(image)s.gif" border=0 %(shader)s">
        </a>
    </div>                 '''%params
                else: 
                    data = '''            
        <img id="gObj%(id)d" style="position:absolute;left:%(x_)d;top:%(y_)d;z-index:%(z_)d;" width="%(w_)d" height="%(h_)d" src="/index/files/item/%(image)s.gif" border=0 %(shader)s">
                           '''%params
        
        elif self.type=='workbench': 
            if mychar_state == -1:
                data = ''
            else:
                params = {'h_':h_, 'w_':w_, 'y_':y_, 'x_':x_, 'z_':self.y,'name':self.name,'shader':'onload="darken(this,lum,false);' if self.message!='light' else '','id':self.id,'image':self.image}
                if not flip:
                    data = ''' 
    <div id="gObj%(id)d" style="position:absolute;left:%(x_)dpx;top:%(y_)dpx;z-index:%(z_)d;"align="left">  
        <a href="/index/work/%(id)d/" class="tBox">             
            <img  width="%(w_)d" height="%(h_)d" src="/index/files/item/%(image)s.gif" border=0 %(shader)s">
        </a>
    </div>                       '''%params
                else: 
                    data = '''            
        <img id="gObj%(id)d" style="position:absolute;left:%(x_)d;top:%(y_)d;z-index:%(z_)d;" width="%(w_)d" height="%(h_)d" src="/index/files/item/%(image)s.gif" border=0 %(shader)s">
                           '''%params
                       
        elif self.type=='iBox':
            params = {'char1':self.interactionbox.first.render(place,mychar_id,mychar_state),
                      'char2':self.interactionbox.second.render(place,mychar_id,mychar_state,True)
            }
            data = ''' 
<a href="/index/interact:return/" class="iBox">             
   %(char1)s
   %(char2)s
<a>
                         '''%params
        
        elif self.type=='cBox':
            params = {'char':self.containerbox.first.render(place,mychar_id,mychar_state),
                      'container':self.containerbox.second.render(place,mychar_id,mychar_state,True),
                      'id':self.id
            }
            if mychar_id in (self.containerbox.first.id,self.containerbox.second.id):
                data = ''' 
<a href="/index/open/%(id)d/" class="tBox" >             
   %(container)s
   %(char)s
<a>
                         '''%params
            else:
                 data = '''             
<div id="box%(id)d">             
   %(container)s
   %(char)s
</div>
                         '''%params
        
        elif self.type=='gBox':
            params = {'char':self.genericbox.first.render(place,mychar_id,mychar_state),
                      'container':self.genericbox.second.render(place,mychar_id,mychar_state,True),
                      'id':self.id
            }
            if mychar_id in (self.genericbox.first.id,self.genericbox.second.id):
                data = ''' 
<a href="/index/work/%(id)d/" class="tBox" >             
   %(char)s
   %(container)s
<a>
                         '''%params
            else:
                 data = '''             
<div id="box%(id)d">             
   %(char)s
   %(container)s
</div>
                         '''%params


        elif self.type=='mob':
            if (mychar_state<0 and self.character.state<0) or (mychar_state>=0 and self.character.state>=0):  
                params = {'h_':h_, 'w_':w_, 'y_':y_, 'x_':x_, 'n_pos_x': n_pos[0],'n_pos_y': n_pos[1],'id':self.id,'mychar':mychar_id,'name':self.name,
                    'shader':'onload="darken(this,lum,false);' if self.message!='light' else '',
                    'image':'%s/%s/%s'%('char',self.image,self.character.gender),
                    'shirt':self.character.shirt.name if self.character.shirt else 'blank','pants':self.character.pants.name if self.character.pants else 'blank',
                    'hat':self.character.hat.name if self.character.hat else 'blank',
                    'flip': 'true' if flip else 'false', 
                    'shoutbox':'<span style="position: absolute;color:#000000;background-color:#f0f0f0;font-family:Verdana;font-size:10px;top:%dpx;left:%dpx;white-space: nowrap;z-index:99;">%s</span>'%(n_pos[1]-16,x_+w_/2-2*len(self.character.shoutbox),self.character.shoutbox) if self.character.counter>datetime.datetime.now() else '',
                    'options':'' if mychar_state else '''
        <a onclick="ajaxReq('/index/attack:m/%(mychar)d/%(id)d/');">
            <img style="position:absolute;left:0px;top:0px;height:27px" src="/index/files/item/icon_attack.gif" border="0"></img>
        </a>
        '''%{'id':self.id,'mychar':mychar_id}}
                data =  '''          
    <span style="position:absolute;left:%(n_pos_x)d;top:%(n_pos_y)d;color:#ffffff;font-family:Verdana;font-size:12px;background-color:#24507b;white-space: nowrap;"">
        %(name)s
    </span>

    <div id="gObj%(id)d" onmouseover="document.getElementById('options%(id)d').style.visibility='visible';" onmouseout="document.getElementById('options%(id)d').style.visibility='hidden';" style="position:absolute;left:%(x_)dpx;top:%(y_)dpx;"align="left">  
        <img style="position:absolute;left:0px;top:0px;" height="%(h_)d" width="%(w_)d" src="/index/files/%(image)s/char.gif" onload="darken(this,lum,%(flip)s);">  

        <div id="clothes%(id)d" style="position:absolute;left:0px;top:0px;width="%(w_)d;">
            <img style="position:absolute;left:0px;top:0px;" height="%(h_)d" width="%(w_)d" src="/index/files/%(image)s/%(pants)s.gif" onmouseover="document.getElementById('options%(id)d').style.visibility='visible';" onmouseout="document.getElementById('options%(id)d').style.visibility='hidden';" onload="darken(this,lum,%(flip)s);">
            <img style="position:absolute;left:0px;top:0px;" height="%(h_)d" width="%(w_)d" src="/index/files/%(image)s/%(hat)s.gif" onmouseover="document.getElementById('options%(id)d').style.visibility='visible';" onmouseout="document.getElementById('options%(id)d').style.visibility='hidden';" onload="darken(this,lum,%(flip)s);">
            <img style="position:absolute;left:0px;top:0px;" height="%(h_)d" width="%(w_)d" src="/index/files/%(image)s/%(shirt)s.gif" onmouseover="document.getElementById('options%(id)d').style.visibility='visible';" onmouseout="document.getElementById('options%(id)d').style.visibility='hidden';" onload="darken(this,lum,%(flip)s);">
        </div>
        %(options)s
        
    </div>
                        '''%params
                self.character.creature.aggresive(place)
            else: data=''
        elif self.type=='spawn': 
            self.spawner.spawn(place)
            data=''
        return data

#Skill model for characters                
class Skill(models.Model):
    name = models.CharField(max_length=50) #name
    xp = models.FloatField(max_length=200,default=0) #current experience level of the skill
    value = models.IntegerField(max_length=250)
    type = models.IntegerField(max_length=6)#1:attack,2:defence,3:productive,4:harvest,5:misc,6:undefined
    
    #level_check returns the level up status 
    #with respect to its xp.
    def level_check(self):
        up = 0;
        while self.xp>=100:
            self.xp-=100
            self.value+=1
            up+=1
        self.save()
        return up
    
    #this function is called everytime this skill
    #is used by its owner.
    def use(self,user,cofactor=1):
        if not cofactor==-1:
            self.xp += (cofactor*50)/(self.value+1)
            up = self.level_check()
            user.empty += up
        else: 
            self.value+=1
            user.empty += 1
        self.save()
        return self.value
    
#General class for active/passive skills, magical and biological effects and spells
#TODO: implement scripted spells
class Spell(models.Model):
    name = models.CharField(max_length=50)
    script = models.TextField(null=True)
    word = models.CharField(max_length=50,null=True)
    expired_at = models.DateTimeField(default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)

    def parse(self,target,usr):
        s = self.script.replace('\r','')
        print 'script:',s
        result =''
        exec(s)
        if usr.id!=target.id: 
          print 'You casted %s on %s'%(self.name,target.name)
          usr.notify('You casted %s on yourself'%(self.nam,target.name))
          target.end_turn()
        else:
          print 'You casted %s on yourself'%self.name 
          usr.notify('You casted %s on yourself'%self.name)
        usr.end_turn()
        return result

#Item class
class Item(GenericObject):

    typeclass=models.CharField(max_length=30)#type of the item
    category=models.CharField(max_length=30)#category of the item
    subtype=models.CharField(max_length=15)#subtype of the item
   
    #variables for binding an item to a character
    owner = models.ForeignKey('Character',related_name='owner',null=True)#id of the owner character
    marked = models.BooleanField(default=False)#marking state
    #True or False regarding whether that a character
    #is currently using or possessing this item or not.
    #IDEA: Qitem
    in_use = models.BooleanField()
    status = models.CharField(max_length=10,default='fine') 
    #Usage variables
    DP=models.IntegerField(default=1)#current DP
    a_maxdp= models.IntegerField(default=1)#Maximum DP
    power=models.IntegerField(default=0)#In use effect
    base_spell=models.ForeignKey(Spell,null=True)#magical effect
    #Commerce variables
    value=models.IntegerField(default=0)
    #Crafting data
    #type_id=models.CharFie'pld(max_length=12,blank=True)
    nickname=models.CharField(max_length=50,blank=True)
    
    #function for using items
    def use(self,user,cread=False):
        data = ''
        id = 0
        exec(self.script)
        onUse(self,user);
        if self.typeclass == 'material':#category should be edible, drinkable, unique, solid.
            #TODO: cover other categories
            if self.category == 'edible':
                user.HP += self.effect()
                user.save()
                user.end_turn()
                if self.DP<1: self.delete()
                return 0
        elif self.typeclass == 'document':#category should be the name of the html file! ##book,article,map,printing,note,blueprint.
            #TODO: cover other categories
            if self.category == 'scroll':
                user.learn_spell(Spell.objects.get(id=int(self.subtype)))
            elif self.category=='blueprint':
                exec('m = '+self.blueprint.materials)
                temp=[]
                for k,v in m.iteritems(): 
                    if k!='null' and k!= 'result':
                        temp.append('  %d x %s<br/>'%(v,k))
                content=''.join(temp)
                self.effect() 
                return content
            else:
                try:
                    if cread:
                        exec('m='+self.subtype)
                        for i in m.iterkeys():
                            if m[i][1]>user.get_skill(i)>m[i][0]:
                                user.use_skill(i)
                except:pass
                data = str(self.category)
                self.effect() 
                return data
        elif self.typeclass == 'container':
            data = str(self.id)
            return data
        elif self.typeclass == 'tool' and self.DP>0 and self.status!='unfinished':#Category should be shirt,boots,pants,gloves,hat,shield, blunt, sword, ranged, key or pen
            if self.category in ('blade','blunt','ranged','key','pen'):
                if user.weapon: 
                  user.inventory.add(user.weapon)
                  data = user.weapon.get_name()
                  id = user.weapon.id
                user.weapon=self
            else:
                if not getattr(user,self.category) == None: 
                  user.inventory.add(getattr(user,self.category))
                  data = getattr(user,self.category).get_name()
                  id = getattr(user,self.category).id
                setattr(user,self.category,self)
            if self.category in ('shirt','pants','boots','gloves'): self.effect()
            user.inventory.remove(self)
            if self.w==0 or self.h==0: self.w,self.h = user.w,user.h
            self.save()
        return data,id;
        
    def effect(self,factor=1):
        result = (bool(self.DP))*self.power
        if self.DP>0: 
            self.DP-=factor
            if self.DP<self.a_maxdp/2: self.status=""
        else:
            if self.category in ('shirt','pants','gloves','hat'): self.status='worn'
            elif self.category in ('blade','ranged','blunt'): self.status='broken'
            elif self.category in ('armor','pauldron','greaves'): self.status='tattered'
            else: self.status=''
        self.save()
        return result
        
    def repair(self,crafter):

        if self.status=='unfinished':
            if self.subtype=='metal':self.DP += (self.a_maxdp*crafter.use_skill('Blacksmithing'))/200
            elif self.subtype=='metal':self.DP += (self.a_maxdp*crafter.use_skill('Tailoring'))/200
            if self.category in ('shirt','pants','gloves','hat'): 
                    if crafter.get_skill('Tailoring')<25: self.status='patched'
                    else: self.status=''
            elif self.category in ('blade','ranged','blunt','armor','greaves'): 
                    if crafter.get_skill('Blacksmithing')<25: self.status='crooked'
                    else: self.status=''
            else: self.status=''
        else:
            self.DP += (self.a_maxdp*crafter.s_smt.use(crafter))/200
            if self.DP>=self.a_maxdp: self.status='fine'
        crafter.FP -=80
        crafter.end_turn()
        if self.DP>self.a_maxdp: self.DP=self.a_maxdp
        self.save()

    def copy(self):
        initial = dict([(f.name, getattr(self, f.name)) for f in self._meta.fields if not isinstance(f, models.AutoField) and not f in self._meta.parents.values()])
        return self.__class__(**initial)
    
    def delete(self):
        p=Item.objects.filter(name=self.name)
        last=len(p)
        super(Item,self).delete()
        if last==1:
            self.in_use=False
            self.marked=False
            self.nickname=''
            self.DP=self.a_maxdp
            self.save()
            
    def get_name(self):
        owner_info=''
        status_info=''
        if self.nickname != '': return self.nickname
        else:
            if self.marked: owner_info = self.owner.name+'\'s '
            status_info='%s '%self.status if self.category != 'key' and self.typeclass not in ('material','document') and self.type != 'bag' else '' 
        if self.typeclass == 'material':
            if self.a_maxdp>2*self.DP: self.status = "";
            if self.DP>1: status_info = '(%dx)'%self.DP
            elif not self.marked: status_info = 'an ' if self.name[0] in ('a','e','i','o','u') else 'a '
        if self.category=='edible' and self.DP>1: return '%s%s%s'%(owner_info, self.name, status_info)
        else: return '%s%s%s'%(owner_info, status_info, self.name)

    def transfer(self,frm,to,amount):
        if self.typeclass=='material':
                if self.DP > amount:
                    self.DP-=amount
                    self.save()
                    try: it = to.filter(name=self.name).filter(category=self.category)[0]
                    except: it = None
                    if it: 
                        it.DP += amount
                        it.save()
                    else:
                        new = self.copy()
                        new.DP = amount
                        new.save()
                        to.add(new)
                elif self.DP == amount:
                    frm.remove(self)
                    try: it = to.filter(name=self.name).filter(category=self.category)[0]
                    except: it = None
                    if it: 
                        self.delete()
                        it.DP += amount
                        it.save()
                    else:
                        to.add(self)
                else: pass
        else:
                frm.remove(self)
                to.add(self)    

#Key class
class Key(Item):
    gate_id = models.IntegerField()
    persistent = models.BooleanField(default=True)
    
#Money class
class MoneyBag(Item):
    
    #Money Currencies:
    #A silver Imperial Volan is 100 copper Imperial Orns.
    Volans = models.IntegerField()
    Orns = models.IntegerField()
    
    def total(self):
        return 100*self.Volans+self.Orns
    
    def add(self,v=0,o=0):#give
        self.Volans += v
        self.Orns += o
        self.save()
    
    def sub(self,v=0,o=0):#take
        self.Volans -= v
        self.Orns -= o
        self.save()
        
    def merge(self,other):#add
        self.Volans += other.Volans
        self.Orns += other.Orns
        other.delete()
        self.save()
        
#Container class:
class Container(Item):

    items = models.ManyToManyField(Item,related_name="contains")
    size = models.IntegerField(default=60)    
    persistent = models.BooleanField(default=False)
        
#NPC Topics Class
#Will be extensively used in Quest system
class Topic(models.Model):
    title = models.CharField(max_length=60)
    request = models.TextField()
    response = models.TextField()
                
#Character class                
class Character(GenericObject):

    #fundamental character properties
    race = models.CharField(max_length=20)
    gender = models.CharField(max_length=2)
    hair = models.IntegerField(default=0)
    face = models.IntegerField(default=0)
    facial = models.IntegerField(default=0)
    level = models.IntegerField(max_length=100)
    #functional properties
    action = models.CharField(max_length=8,default='idle')
    state = models.IntegerField()#state checks if characer is capable of doing any action
    user = models.ForeignKey(User,null=True)
    #travelling properties
    current_place = models.IntegerField()#id of the current place
    destination_place = models.IntegerField()#id of the destination
    time_left = models.DateTimeField(null=True)#time left for arrival
    #Money bag
    bag = models.ForeignKey(MoneyBag,related_name='mybag')
    #equipped items
    shirt = models.ForeignKey(Item,null=True,related_name='shirt')
    pants = models.ForeignKey(Item,null=True,related_name='pants')
    boots = models.ForeignKey(Item,null=True,related_name='boots')
    gloves = models.ForeignKey(Item,null=True,related_name='gloves')
    hat = models.ForeignKey(Item,null=True,related_name='hat')
    armor = models.ForeignKey(Item,null=True,related_name='armor')
    pauldrons = models.ForeignKey(Item,null=True,related_name='paunldrons')
    greaves = models.ForeignKey(Item,null=True,related_name='greaves')
    mask = models.ForeignKey(Item,null=True,related_name='mask')
    cape = models.ForeignKey(Item,null=True,related_name='cape')
    #hand items
    hand = models.ForeignKey(Item,null=True,related_name='in hand')
    weapon = models.ForeignKey(Item,null=True,related_name='weapon')
    shield = models.ForeignKey(Item,null=True,related_name='shield')
    #shouting
    shoutbox = models.CharField(max_length=80,null=True)
    #render control
    has_update = models.DateTimeField(default=datetime.datetime.now());
    
    a_str=models.IntegerField()#strength
    a_int=models.IntegerField()#intelligence
    a_dex=models.IntegerField()#dexterity
    a_wis=models.IntegerField()#wisdom
    a_sta=models.IntegerField()#stamina
    a_luk=models.IntegerField()#luck
    empty=models.IntegerField()#distributable stats
    
    HP=models.IntegerField()#current HP
    a_maxhp= models.IntegerField()#Maximum HP
    MP=models.IntegerField()#current MP
    a_maxmp=models.IntegerField()#Maximum MP
    FP=models.IntegerField()#current FP
    a_maxfp=models.IntegerField()#Maximum FP
    
    inventory = models.ManyToManyField(Item)
    spellbook = models.ManyToManyField(Spell,related_name='spellbook')
    blueprints = models.ManyToManyField('Blueprint',related_name="memorized")
    readyspell = models.ForeignKey(Spell,related_name='readyspell',null=True)
    skills = models.ManyToManyField(Skill,related_name="misc_skills")
    effects = models.ManyToManyField(Spell,related_name='active_effects')
    
    share_box = models.ManyToManyField(Item,related_name='tfbox')
    
    skill_xp=models.IntegerField(max_length=15,default=0)
    
    #Character initialization
    @staticmethod
    def init(request,name,race,sex,stats,appereance,attacks,defences,productives,harvest,miscs,perks):
        #create a money bag
        bag = MoneyBag.objects.create(Volans=1,Orns=15,x=0,y=0,w=50,h=25,name='bag',type='bag',value='115',DP=115,a_maxdp=115)
        bag.save()
        #create the object
        chr = Character.objects.create(name=name,type='char' if name is not 'NPC' else 'npcChar',race=race,gender=sex,image=race,current_place=1,destination_place=1, bag = bag,x=randint(70,550),y=randint(330,385),w=0,h=0,user=request.user,state=0,empty=0,a_str=stats[0],a_int=stats[1],a_dex=stats[2],a_sta=stats[3],a_wis=stats[4],a_luk=stats[5],HP=1,MP=1,FP=1,a_maxhp=1,a_maxmp=1,a_maxfp=1,level=1)
        chr.race=race
        chr.gender=sex
        
        #set appereance
        chr.hair, chr.face, chr.facial = appereance
        
        #Add skillset
        skill=Skill.objects.create(name='Athletics',value=randint(10,20),type=4)
        skill=Skill.objects.create(name='Speechcraft',value=randint(10,20),type=4)
        for e in attacks:
            skill=Skill.objects.create(name=e,value=randint(15,25),type=1)
            skill.save()
            chr.skills.add(skill)
        for e in defences:
            skill=Skill.objects.create(name=e,value=randint(15,25),type=2)
            skill.save()
            chr.skills.add(skill)
        for e in productives:
            skill=Skill.objects.create(name=e,value=randint(10,20),type=3)
            skill.save()
            chr.skills.add(skill)
        skill=Skill.objects.create(name=harvest,value=randint(10,20),type=4)
        skill.save()
        chr.skills.add(skill)    
        for e in miscs:
            skill=Skill.objects.create(name=e,value=randint(5,20),type=5)
            skill.save()
            chr.skills.add(skill)
        for e in perks:
            perk=Spell.objects.create(name=e)
            perk.save()
            chr.effects.add(perk)
        
        #edit innate abilities
        if chr.race=='Dark Elf':
            if chr.name is 'NPC' and chr.gender is 'f': chr.name = def_names[randint(0,14)]+'[NPC]'
            elif chr.name is 'NPC' and  chr.gender is 'm': chr.name = dem_names[randint(0,25)]+'[NPC]'
            if chr.gender == 'm': chr.w,chr.h = 61,113
            else: chr.w,chr.h = 43,103
        elif chr.race=='Mauron':
            if chr.name is 'NPC' and chr.gender is 'f': chr.name = def_names[randint(0,14)]+'[NPC]'
            elif chr.name is 'NPC' and  chr.gender is 'm': chr.name = dem_names[randint(0,25)]+'[NPC]'
            if chr.gender is 'm': chr.w,chr.h = 89,96
            else: chr.w,chr.h = 0,0
        elif chr.race=='Night Elf':
            if chr.name is 'NPC' and chr.gender is 'f': chr.name = def_names[randint(0,14)]+'[NPC]'
            elif chr.name is 'NPC' and  chr.gender is 'm': chr.name = dem_names[randint(0,25)]+'[NPC]'
            if chr.gender == 'm': chr.w,chr.h = 61,113
            else: chr.w,chr.h = 43,103
            chr.set_skill('Elven',50)
            chr.set_skill('Imperial',20)
            chr.set_skill('Merchantile',10)
        elif chr.race=='Heartland Elf':
            if chr.name is 'NPC' and chr.gender is 'f': chr.name = def_names[randint(0,14)]+'[NPC]'
            elif chr.name is 'NPC' and  chr.gender is 'm': chr.name = dem_names[randint(0,25)]+'[NPC]'
            if chr.gender == 'm': chr.w,chr.h = 61,113
            else: chr.w,chr.h = 43,103
            chr.set_skill('Elven',55) 
            chr.set_skill('Imperial',20)
        elif chr.race=='High Elf':
            if chr.name is 'NPC': chr.name = hef_names[randint(0,14)]+'[NPC]'
            if chr.gender is 'm': chr.w,chr.h = 59,141
            else: chr.w,chr.h = 57,138
            chr.set_skill('Elven',65) 
            chr.set_skill('Imperial',10)
        elif chr.race=='Human':
            if chr.name is 'NPC': chr.name = hum_names[randint(0,18)]+'[NPC]'
            if chr.gender is 'm': chr.w,chr.h = 59,117
            else: chr.w,chr.h = 59,117
            chr.set_skill('Imperial',50) 
        elif chr.race=='Orc':
            if chr.gender is 'm': chr.w,chr.h = 72,145
            else: chr.w,chr.h = 54,120
            if chr.name is 'NPC': chr.name = orm_names[randint(0,14)]+'[NPC]'
            chr.set_skill('Orcish',40) 

        chr.a_maxhp=(chr.a_str*3.75+chr.a_dex*1.25+chr.a_sta*2.00+chr.a_luk*1.00)
        chr.HP=chr.a_maxhp
        
        chr.a_maxmp=(chr.a_int*4.00+chr.a_sta*0.75+chr.a_wis*2.25+chr.a_luk*1.00)
        chr.MP=chr.a_maxmp

        chr.a_maxfp=(chr.a_str*1.50+chr.a_dex*1.50+chr.a_sta*4.00+chr.a_luk*1.00)*10
        chr.FP=chr.a_maxfp

        chr.image = chr.race
        
        p=Place.objects.get(id=1)
        p.people.add(chr)
        
        #create generic items
        lpants=Item.objects.create(name='Leather Pants',type='item',category='pants',typeclass='tool',subtype='wear',value=50,x=0,y=0,marked=False,DP=15000,a_maxdp=15000,w=25,h=50,image='item')
        lpants.save()
        bshirt=Item.objects.create(name='Blue Shirt',type='item',category='shirt',typeclass='tool',subtype='wear',value=50,x=0,y=0,marked=False,DP=10000,a_maxdp=10000,w=25,h=50,image='item')
        bshirt.save()
        hpot=Item.objects.create(name='health potion',type='item',category='edible',typeclass='material',subtype='drink',value=10,x=0,y=0,marked=False,DP=1,a_maxdp=1,power=10,w=25,h=50,image='item')
        hpot.save()
        baga=Container.objects.create(name='leather bag',type='container',category='leather',typeclass='medium',subtype='bag',value=18,x=0,y=0,marked=False,DP=1,a_maxdp=1,power=10,w=40,h=40,image='leather bag')
        baga.save()
    
        chr.shirt=bshirt
        chr.pants=lpants
        chr.inventory.add(hpot)
        chr.inventory.add(baga)
        
        chr.save()
        
        return chr
    
    def get_skill(self,n):
        try: return self.skills.get(name=n).value
        except: return 0

    def set_skill(self,n,v):
        try: 
            s = self.skills.get(name=n);
            print "skill: %s, val:%d"%(s.name,s.value)
            s.value = v;
            if(s.value<=0):
              print "removing skill"
              s.delete()
            else:
              s.save();
        except: 
            #TODO:probable inconsistency,check with views
            print "new skill"
            s=Skill.objects.create(name=n,type=5,value=v);
            s.save()
            self.skills.add(s);
            return s.value

    def use_skill(self,n):
        try: 
            s = self.skills.get(name=n)
            s.use(self);
            return s.value
        except: 
            s=Skill.objects.create(name=n,type=5,value=2);
            s.save()
            self.skills.add(s);
            return s.value


    def notify(self,message):
      prd('notification%d'%self.id,message)

    def travel_check(self,__place):
        p1=Place.objects.get(id=self.current_place)
        can_go=True
        #delete the current interraction box
        try:
            iBox=InteractionBox.objects.get(first=self)
            other = iBox.second
        except InteractionBox.DoesNotExist: 
            try:
                iBox=InteractionBox.objects.get(second=self)
                other= iBox.first
            except InteractionBox.DoesNotExist: pass
            
        try:
            cBox=ContainerBox.objects.get(first=self)
            cBox.decompose()
        except ContainerBox.DoesNotExist: pass
        
        try:
            gBox=GenericBox.objects.get(first=self)
            gBox.decompose()
        except GenericBox.DoesNotExist: pass
        
        try:
            if iBox.balance>=0:
                iBox.decompose()
            else: can_go=False
        except: pass
        self.end_turn()
        if not self.FP: can_go=False
        return can_go
        
    def travel(self,place):
        self.state=0 if self.state>0 else self.state
        p = Place.objects.get(id=self.current_place)
        p.people.remove(self)
        if self.action=='travel':
            try: distance = Path.objects.filter(cell0=p).filter(cell1=place)[0].distance
            except: distance = Path.objects.filter(cell0=place).filter(cell1=p)[0].distance
        else: distance = 0
        self.current_place=place.id
        place.people.add(self)
        place.save()
        p.save()
        self.current_place=self.destination_place
        self.action='idle'
        self.FP -= distance//100
        self.x,self.y = randint(130,430), randint(p.horizon+50,int(p.horizon+p.depth*2.0/3))
        
        prd('render'+str(int(p.id)),simplejson.dumps({'action':'travel','destination':place.id,'id':self.id}))
        prd('render'+str(int(place.id)),simplejson.dumps({'action':'travel','destination':place.id,'id':self.id,'data':self.render(place,self.id,self.state)}))
        try:
            self.skill_xp+=self.s_ath.use(self,distance/250)[0]   
        except: pass
        f=distance//500
        if f>0:
            for e in (self.shirt,self.pants,self.boots):
                if e: e.effect(f)
                f = f*4
        print "action:",self.action
        self.save()

    def interact(self,contact):
        try:self.s_spc.use(self)
        except:pass 
        place=Place.objects.get(id=self.current_place)
        if contact.current_place==self.current_place and self.state==0 and contact.state==0:
            if contact.x>400:
                iBox = InteractionBox(name='%s and %s'%(contact.name,self.name),type='iBox',first=self,second=contact,current_place=contact.current_place,x=0,y=0,w=1,h=1)
            elif self.x>400:
                iBox = InteractionBox(name='%s and %s'%(contact.name,self.name),type='iBox',first=contact,second=self,current_place=contact.current_place,x=0,y=0,w=1,h=1)
            else:
                iBox = InteractionBox(name='%s and %s'%(contact.name,self.name),type='iBox',first=self,second=contact,current_place=contact.current_place,x=0,y=0,w=1,h=1)

            contact.state=1
            self.state=1
            iBox.first.x, iBox.first.y = iBox.second.x + iBox.first.w, iBox.second.y
            iBox.first.save()
            place.people.remove(contact)
            place.people.remove(self)
            iBox.y = self.y
            iBox.save()
            place.people.add(iBox)
            contact.save()
            self.save()
            place.save()
            
    def move(self,place):
        #delete the current interraction box
        try:
            iBox=InteractionBox.objects.get(first=self)
            iBox.decompose()
        except InteractionBox.DoesNotExist: 
            try:
                iBox=InteractionBox.objects.get(second=self)
                iBox.decompose()
            except InteractionBox.DoesNotExist: pass
            
        try:
            cBox=ContainerBox.objects.get(first=self)
            cBox.decompose()
        except ContainerBox.DoesNotExist: pass
        self.state=0 if self.state>0 else self.state
        self.action='idle'
        p=Place.objects.get(id=self.current_place)
        p.people.remove(self)
        place.people.add(self)
        self.current_place=place.id
        self.save()
        place.save()
        p.save()
        
    def interrupt(self):
        try:
            iBox = InteractionBox.objects.get(first=self)
            iBox.decompose()
        except: 
            iBox = InteractionBox.objects.get(second=self)
            iBox.decompose()
    
    def attack(self,opp):
        
            def dist(a,b): return int(((a.x-b.x)**2+(a.y-b.y)**2)**0.5)
            
            cstr=self.a_str
            cint=self.a_int
            cdex=self.a_dex
            cluk=self.a_luk

            osta=opp.a_sta
            oint=opp.a_int
            odex=opp.a_dex
            oluk=opp.a_luk

            fname= 'his' if self.gender=='m' else 'her'
            fist=Item.objects.create(name='fist',type='item',category='weapon',typeclass='tool',value=2,x=0,y=0,w=0,h=0,marked=False,DP=30,a_maxdp=30,power=1)
            fist.save()
            used_item = self.weapon if self.weapon else fist

            if used_item:
                rfactor=1
                ceffect=e*log(used_item.effect()+1)
                if used_item.category=='blade':
                    cfactor=self.use_skill('Swordmanship')
                    action_spec = choice(['cuts','slits'])
                elif used_item.category=='blunt':
                    cfactor=self.use_skill('Blunt Weapon')
                    action_spec = choice(['hits','crushes'])
                elif used_item.category=='ranged':
                    cfactor=self.use_skill('Marksmanship')
                    action_spec = 'shoots'
                    rfactor=0
                else:
                    cfactor=self.use_skill('Hand to Hand')
                    action_spec = choice(['punches','hits'])
                oarmors = [opp.shield, opp.gloves , opp.pants , opp.shirt , opp.hat]
                owhere = ['shoulder' if opp.shield is None else 'shield', choice(['right hand','left hand']), choice(['right leg','left leg']), choice(['chest','abdomen','groins']) , choice(['face','right temple' , 'neck', 'left ear'])]
                select = randint(0,4)
                ohitby = oarmors[select]
                where=owhere[select]
                oeffect= (ohitby.effect(cfactor+cstr*4)*4 if ohitby else 4)-select
                ofactor= (opp.use_skill('Armor') if not ohitby else opp.use_skill('Unarmored')) + opp.use_skill('Dodging')
                vfactor= randint(50,100)/2
                res = int(vfactor*(cstr*0.6+cdex*0.3+cluk*0.1)*(ceffect*0.65)*cfactor/250 - (osta*0.2+odex*0.7+oluk*0.1)*(oeffect)*ofactor/100)
                if res<0 or (dist(self,opp)>100 and not used_item.category=='ranged'): 
                  res=0.5
                else:
                    opp.HP -= res
                    opp.state=90
                opp.end_turn()
                self.save()
                rstring = [where,'%s %s'%(fname,used_item.name),res,action_spec]
                fist.delete()
                return rstring
            elif self.used_spell: pass
            
    
    def receive_effect(self,base,effect):
        
        self.setattr(base, self.setattr(base) + effect)
        
        
    def end_turn(self):

        if self.MP>self.a_maxmp: self.MP=self.a_maxmp
        elif self.MP<0: self.MP=0

        if self.FP>self.a_maxfp: 
            self.FP=self.a_maxfp
            self.action="idle"
        elif self.FP<0: 
            self.FP=0

        if self.HP>self.a_maxhp: self.HP=self.a_maxhp
        elif self.HP<=0 and self.state>-1: 
            self.HP=0
            self.state=-1
            self.save()
            place=Place.objects.get(id=self.current_place)
            if self.type=="creature": 
                spw = Spawner.objects.get(spawnt_type=self.creature.type_id)
                spw.max+=1;
            corpse=Container.objects.create(name='corpse',image='corpse',size=100,type='container', typeclass='container',y=self.y,x=self.x,w=100,h=30,marked=True,owner=self)
            if (self.bag.total())>0:
                abag = MoneyBag.objects.create(Volans=self.bag.Volans,Orns=self.bag.Orns,y=self.y+5,x=self.x+randint(-10,10),w=40,h=25,name=(('%s Volans and '%self.bag.Volans) if self.bag.Volans>0 else '') + '%d Orns'%self.bag.Orns,type='bag',value=100*self.bag.Volans+self.bag.Orns,DP=2,a_maxdp=2)
                self.bag.sub(self.bag.Volans,self.bag.Orns)
                self.bag.save()
                corpse.items.add(abag)
                
            for item in self.inventory.all():
                self.inventory.remove(item)
                item.in_use=False
                item.marked=False
                item.save()
                corpse.items.add(item)
            for item in (self.shirt,self.pants,self.hat,self.shield,self.boots,self.armor,self.pauldrons,self.greaves,self.shield,self.gloves):
                if item:
                    setattr(self,item.category,None)
                    item.in_use=False
                    item.marked=False
                    item.save()
                    corpse.items.add(item)
            if self.weapon: 
                corpse.items.add(self.weapon)
                self.weapon=None

            organ=Item.objects.create(name='heart',type='item',category='edible',typeclass='material',value=25,x=0,y=0,marked=True,owner=self,DP=1,a_maxdp=1,power=5,w=25,h=50,image='item')
            organ.save() 
            corpse.items.add(organ)     
            organ=Item.objects.create(name='liver',type='item',category='edible',typeclass='material',value=20,x=0,y=0,marked=True,owner=self,DP=1,a_maxdp=1,power=8,w=25,h=50,image='item')
            organ.save() 
            corpse.items.add(organ) 
            organ=Item.objects.create(name='eye',type='item',category='edible',typeclass='material',value=10,x=0,y=0,marked=True,owner=self,DP=1,a_maxdp=1,power=1,w=25,h=50,image='item')
            organ.save()
            corpse.items.add(organ)

            corpse.save()
            place.people.add(corpse)
            place.save()
            self.move(Place.objects.get(id=10))
            self.save() 
            
        self.save()

    def learn_spell(self,spell):
        if spell not in self.spellbook.all():
            self.spellbook.add(spell)
            self.save()
            return 1
        return 0
    
        
    def return_all(self):
        return {'name':self.name,'race':self.race,'gender':self.gender,'str':self.a_str,'int':self.a_int,
        'dex':self.a_dex,'wis':self.a_wis,'sta':self.a_sta,'luk':self.a_luk,'empty':self.empty,'level':self.level,'dist': self.empty,
        'HP':self.HP,'MP':self.MP,'FP':int(self.FP/10),'maxHP':self.a_maxhp,'maxMP':self.a_maxmp,'maxFP':int(self.a_maxfp/10),'hat':self.hat,
        'shirt':self.shirt,'gloves':self.gloves,'pants':self.pants,'boots':self.boots,'pauldrons':self.pauldrons,'cape':self.cape,
        'beard':self.facial,'hair':self.hair,'face':self.face,
        'weapon':self.weapon,'armor':self.armor,'greaves':self.greaves,'mask':self.mask,'shield':self.shield,'action':self.action}
 
    def return_skills(self):
        return self.skills.all()

    def level_up(self):
        #purple spaces
        if self.xp>=10:
            self.xp-=10
            self.level+=1
            self.empty+=1
            self.save()
    #cell state functions 
    def crs(self):#Change Render State
        self.has_update = Place.objects.get(id=self.current_place).has_update
        self.save()
        
    def cgrs(self):#Change Global(Cell) Render State
        Place.objects.get(id=self.current_place).save()
        self.save()
        
    def rrs(self):#Return Render State
        return self.has_update >= Place.objects.get(id=self.current_place).has_update
        self.save()
        
            
class NPC(models.Model):
    topics = models.ManyToManyField(Topic,null=True)
    is_shopkeeper = models.BooleanField()
    char = models.ForeignKey(Character,related_name='chr1')
    disposition = models.TextField(default='{}')
    
    def operate_char(self):
            op = choice([0,1,2,3,4,2,2,8])
            eCode=0
            p=Place.objects.get(id=self.char.current_place)
            if not self.is_shopkeeper:
                    if op==0 and not self.char.state and not self.char.action=='travel':
                        where = p.connection.all()
                        p2 = choice(where)
                        if self.char.travel_check(p2): 
                            try: distance = Path.objects.filter(cell0=p).filter(cell1=p2)[0].distance
                            except: distance = Path.objects.filter(cell0=p2).filter(cell1=p)[0].distance
                            t_amount = int(distance*1.0/self.char.get_skill('Athletics'))
                            self.char.time_left = datetime.datetime.now() + datetime.timedelta(seconds=t_amount)
                            self.char.move(p2)
                            #self.char.action = 'travel'
                            self.char.save()
                    if op==1 and not self.char.action=='travel':
                        n= choice(p.people.filter(type='npcChar'))
                        if not n.character==self.char: self.char.interact(n.character)
                        eCode=1
                    if op==2 or (not op==1 and self.char.state>0):
                        try: self.char.interrupt()
                        except: pass
                    if op==3:
                        if self.char.state<1:
                            self.char.x, self.char.y = randint(130,430), randint(p.horizon+50,(p.horizon+p.depth*2.0/3))
                            self.char.save()
                        
                    if op==4 and not self.char.state and not self.char.action=='travel':
                        gates = Gate.objects.filter(current_place=self.char.current_place)
                        if len(gates)>0: 
                            gate = choice(gates)
                            if not gate.locked: self.move(Place.objects.get(gate.route))

            if self.char.action=='travel' and self.char.time_left<datetime.datetime.now():
                self.char.action='idle'
                self.char.save()
            p.save()
            return eCode
    
    def add_topic(self,req,rsp,ttl):
        t = Topic.objects.create(request=req,response=rsp,title=ttl)
        t.save()
        self.topics.add(t)

    def add_existing_topic(self,topic_id):
        t = Topic.objects.get(id=topic_id)
        self.topics.add(t)

class Place(models.Model):
    
    name = models.CharField(max_length=80)
    category = models.CharField(max_length=10)
    connection = models.ManyToManyField('self',symmetrical=True)
    depth = models.IntegerField()
    horizon = models.IntegerField()
    people = models.ManyToManyField(GenericObject,related_name='people outside')
    has_update = models.DateTimeField(auto_now=True)
    
    harvests = models.ManyToManyField('Harvest')
    
    def insert(self,other,n,i,x,y,w,h,xi,yi,wi,hi):
        p = Place.objects.get(id=other)
        g1 = Gate.objects.create(name=n, image=i, x=x,y=y,w=w,h=h,type='gate',current_place=self.id,route=other)
        g2 = Gate.objects.create(name=self.name, image='door', x=xi,y=yi,w=wi,h=hi,type='gate',current_place=self.id,route=self.id)
        g1.save()
        g2.save()
        g1.mirror = g2.id
        g2.mirror = g1.id
        g1.save()
        g2.save()
        self.people.add(g1)
        p.people.add(g2)
        m_key = Key.objects.create(name='%s Key'%n,type='item',category='key',typeclass='tool',subtype='lock',gate_id=g2.id*g1.id,marked=False,value=7,x=randint(100,550),y=randint(330,390),DP=10000,a_maxdp=10000,w=20,h=20)
        m_key.save()
        p.people.add(m_key)
        
    def crs(self):
        self.save()
        return self.has_update
        
    def connect(self, other, dist):
        p = Path.objects.create(distance=dist,cell0=self,cell1=other)
        other.connection.add(self)
        p.save()

class Gate(GenericObject):
    
    current_place = models.IntegerField()
    route = models.IntegerField(null=True)
    mirror = models.IntegerField(null=True)
    locked = models.BooleanField(default=False)
    #knocked = models.IntegerField(default=0)
   
#Road model    
class Path(models.Model):
    cell0 = models.ForeignKey('Place',related_name='p1')
    cell1 = models.ForeignKey('Place',related_name='p2')
    distance = models.IntegerField(default=0) #distance in meters

class Veichle(Place):
    is_veichle = models.BooleanField(default=True)
    route = models.IntegerField()

    def move(self):
        gate = Gate.objects.get(route=self.id)
        p1 = Place.objects.get(id=gate.current_place)
        p2 = Place.objects.get(id=self.route)
        p1.people.remove(gate)
        p2.people.add(gate)
        gate.current_place = p2.id
        gate.save()
        self.name= ''.join([self.name.split(' ')[0],' at %s'%p2.name])
        gate = Gate.objects.get(current_place=self.id)
        gate.route = p2.id
        gate.save()
        self.route = p1.id
        self.save()
        p1.save()
        p2.save()

class InteractionBox(GenericObject):

    first = models.ForeignKey(Character,related_name='talker')
    second = models.ForeignKey(Character,related_name='listener', null=True)
    message_box = models.TextField()
    current_place = models.CharField(max_length=50,blank=True)
    balance=models.IntegerField(default=0)#For trade actions

    def decompose(self):
        p=Place.objects.get(id=self.current_place)
        self.first.state = 0
        self.second.state = 0
        self.first.action = 'idle'
        self.second.action = 'idle'
        self.first.save()
        self.second.save()
        for item in self.first.share_box.all():
            if item.category=='edible': item.transfer(self.first.share_box,self.first.inventory,item.DP)
            else: self.first.inventory.add(item)
            self.first.share_box.remove(item)
        for item in self.second.share_box.all():
            if item.category=='edible': item.transfer(self.second.share_box,self.second.inventory,item.DP)
            else: self.second.inventory.add(item)
            self.second.share_box.remove(item)
        self.delete()
        p.save()
        
    
    def __unicode__(self):
        messages = self.message_box
        if self.second.type=='npcChar':
            replist=['%name','%gender','%race','%line']
            for e in replist:
                if e=='%line': messages= messages.replace(e,'\n')
                elif not e=='%gender':
                   messages= messages.replace(e,eval('str(self.second.'+e[1:]+')'))
                else:
                    if self.second.gender=='m': messages= messages.replace(e,'male')
                    else:messages= messages.replace(e,'female')
        return messages

class Creature(Character):

    type_id = models.CharField(max_length=10,null=True)
        
    #Creature initialization
    @staticmethod
    def init_creature(name,race,sex,mod=0): pass;

    def aggresive(self,cell):
        if randint(0,2):
            #local constants
            available=0
            intact=1
            #fetch the characters
            otherone  = choice([e for e in cell.people.all() if e.type in ('char','npcChar','mob')])
            self.x, self.y = otherone.x + randint(-40,40), otherone.y+15 if otherone.y>330 else otherone.y-15
            self.save();
            self.attack(otherone.character);
            
     
    @staticmethod
    def clone(creature_id):
        cret = Creature.objects.filter(type_id=creature_id)[0]
        c_new = Creature.init_creature(cret.name,cret.race,cret.gender)
        return c_new
        

#Creature spawner Object.
#Spawns a creature of given unique_id
#between given interval if creatures in 
#the cell is less than max    
class Spawner(GenericObject):
    spawn_type = models.CharField(max_length=10,default=-1)
    interval = models.IntegerField()
    max = models.IntegerField();
    
    def bind_creature(self,c):
        id_t = self.create_type_id(self.id)
        if self.spawn_type==-1:
            c.type_id, self.spawn_type = id_t,id_t
        else:
            self.spawn_type = c.type_id 
        c.save()
        self.save()
    
    @staticmethod
    def create_type_id(id):
        return '%s%s%s%d%s%4.4d' %(choice([chr(e) for e in range(97,123)+range(65,91)]) ,
                                  choice([chr(e) for e in range(97,123)+range(65,91)]) ,
                                  choice([chr(e) for e in range(97,123)+range(65,91)]) ,
                                  randint(10,99) ,
                                  choice([chr(e) for e in range(97,123)]) ,
                                  id)
    
    def spawn(self,cell): 
        if self.max>0:
            cret = Creature.clone(self.spawn_type)
            cell.people.add(cret)
            cret.currenp_place=cell.id
            cret.save()
            cell.crs()
            self.max -=1;
            self.save()
    
    
class ContainerBox(GenericObject):

    first = models.ForeignKey(Character,related_name='player')
    second = models.ForeignKey(Container,related_name='container', null=True)
    current_place = models.CharField(max_length=50,blank=True)

    def decompose(self):
        p=Place.objects.get(id=self.current_place)
        p.people.add(self.first)
        p.people.remove(self)
        self.first.state=0
        self.first.save()
        if not self.second.persistent:
            if self.second.items.count()>0:
                self.second.save()
                p.people.add(self.second)
            else:
                self.second.delete()
        else:
            self.second.save()
            p.people.add(self.second)
        p.save()
        try: self.delete()
        except: pass

class GenericBox(GenericObject):

    first = models.ForeignKey(Character,related_name='worker')
    second = models.ForeignKey(GenericObject,related_name='project', null=True)
    current_place = models.CharField(max_length=50,blank=True)

    def decompose(self):
        p=Place.objects.get(id=self.current_place)
        p.people.add(self.first)
        p.people.remove(self)
        self.first.state=0
        self.first.save()
        p.people.add(self.second)
        p.save()
        try: self.delete()
        except: pass

#Harvesting handler
class Harvest(models.Model):

    name = models.CharField(max_length=30) #name of the action
    container = models.ForeignKey(Item) #Item to be harvested
    amount = models.IntegerField(default=99999) #amount of the items
    interval = models.IntegerField(default=60) #amount of time for harvesting
    handler = models.CharField(max_length=10, null=True) #Item type required for harvesting
        
    def start_harvest(self,harvester):
        char_handler = 'Gathering' if not harvester.weapon else harvester.weapon.subtype 
        if self.amount>0 and char_handler==self.handler and harvester.FP>=self.interval/4:
            if not char_handler=='Gathering':
                s=harvester.get_skill(char_handler)
            else: s=1
            return (True,int(2*self.interval*(101-s/100.0)),self.amount)
        else: 
            if self.amount<0: return (False,0,0)
            if char_handler!=self.handler: return (False,0,1)
            if harvester.FP<self.interval/4: return (False,0,2)

#Crafting handlers        
class Workbench(GenericObject):
    skill_type = models.CharField(max_length=25)
    power = models.IntegerField(max_length=100)
        
class Blueprint(Item):

    item = models.ForeignKey(Item,related_name="crafted");
    req_skill_type = models.CharField(max_length=25)
    req_skill_amount = models.IntegerField(max_length=100)
    materials=models.CharField(max_length=120)
   
    def get_materials(self):
        m = eval(self.materials)
        return m.items()
    
    def create_project(self,crafter,bench):
        def flush(inv,crafter):
            for item in inv.all():
                    crafter.inventory.add(item)
                    inv.remove(item)
        
        inv = crafter.inventory

        if crafter.get_skill(self.req_skill_type)>self.req_skill_amount and self.req_skill_type==bench.skill_type:
            exec('m='+self.materials)
            n={}
            try:
                for k,v in m.iteritems():
                    if k != 'null' and k != 'result':
                        s=inv.get(name=k)
                        n[s] = v
                        if s.DP<v: return (-2,None)
            except: return (-2,None)
            for k,v in n.iteritems():
                if k.typeclass=='material': 
                    k.DP-=v
                    k.save()
                else: k.delete()
            crafter.action='craft'
            slevel= crafter.use_skill(self.req_skill_type)
            if self.item.typeclass=='material' and len(crafter.inventory.filter(name=self.item.name).filter(typeclass=self.item.typeclass))>0:
                already = crafter.inventory.filter(name=self.item.name)[0]
                already.DP+=m['result']
                already.save()
                crafter.blueprints.add(self)
                return (1,already)
            else:
                print 60
                if self.item.typeclass=='material':
                    print 68
                    new = self.item.copy()
                    new.DP=m['result']
                    new.save()
                    crafter.inventory.add(new)
                elif self.item.typeclass=='tool':
                    print 73
                    dp = self.item.a_maxdp*(101-slevel)/100
                    for e in xrange(0,int(m['result'])):
                        print 78
                        new = self.item.copy()
                        new.status='unfinished'
                        new.DP=dp
                        new.save()
                        crafter.inventory.add(new)
                print 88
                crafter.blueprints.add(self)
                return (1,new)
        else:
            return (-1,None)     
       
