"""
    SleekXMPP: The Sleek XMPP Library
    XEP-0363: HTTP File Upload
    Copyright (C) 2015 Matthias Rieber
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

from sleekxmpp.plugins.base import register_plugin

from sleekxmpp.plugins.xep_0363 import stanza
from sleekxmpp.plugins.xep_0363.stanza import RequestUploadSlot, Slot
from sleekxmpp.plugins.xep_0363.upload import XEP_0363


register_plugin(XEP_0363)
