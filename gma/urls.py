from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^gma/', include('gma.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/(.*)', 'admin.site.root'),
    
    (r'^cs484/$', 'gma.game.views.cs484'),
  
    (r'^project/$', 'gma.game.views.project_page') ,

    (r'^personal/$', 'gma.game.views.personal_page') ,
    
    (r'^rps/$', 'gma.game.views.rps_page') ,
   
    (r'^rule110/$', 'gma.game.views.rule110') ,
    
    (r'^chat/$', 'gma.chat.views.chat') ,
   
    (r'^rule110/(?P<iters>.*)/$', 'gma.game.views.rule110') ,

    #Uncomment the following three for development stage:

    #(r'^cs484/.*/$', 'gma.game.views.construction'),

    #(r'^.*/$', 'gma.game.views.construction') ,
    
    #(r'^$', 'gma.game.views.construction'),

    (r'^index/$', 'gma.game.views.render') ,

    (r'^$', 'gma.game.views.render') ,
    
    (r'^index/attack:(?P<action>.)/(?P<first>.*)/(?P<other>.*)/$', 'gma.game.views.attack') ,
    
    (r'^index/interact/tweak/(?P<amount>.*)/$', 'gma.game.views.tweak_balance') ,

    (r'^index/interact/(?P<first>.*)/(?P<other>.*)/$', 'gma.game.views.interact') ,
    
    (r'^index/interact:return/$', 'gma.game.views.interact_return') ,
    
    (r'^index/interact/otherbox/$', 'gma.game.views.other_box') ,
    
    (r'^index/status/signal/$', 'gma.game.views.exchange_signal') ,
    
    (r'^index/interact/exchange/$', 'gma.game.views.interact_action') ,  
    
    (r'^index/interact/exchange:npc/$', 'gma.game.views.npc_interact_action') ,
    
    (r'^index/interrupt/$', 'gma.game.views.interrupt') ,

    (r'^index/login/$', 'gma.game.views.alogin') ,

    (r'^index/notify/$', 'gma.game.views.notify') ,

    (r'^accounts/login/$', 'gma.game.views.alogin') ,

    (r'^index/log/$', 'gma.game.views.login') ,
    
    (r'^index/logout/$', 'gma.game.views.logout') ,

    (r'^index/register/$', 'gma.game.views.aregister') ,

    (r'^index/getlist/(?P<p_id>.*)/$', 'gma.game.views.getlist') ,
    
    (r'^index/getstatus/$', 'gma.game.views.getstatus') ,
    
    (r'^index/test/render/$', 'gma.game.views.render_json') ,
    
    (r'^index/test/getlist/$', 'gma.game.views.getlist_json') ,
    
    (r'^index/get_msg_list/$', 'gma.game.views.get_msg_list') ,
    
    (r'^index/send_msg/$', 'gma.game.views.send_msg') ,

    (r'^index/reg/$', 'gma.game.views.register') ,
    
    (r'^index/cpanel/(?P<tab>.*)/$', 'gma.game.views.panel') ,
    
    (r'^index/cpanel/$', 'gma.game.views.panel') ,

    (r'^index/char/$', 'gma.game.views.char_panel') ,
   
    (r'^index/char/relocate/$', 'gma.game.views.relocate') ,

    (r'^index/char/rest/$', 'gma.game.views.rest') ,
    
    (r'^index/chars/handle/$', 'gma.game.views.handle_chars') ,
    
    (r'^index/sendpos/(?P<x>.*)/(?P<y>.*)/$', 'gma.game.views.processPosInfo') ,
    
    (r'^index/npc/action/$', 'gma.game.views.npc_action') ,
    
    (r'^index/veichle/schedule/$', 'gma.game.views.veichle') ,
    
    (r'^index/shout/$', 'gma.game.views.shout') ,
    
    (r'^index/gate/lock:(?P<g_id>.*)/$', 'gma.game.views.lock') ,
    
    (r'^index/gate/enter:(?P<g_id>.*)/$', 'gma.game.views.enter') ,

    (r'^index/char/inv/$', 'gma.game.views.show_inventory') ,
    
    (r'^index/char/sbk/$', 'gma.game.views.show_spellbook') ,
    
    (r'^index/char/skills/$', 'gma.game.views.skill_panel') ,
    
    (r'^index/char/inv/async/$', 'gma.game.views.show_inventory_async') ,

    (r'^index/item_act/$', 'gma.game.views.item_action') ,
    
    (r'^index/viewdoc/(?P<d_id>.*)/(?P<whr>.*)/$', 'gma.game.views.view_document') ,
    
    (r'^index/writedoc/(?P<d_id>.*)/$', 'gma.game.views.write_document') ,
    
    (r'^index/savedoc/(?P<d_id>.*)/$', 'gma.game.views.save_document') ,
    
    (r'^index/viewdocx/(?P<d_id>.*)/(?P<whr>.*)/$', 'gma.game.views.view_the_book') ,
    
    (r'^index/thebook/$', 'gma.game.views.the_book') ,

    (r'^index/inv/put/$', 'gma.game.views.put_money') ,
    
    (r'^index/inv/return/$', 'gma.game.views.return_money') ,
    
	  (r'^index/inv/amount:take/(?P<i>.*)/$', 'gma.game.views.take_amount') ,
    
    (r'^index/inv/amount:choose/(?P<i>.*)/$', 'gma.game.views.choose_amount') ,

    (r'^index/travel/(?P<cell>.*)/$', 'gma.game.views.travel') ,
    
    (r'^index/arrive/$', 'gma.game.views.arrive') ,

    (r'^index/create/$', 'gma.game.views.create_char') ,

    (r'^index/save/$', 'gma.game.views.save_char') ,
    
    (r'^index/open/(?P<c_id>.*)/$', 'gma.game.views.open_chest') ,

    (r'^index/look/(?P<c_id>.*)/$', 'gma.game.views.look_chest') ,
    
    (r'^index/work/(?P<c_id>.*)/$', 'gma.game.views.open_workbench') ,
    
    (r'^index/bench/action/$', 'gma.game.views.bench_action') ,
    
    (r'^index/harvest/(?P<h_id>.*)/$', 'gma.game.views.harvest') ,
    
    (r'^index/collect/(?P<h_id>.*)/$', 'gma.game.views.collect') ,
    
    (r'^index/chest:return/$', 'gma.game.views.chest_return') ,
    
    (r'^index/chest/action/(?P<type>.*)/$', 'gma.game.views.chest_action') ,

    (r'^index/blueprint/create/$', 'gma.game.views.edit_blueprint') ,

    (r'^index/blueprint/save/$', 'gma.game.views.save_blueprint') ,

    (r'^index/cell/create/$', 'gma.game.views.edit_cell') ,

    (r'^index/cell/save/$', 'gma.game.views.save_cell') ,
    
    (r'^index/cell/check/(?P<p_name>.*)/(?P<time>.*)/$', 'gma.game.views.check_place') ,
    
    (r'^index/item/create/$', 'gma.game.views.edit_item') ,
    
    (r'^index/item/take/(?P<id>.*)/(?P<proc>.*)/$', 'gma.game.views.take_item') ,

    (r'^index/item/save/$', 'gma.game.views.save_item') ,
    
    (r'^index/init/$', 'gma.game.views.init_world') ,
    
    (r'^index/add/topic/$', 'gma.game.views.add_topic') ,
    
    (r'^index/docsc/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/can/gcv4/gma/public/documents/custom/'}),
    
    (r'^index/docs/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/can/gcv4/gma/public/documents/'}),
    
    (r'^index/files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/can/gcv4/gma/public/templates/files/'}),
    
    #(r'^index/docsc/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/gma/www/gma/public/documents/custom/'}),
    
    #(r'^index/docs/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/gma/www/gma/public/documents/'}),
    
    #(r'^index/files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/gma/www/gma/public/templates/files/'})
    
    #(r'^index/files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'public/templates/files/'}),

    #(r'^index/docs/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'public/documents/'}) 
    

)
