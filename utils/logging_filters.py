#
# Freesound is (c) MUSIC TECHNOLOGY GROUP, UNIVERSITAT POMPEU FABRA
#
# Freesound is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Freesound is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     See AUTHORS file.
#

import ipaddress
import logging
import json

from django.conf import settings


def get_client_ip(request):
    """
    This method returns the IP of the current request by retrieving it from the HTTP_X_FORWARDED_FOR header (which
    is added by nginx). If in DEBUG mode, a fake test IP will be returned.
    """
    if settings.DEBUG:
        return '1.2.3.4'

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
        try:
            ipaddress.ip_network(unicode(ip))
        except ValueError:
            # Not a valid ip address
            ip = '-'
    else:
        ip = '-'
    return ip


class GenericDataFilter(logging.Filter):
    """
    This filter expects a message of the form:
        XXX(YYY)
    Where XXX can be anything, YYY must be a serialized json object, and the message ends with )
    Assuming this format, the filter tries to separate the json part, unserialize it and add it as
    properties of the emessage so graylog can process them. If the parsing does not succeed, the 
    message is sent as is.
    """
    def filter(self, record):
        try:
            message = record.getMessage()
            json_part = message[message.find('(') + 1:-1]
            fields = json.loads(json_part)
            for key, value in fields.items():
                setattr(record, key, value)
        except (IndexError, ValueError, AttributeError):
            pass  # Message is not formatted for json parsing
        return True


class APILogsFilter(logging.Filter):

    def filter(self, record):
        message = record.getMessage().encode('utf8')
        try:
            (message, data, info) = message.split(' #!# ')
            if ':' in message:
                message = ' '.join([item.split(':')[0] for item in message.split(' ')])
            record.api_resource = message
            for key, value in json.loads(info).items():
                setattr(record, key, value)
            for key, value in json.loads(data).items():
                setattr(record, key, value)
        except:
            pass
        return True
