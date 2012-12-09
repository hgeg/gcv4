#
# This is free software intended for integrating your custom python
# software with Envolve's website chat software. You may do with this 
# software as you wish.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or 
#implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modified from an original version written by Matt Wood 
#<http://github.com/mattwood>
#

"""Envolve API module to create signed commands and javascript tags to 
interact
with Envolve chat service.

"""

import base64
import hashlib
import time
import hmac

ENVOLVE_API_VERSION = '0.3'
ENVOLVE_JS_ROOT = 'd.envolve.com/env.nocache.js'


class EnvolveAPIException(Exception):
    """Inherits from Exception. Overrides __init__ and __str__."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class EnvolveAPIKey():
    """Handles encapsulation and validation of the Envolve API key."""

    def __init__(self, api_key):
        """EnvolveAPIKey constructor.

        Keyword arguments:
        api_key -- optional string argument that defaults to 
ENVOLVE_API_KEY.

        """
        try:
            api_key_pieces = api_key.strip().split('-')
            if (not len(api_key_pieces) == 2 or
                not len(api_key_pieces[0]) > 0 or
                not len(api_key_pieces[1]) > 0):
                raise EnvolveAPIException('Invalid or missing Envolve API Key.')
            api_key_pieces[0] = int(api_key_pieces[0])
        except (AttributeError, ValueError, TypeError):
            raise EnvolveAPIException('Invalid or missing Envolve API Key.')
        self.site_id = api_key_pieces[0]
        self.secret_key = api_key_pieces[1]
        self.full_key = '{0:d}-{1}'.format(self.site_id, 
self.secret_key)


def _base64_encode(string):
    """Returns a base64-encoded string based on the Envolve 
specifications.

    Keyword arguments:
    string -- plaintext string to encode to URL-safe base64

    """
    try:
        data = unicode(string, 'utf-8')
    except UnicodeDecodeError:
        raise EnvolveAPIException('Envolve API requires support for UTF-8')
    return base64.urlsafe_b64encode(data)


def _wrap_command(api_key, command):
    """Returns the hashed command string to perform calls to the API.

    Keyword arguments:
    api_key -- EnvolveAPIKey object
    command -- plaintext command string to be encoded and hashed

    """
    dt = str(long(time.time()*1000))
    command_string = dt + ';' + command
    return hmac.new(api_key.secret_key, command_string, 
hashlib.sha1).hexdigest() + ';' + command_string


def _get_html_for_command(api_key, command=None):
    """Returns the javascript tags for a given hashed command.

    Keyword arguments:
    api_key -- EnvolveAPIKey object
    command -- Hashed command string for which to return the javascript.

    """

    js = ['<!-- Envolve Chat -->',
          '<script type="text/javascript">',
          'var envoSn={0:d};'.format(api_key.site_id)]
    if command:
        js.append('env_commandString="{0}";'.format(command))
    js.append('var envProtoType = (("https:" == document.location.protocol) ? "https://" : "http://");')
    js.append('document.write(unescape("%3Cscript src=\'" + envProtoType + "{0}\' type=\'text/javascript\'%3E%3C/script%3E"));'.format(ENVOLVE_JS_ROOT))
    js.append('</script>')
    return '\n'.join([line for line in js if line])


def get_login_command(envolve_api_key, first_name,
                        last_name=None, pic=None, is_admin=False, 
profHTML=None):
    """Returns the hashed logout command string for use in the 
javascript call
    to the Envolve API.

    Keyword argument:
    envolve_api_key -- your site's Envolve API key as a string
    first_name -- string for the user's first name.
    last_name -- optional string for the user's last name.
                 Default value: None.
    pic -- optional string for the user's avatar.
           Default value: None.
    is_admin -- optional boolean for the user's admin status.
                Default value: False.
    profHTML -- optional HTML to be inserted into a user's profile 
rollover
                Default value: None.
    """
    api_key = EnvolveAPIKey(envolve_api_key)
    if not first_name:
        raise EnvolveAPIException("""You must provide at least a first 
name.
                                     If you are providing a username, 
use it
                                     for the first name.""")
    command = ['v={0}'.format(ENVOLVE_API_VERSION),
               'c=login',
               'fn={0}'.format(_base64_encode(first_name))]
    if last_name:
        command.append('ln={0}'.format(_base64_encode(last_name)))
    if pic:
        command.append('pic={0}'.format(_base64_encode(pic)))
    if is_admin:
        command.append('admin=t')
    if profHTML:
        command.append('prof={0}'.format(_base64_encode(profHTML)))
    return _wrap_command(api_key, ','.join(command))


def get_logout_command(envolve_api_key):
    """Returns the hashed logout command string for use in the 
javascript call
    to the Envolve API.

    Keyword argument:
    envolve_api_key -- your site's Envolve API key as a string

    """
    api_key = EnvolveAPIKey(envolve_api_key)
    return _wrap_command(api_key, "c=logout")


def get_html(envolve_api_key, first_name=None, last_name=None,
                pic=None, is_admin=False, profHTML=None):
    """Returns the javascript tags necessary to use the Envolve API 
login
    mechanism.

    Keyword arguments:
    envolve_api_key -- your site's Envolve API key as a string
    first_name -- optional string for the user's first name.
                  Default value: None.
    last_name -- optional string for the user's last name.
                 Default value: None.
    pic -- optional string of the absolute URL to the user's avatar.
           Default value: None.
    is_admin -- optional boolean for the user's admin status.
                Default value: False.
    profHTML -- optional HTML to be inserted into the user's profile 
rollover
                Default value: None.

    If first_name is not passed in, the user will be anonymous.

    To use, import this module and call the get_html function
    with the appropriate and correct keywords specified.  The function 
will
    return javascript that you can use in your page's HTML as you build 
your
    GET response.

    This python code:

        import envolve
        envolve.get_html('123-0123456789ABCDEF', first_name='user001')

    will produce javascript similar to:

        <!-- Envolve Chat -->
        <script type="text/javascript">
        var envoSn=123;
        env_commandString="{ command string }";
        var envProtoType = (("https:" == document.location.protocol) ? 
"https://" : "http://");
        document.write(unescape("%3Cscript src='" + envProtoType + 
"d.envolve.com/env.nocache.js' 
type='text/javascript'%3E%3C/script%3E"));
        </script>

    """
    api_key = EnvolveAPIKey(envolve_api_key)
    if first_name:
        return _get_html_for_command(api_key,
                                     get_login_command(api_key.full_key,
                                        first_name, last_name, pic,
                                        is_admin, profHTML))
    else:
        return _get_html_for_command(api_key, 
get_logout_command(api_key.full_key))
