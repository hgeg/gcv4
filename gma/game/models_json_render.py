  def render(self,place,mychar_id,mychar_state,flip=False):
        c = 180 #perspective constant
        h_=self.h*1.5*c/(place.depth*2.0-self.y) #display height
        w_=self.w*1.5*c/(place.depth*2.0-self.y) #display width
        y_= (self.y*1.2*c/place.depth)+place.horizon-(h_*12/11) #y position on screen
        x_= self.x-w_/2 #x position on screen
        w_large = (14*w_/(self.w+25))+w_ #increase width if a weapon is hold.
        n_pos = (x_+w_/2-len(self.name)*3,(y_-h_/10)-2) #current coordinates of GO's name
        ischar= self.type in ['char','npcChar']
        ismychar = self.id == mychar_id
        data=''
        #if the object is a character
        if ischar:    
          if self.character.type=='npcChar' and self.character.action=="travel":
            if self.character.time_left>datetime.datetime.now(): return ''
          else:
            params = {'h_':h_, 'w_':w_, 'y_':y_, 'x_':x_, 'w_large':w_large if self.character.weapon and self.character.weapon.message=='large' else w_, 'n_pos_x': n_pos[0],'n_pos_y': n_pos[1],
                'id':self.id,'mychar':mychar_id,'name':self.name,'action':self.character.action,
                'gender':self.character.gender,
                'hair':self.character.hair,
                'face':self.character.face,
                'beard':self.character.facial,
                'image':self.image,
                'shader':'onload="darken(this,lum,false);',
                'shirt':self.character.shirt.name if self.character.shirt else 'blank',
                'pants':self.character.pants.name if self.character.pants else 'blank',
                'armor':self.character.armor.name if self.character.armor else 'blank',
                'boots':self.character.boots.name if self.character.boots else 'blank',
                'gloves':self.character.gloves.name if self.character.gloves else 'blank',
                'greaves':self.character.greaves.name if self.character.greaves else 'blank',
                'pauldrons':self.character.pauldrons.name if self.character.pauldrons else 'blank',
                'weapon':('key' if self.character.weapon.category=='key' else self.character.weapon.name) if self.character.weapon else 'blank',
                'hat':self.character.hat.name if self.character.hat else 'blank',
                'flip': 'true' if flip else 'false', 
                'shoutbox':'<span style="position: absolute;padding: 3 3 3 3;border: 1px solid  #000000; text-align: center; -moz-border-radius:5px; border-radius:5px;color:#000000;background-color:#f0f0f0;font-family:Verdana;font-size:10px;top:%dpx;left:%dpx;white-space: nowrap;z-index:99;"> %s </span>'%(n_pos[1]-20,x_-4+w_/2-2*len(self.character.shoutbox.encode('utf-8')),self.character.shoutbox) if self.character.counter>datetime.datetime.now() else '',
                'options':'' if (mychar_state or self.character.state) else '''
<div id="options%(id)d" onmouseover="jQuery(this).css({visibility:'visible','z-index':999999});"  onmouseout="jQuery(this).css({visibility:'hidden','z-index':-1});" style="position:absolute;left:0px;top:0px;width:%(w_)dpx;height:%(h_)dpx;visibility:hidden;">
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
                          '''%{'id':self.id,'mychar':mychar_id,'h_':h_, 'w_':w_, 'y_':y_, 'x_':x_}}
            #if this character  belongs to the user:
            if ismychar:
                if mychar_state in [0,-1]:
                    data =  ''' 

    %(shoutbox)s                
    <span style="position:absolute;left:%(n_pos_x)d;top:%(n_pos_y)d;color:#ffffff;font-family:Verdana;font-size:12px;background-color:#24507b;white-space: nowrap;">
        %(name)s
    </span>
    <div ondrop="drop(event);" ondragenter="return false;" ondragover="event.preventDefault()" id="gObj%(id)d" style="position:absolute;left:%(x_)dpx;top:%(y_)dpx;border:none;"align="left"> 
        <a ondrop="drop(event);" ondragenter="return false;" ondragover="event.preventDefault()" href="/index/cpanel/" class="cBox">
            <img id="char%(id)d"  style="width:%(w_)dpx;height:%(h_)dpx;border:none;" 
            name="{'image':'%(image)s','gender':'%(gender)s','appereance':[%(hair)d,%(beard)d],'equipment':['%(weapon)s','%(hat)s','%(pauldrons)s','%(armor)s','%(gloves)s','%(shirt)s','%(greaves)s','%(pants)s','%(boots)s']}" ></img>
        </a>
    </div>  
                        
                            '''%params
                else:
                    data =  ''' 

        %(shoutbox)s                
    <span ondrop="drop(event);" ondragenter="return false;" ondragover="event.preventDefault()" style="position:absolute;left:%(n_pos_x)d;top:%(n_pos_y)d;color:#ffffff;font-family:Verdana;font-size:12px;background-color:#24507b;white-space: nowrap;">
        %(name)s
    </span>
    <div id="gObj%(id)d" style="position:absolute;left:%(x_)dpx;top:%(y_)dpx;border: 0px;"align="left"> 
        <img id="char%(id)d"  style="width:%(w_)dpx;height:%(h_)dpx;border: 0px;" 
             name="{'image':'%(image)s','gender':'%(gender)s','appereance':[%(hair)s,%(beard)s,%(face)s],'equipment':['%(weapon)s','%(hat)s','%(pauldrons)s','%(armor)s','%(gloves)s','%(shirt)s','%(greaves)s','%(pants)s','%(boots)s']}" ></img>
    </div>                    
                            '''%params
                
            else:
                if (mychar_state<0 and self.character.state<0) or (mychar_state>=0 and self.character.state>=0):  
                    data = '''
            %(shoutbox)s                
    <span style="position:absolute;left:%(n_pos_x)d;top:%(n_pos_y)d;color:#ffffff;font-family:Verdana;font-size:12px;background-color:#24507b;white-space: nowrap;">
        %(name)s
    </span>
    <div id="gObj%(id)d" onmouseover="jQuery('#options%(id)d').css({visibility:'visible','z-index':999999});" style="position:absolute;left:%(x_)dpx;top:%(y_)dpx;"align="left"> 
        <img id="char%(id)d"  style="width:%(w_)dpx;height:%(h_)dpx;" 
             name="{'image':'%(image)s','gender':'%(gender)s','appereance':[%(hair)s,%(beard)s,%(face)s],'equipment':['%(weapon)s','%(hat)s','%(pauldrons)s','%(armor)s','%(gloves)s','%(shirt)s','%(greaves)s','%(pants)s','%(boots)s']}" 
             border="0"></img>
        %(options)s
    </div>               
                            '''%params
                else: data=''
                        
        elif self.type=='item':
            if mychar_state == -1:
                data = '' 
            else:
                params = {'h_':h_, 'w_':w_, 'y_':y_-h_/4, 'x_':x_, 'name':self.name, 'name_d':self.item.get_name(),'id':self.id,'shader':'onload="darken(this,lum,false);' if self.message!='light' else '','image':self.item.typeclass, 'lum': 'lum' if place.category=="outer" else 0}
                if self.item.typeclass=='document':
                    if self.item.category=='TheBook': data =  ''' 
                    
        <a title="%(name)s" class="tooltip"  draggable="true" ondragstart="return drag(event,%(id)d);" href="/index/viewdocx/%(id)d/1/" class="dBox">         
            <img style="position:absolute;left:%(x_)d;top:%(y_)d" width="%(w_)d" height="%(h_)d" src="/index/files/item/%(image)s.gif" border="0" %(shader)s">
        </a>
                                                              '''%params
                    elif self.item.category=='scroll': data =  ''' 
        <div onclick="sendCursorPos();" style="position:absolute;left:%(x_)d;top:%(y_)d" width="%(w_)d" height="%(h_)d" draggable="true" ondragstart="return drag(event,%(id)d);">              
            <img title="%(name_d)s" src="/index/files/item/%(image)s.gif" border="0" %(shader)s">
        </div>
                                                              '''%params
                    else: data =  ''' 
                    
        <a draggable="true" ondragstart="return drag(event,%(id)d);" title="%(name_d)s" href="/index/viewdoc/%(id)s/1/" class="dBox">            
            <img style="position:absolute;left:%(x_)d;top:%(y_)d" width="%(w_)d" height="%(h_)d" src="/index/files/item/%(image)s.gif" border="0">
        </a>
                    
                                  '''%params
                              
                elif self.item.typeclass in ['tool','material']:
                    if self.item.category == 'key': data =  '''    

        <a title="%(name_d)s" class="tooltip" draggable="true"  ondragstart="return drag(event,%(id)d);" title="%(name_d)s" onclick="sendCursorPos();">            
            <img style="position:absolute;left:%(x_)d;top:%(y_)d" width="%(w_)d" height="%(h_)d" src="/index/files/item/keys.gif" border="0" %(shader)s">
        </a>        
                                                                         '''%params
                    elif self.item.typeclass == 'material': data =  '''    
        <a title="%(name_d)s" class="tooltip" draggable="true"  ondragstart="return drag(event,%(id)d);" title="%(name_d)s" onclick="sendCursorPos();">                  
            <img style="position:absolute;left:%(x_)d;top:%(y_)d;z-index:0" width="%(w_)d" height="%(h_)d" src="/index/files/item/%(name)s.gif" border="0" %(shader)s">
        </a>        
                                                                         '''%params
                    else: data =  '''    
        <a draggable="true" ondragstart="return drag(event,%(id)d);" title="%(name_d)s" onclick="sendCursorPos();">                  
            <img style="position:absolute;left:%(x_)d;top:%(y_)d" width="%(w_)d" height="%(h_)d" src="/index/files/item/item.gif" border="0" %(shader)s">
        </a>        
                                                                         '''%params
                              
                          
        elif self.type=='gate': 
            if mychar_state == -1:
                data = ''
            else:
                params = {'h_':h_, 'w_':w_, 'y_':y_, 'x_':x_,'name':self.name,'id':self.gate.id,'shader':'onload="darken(this,lum,false);' if self.message!='light' else '','image':self.image, 'lum': 'lum' if place.category=="outer" else 0, 'lock':'unlock' if self.gate.locked else 'lock'}
                data = ''' 
    <div onmouseover="jQuery($('g_options%(id)d')).css({visibility:'visible','z-index':999999});" onmouseout="jQuery($('g_options%(id)d')).css({visibility:'visible','z-index':-1});" >            
        <a title="%(name)s">            
            <img style="position:absolute;left:%(x_)d;top:%(y_)d" width="%(w_)d" height="%(h_)d" src="/index/files/item/%(image)s.gif" border="0" %(shader)s">
        </a>

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
                params = {'h_':h_, 'w_':w_, 'y_':y_, 'x_':x_,'name':self.name,'shader':'onload="darken(this,lum,false);' if self.message!='light' else '','id':self.id,'image':'bag', 'lum': 'lum'}
                data = ''' 
    <div id="gObj%(id)d" style="position:absolute;left:%(x_)d;top:%(y_)d" draggable="true" ondragstart="drag(event,%(id)d);" onclick="sendCursorPos();"> 
        <img style="position:absolute;left:0;top:0" width="%(w_)d" height="%(h_)d" src="/index/files/item/%(image)s.gif" %(shader)s">
    </div>
                       '''%params
        
        elif self.type=='container': 
            if mychar_state == -1:
                data = ''
            else:
                params = {'h_':h_, 'w_':w_, 'y_':y_, 'x_':x_,'name':self.name,'shader':'onload="darken(this,lum,false);' if self.message!='light' else '','id':self.id,'image':self.image}
                if not flip:
                    data = ''' 
    <div id="gObj%(id)d" draggable="false" ondragstart="event.preventDefault();" style="position:absolute;left:%(x_)d;top:%(y_)d">
        <a href="/index/open/%(id)d/" class="tBox">             
            <img width="%(w_)d" height="%(h_)d" src="/index/files/item/%(image)s.gif" border=0 %(shader)s">
        </a>
    </div>                 '''%params
                else: 
                    data = '''            
        <img style="position:absolute;left:%(x_)d;top:%(y_)d" width="%(w_)d" height="%(h_)d" src="/index/files/item/%(image)s.gif" border=0 %(shader)s">
                           '''%params
        
        elif self.type=='workbench': 
            if mychar_state == -1:
                data = ''
            else:
                params = {'h_':h_, 'w_':w_, 'y_':y_, 'x_':x_,'name':self.name,'shader':'onload="darken(this,lum,false);' if self.message!='light' else '','id':self.id,'image':self.image}
                if not flip:
                    data = ''' 
    <a href="/index/work/%(id)d/" class="tBox">             
        <img style="position:absolute;left:%(x_)d;top:%(y_)d" width="%(w_)d" height="%(h_)d" src="/index/files/item/%(image)s.gif" border=0 %(shader)s">
    </a>
                           '''%params
                else: 
                    data = '''            
        <img style="position:absolute;left:%(x_)d;top:%(y_)d" width="%(w_)d" height="%(h_)d" src="/index/files/item/%(image)s.gif" border=0 %(shader)s">
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
<div id="gObj%(id)d">             
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
<div id="gObj%(id)d">             
   %(char)s
   %(container)s
</div>
                         '''%params


        elif self.type=='iBox': 
            params = {'char1':self.interactionbox.first.render(place,mychar_id,mychar_state,),
                      'char2':self.interactionbox.second.render(place,mychar_id,mychar_state,True),
                      'link' : '<a href="/index/interact:return/" class="iBox">' if self.interactionbox.first.id == mychar_id or self.interactionbox.second.id == mychar_id else '',
                      'id':self.id, 'opn':'%',
                      'notification':'onload="notification(\'%s has been contacted with you!\')"'%self.interactionbox.first.name if mychar_id==self.interactionbox.second.id else ''}
            data = ''' 
%(link)s
%(char2)s
%(char1)s
<img src="/index/files/blank.gif" %(notification)s"></img>
</a>
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