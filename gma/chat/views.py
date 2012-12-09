# Create your views here.
#from envolve import get_html, get_login_command
#from envolve.envolve import EnvolveAPIException 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required(redirect_field_name='')
def chat(request):
    madafaka = """
<!-- Envolve Chat -->
<script type="text/javascript">
var envoSn=67378;
var envProtoType = (("https:" == document.location.protocol) ? "https://" : "http://");
document.write(unescape("%3Cscript src='" + envProtoType + "d.envolve.com/env.nocache.js' type='text/javascript'%3E%3C/script%3E"));
</script>
    """
    #temp_html_code = get_html('67378-QZJ3hhDOgUnqJscF6S68h2052aEDv4Re' , first_name='Musa', last_name='Yirmibir', pic='http://gcv4.s3.amazonaws.com/files/misc/asd.jpg', is_admin=False, 'Deneme')
    HttpResponse(madafaka)
