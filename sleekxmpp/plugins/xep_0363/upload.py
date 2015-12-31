"""
    SleekXMPP: The Sleek XMPP Library
    XEP-0363: HTTP File Upload
    Copyright (C) 2015 Matthias Rieber
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""


import os
import logging
import mimetypes
import requests

from sleekxmpp import Iq
from sleekxmpp.plugins import BasePlugin
from sleekxmpp.xmlstream import register_stanza_plugin
from sleekxmpp.jid import JID
from sleekxmpp.plugins.xep_0363 import stanza, RequestUploadSlot, Slot
from sleekxmpp.exceptions import XMPPError

from pprint import pprint

class XEP_0363(BasePlugin):

    name = 'xep_0363'
    description = 'XEP-0363: HTTP File Upload'
    dependencies = set(['xep_0030'])
    stanza = stanza
    jid = None
    http_upload = None

    def plugin_init(self):
        register_stanza_plugin(Iq, RequestUploadSlot)
        register_stanza_plugin(Iq, Slot)

    def session_bind(self, jid):
        self.xmpp['xep_0030'].add_feature('urn:xmpp:http:upload')
        self.jid = jid

    def plugin_end(self):
        self.xmpp['xep_0030'].del_feature(feature='urn:xmpp:http:upload')

    def get_upload_slot(self, filename = None):
        if not self.http_upload:
            server_jid = JID(self.jid).domain
            self.http_upload = self._query_http_upload(server_jid)
        file_size = os.path.getsize(filename)
        iq = self.xmpp.Iq()
        iq['type'] = 'get'
        iq['to'] = self.http_upload
        iq.enable('req_upload_slot')
        iq['req_upload_slot']['filename'] = os.path.basename(filename)
        iq['req_upload_slot']['size'] = str(file_size)
        mt = mimetypes.guess_type(filename)
        iq['req_upload_slot']['content-type'] = mt[1]
        res = iq.send(block=True, timeout=1000)
        res.enable('slot')
        return (res['slot']['put'], res['slot']['get'])

    def upload_file(self, filename = None):
        put_url, get_url = self.get_upload_slot(filename)

        f = open(filename, 'rb')
        r = requests.put(put_url, data = f)
        f.close()
        if r.status_code == 201:
            return get_url
        else:
            raise XMPPError()


    def _query_http_upload(self, server_jid):
        upload_jid = False
        items = self.xmpp['xep_0030'].get_items(server_jid, block=True, iterator=False)
        for item in items['disco_items']['items']:
            if self.xmpp['xep_0030'].supports(item[0],
                    feature="urn:xmpp:http:upload"):
                upload_jid = item[0]
                break

        if upload_jid:
            return upload_jid
        else:
            raise XMPPError()

