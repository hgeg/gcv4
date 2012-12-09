var minWidth = 45;
var maxWidth = 340;
var item_id = -1;
var action="idle";
var shout;
var myshout;

// Created by Dynamic HTML Editor V.5.5
// Road Sign
function jsGetLayer(n){var o;if(isDom2)return document.getElementById(n);if(isNS)return document.layers[n];if(isIE)return document.all(n);if(o=eval('document.'+n))return o;return null;}
function jsLink(sl,st){if(!st)st="_self";window.open (sl,st);}
function jsComboLink(o){var v,i,sl,st;if(o){i=o.selectedIndex;if(i>0){v=o[i].value;if(v.length){v=v.split('[*]');jsLink(v[0],v[1]);}}}}
//basic ajax method
function ajaxReq(u){$.ajax({url:u,method: 'get'});}
//Colorbox
$(document).ready(function(){
        $(".cBox").colorbox({width:"350", height:"320", iframe:true});
        $(".tBox").colorbox({width:"620", height:"300", iframe:true});
        $(".iBox").colorbox({width:"750", height:"510", iframe:true});
        $(".dBox").colorbox({width:"600", height:"490", iframe:true});
        $(".hBox").colorbox({width:"300", height:"200", iframe:true});
        $('#box').css('width',minWidth);
        $('#box_link').toggle(function(){                          
            $('#box').animate({'width':'390px'}, 400, 'swing');
        },function(){               
            $('#box').animate({'width':'45px'}, 400, 'swing');
        });
    });
function pageLoad(){
        $(".cBox").colorbox({width:"350", height:"320", iframe:true});
        $(".tBox").colorbox({width:"620", height:"300", iframe:true});
        $(".iBox").colorbox({width:"750", height:"510", iframe:true});
        $(".dBox").colorbox({width:"600", height:"490", iframe:true});
        $(".hBox").colorbox({width:"300", height:"200", iframe:true});
        tooltip();
    };
    
function takeItem(id){ajaxReq("/index/item/take/"+id+"/ground");};
function lock(id){ajaxReq("/index/gate/lock:"+id+"/");};
function wander(){$.ajax({url:"/index/char/relocate/",method:'get',success:function()
{
    document.body.style.cursor = 'url("http://gcv4.s3.amazonaws.com/files/misc/move.gif")';
    action='move';
}});};
function darken(obj,amount,flip){
    if(flip) $(obj).pixastic('brightness',{brightness:amount,contrast:0}).pixastic('fliph');
    else $(obj).pixastic('brightness',{brightness:amount,contrast:0});
};

function send_form(){
    $.post('/index/shout/',"shouted="+$('#shouttext').attr('value'));
    clearTimeout(shout);
}

function drag(e,id){
    e.dataTransfer.effectAllowed = 'move';
    elem = id;
    e.dataTransfer.setData("Text",id);
    e.dataTransfer.setDragImage(e.target, 20, 10);
    return true;
}

function drop(e){
    e.stopPropagation();
    item_id = e.dataTransfer.getData("Text");
    takeItem(item_id);
    e.preventDefault();
}

function render(JSONData){
    eval(JSONData)
    rdata = objs.fields[8] + '  <span style="position:absolute;left:%(n_pos_x)d;top:%(n_pos_y)d;color:#ffffff;font-family:Verdana;font-size:12px;background-color:#24507b;white-space: nowrap;""> '+ objs.fields[2] +'</span> <a ondrop="drop(event);" ondragenter="return false;" ondragover="return false;" href="/index/cpanel/" class="cBox"> <img style="position:absolute;left:'+obj.fields[4]+'px;top:'+obj.fields[5]+'px" width="'+obj.fields[6]+'" height="'+obj.fields[7]+'" src="/index/files/'+obj.fields[3]+'/char.gif/" border="0"> </a>'
    document.getElementById('peole').innerHTML = rdata;
    return 0;
}

