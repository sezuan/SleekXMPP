"""
    SleekXMPP: The Sleek XMPP Library
    XEP-0363: HTTP File Upload
    Copyright (C) 2015 Matthias Rieber
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

from sleekxmpp.xmlstream import ElementBase


class RequestUploadSlot(ElementBase):

    name = 'request'
    namespace = 'urn:xmpp:http:upload'
    plugin_attrib = 'req_upload_slot'
    interfaces = set(('filename', 'size', 'content-type'))
    sub_interfaces = interfaces
    is_extension = False


class Slot(ElementBase):

    name = 'slot'
    namespace = 'urn:xmpp:http:upload'
    plugin_attrib = 'slot'
    interfaces = set(('put', 'get'))
    sub_interfaces = interfaces
    is_extension = False
