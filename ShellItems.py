import datetime
import logging

from BinaryParser import Block
from BinaryParser import align
from BinaryParser import OverrunBufferException
from known_guids import known_guids


g_logger = logging.getLogger("ShellItems")


class SHITEMTYPE:
    '''
    This is like an enum...
    These are the 'supported' SHITEM types
    '''
    UNKNOWN0 = 0x00
    UNKNOWN1 = 0x01
    UNKNOWN2 = 0x2E
    FILE_ENTRY0 = 0x31
    FILE_ENTRY1 = 0x32
    FILE_ENTRY2 = 0xB1
    FOLDER_ENTRY = 0x1F
    VOLUME_NAME = 0x2F
    NETWORK_VOLUME_NAME0 = 0x41
    NETWORK_VOLUME_NAME1 = 0x42
    NETWORK_VOLUME_NAME2 = 0x46
    NETWORK_VOLUME_NAME3 = 0x47
    NETWORK_SHARE = 0xC3
    URI = 0x61
    CONTROL_PANEL = 0x71
    UNKNOWN3 = 0x74


class SHITEM(Block):
    def __init__(self, buf, offset, parent):
        super(SHITEM, self).__init__(buf, offset, parent)

        self.declare_field("word", "size", 0x0)
        self.declare_field("byte", "type", 0x2)
        g_logger.debug("SHITEM @ %s of type %s.", hex(offset), hex(self.type()))

    def __unicode__(self):
        return u"SHITEM @ %s." % (hex(self.offset()))

    def name(self):
        return "??"

    def m_date(self):
        return datetime.datetime.min

    def a_date(self):
        return datetime.datetime.min

    def cr_date(self):
        return datetime.datetime.min


class SHITEM_FOLDERENTRY(SHITEM):
    def __init__(self, buf, offset, parent):
        g_logger.debug("SHITEM_FOLDERENTRY @ %s.", hex(offset))
        super(SHITEM_FOLDERENTRY, self).__init__(buf, offset, parent)

        self._off_folderid = 0x3      # UINT8
        self.declare_field("guid", "guid", 0x4)

    def __unicode__(self):
        return u"SHITEM_FOLDERENTRY @ %s: %s." % \
          (hex(self.offset()), self.name())

    def folder_id(self):
        _id = self.unpack_byte(self._off_folderid)

        if _id == 0x00:
            return "INTERNET_EXPLORER"
        elif _id == 0x42:
            return "LIBRARIES"
        elif _id == 0x44:
            return "USERS"
        elif _id == 0x48:
            return "MY_DOCUMENTS"
        elif _id == 0x50:
            return "MY_COMPUTER"
        elif _id == 0x58:
            return "NETWORK"
        elif _id == 0x60:
            return "RECYCLE_BIN"
        elif _id == 0x68:
            return "INTERNET_EXPLORER"
        elif _id == 0x70:
            return "UKNOWN"
        elif _id == 0x80:
            return "MY_GAMES"
        else:
            return ""

    def name(self):
        if self.guid() in known_guids:
            return known_guids[self.guid()]
        else:
            return "{%s: %s}" % (self.folder_id(), self.guid())


class SHITEM_UNKNOWNENTRY0(SHITEM):
    def __init__(self, buf, offset, parent):
        g_logger.debug("SHITEM_UNKNOWNENTRY0 @ %s.", hex(offset))
        super(SHITEM_UNKNOWNENTRY0, self).__init__(buf, offset, parent)

        self.declare_field("word", "size", 0x0)
        if self.size() == 0x20:
            self.declare_field("guid", "guid", 0xE)
        # pretty much completely unknown
        # TODO, if you have time for research

    def __unicode__(self):
        return u"SHITEM_UNKNOWNENTRY0 @ %s: %s." % \
          (hex(self.offset()), self.name())

    def name(self):
        if self.size() == 0x20:
            if self.guid() in known_guids:
                return known_guids[self.guid()]
            else:
                return "{%s}" % (self.guid())
        else:
            return "??"


class SHITEM_UNKNOWNENTRY2(SHITEM):
    def __init__(self, buf, offset, parent):
        g_logger.debug("SHITEM_UNKNOWNENTRY2 @ %s.", hex(offset))
        super(SHITEM_UNKNOWNENTRY2, self).__init__(buf, offset, parent)

        self.declare_field("byte", "flags", 0x3)
        self.declare_field("guid", "guid", 0x4)

    def __unicode__(self):
        return u"SHITEM_UNKNOWNENTRY2 @ %s: %s." % \
          (hex(self.offset()), self.name())

    def __str__(self):
        return "SHITEM_UNKNOWNENTRY2 @ %s: %s." % \
          (hex(self.offset()), self.name())

    def name(self):
        if self.guid() in known_guids:
            return known_guids[self.guid()]
        else:
            return "{%s}" % (self.guid())


class SHITEM_URIENTRY(SHITEM):
    def __init__(self, buf, offset, parent):
        g_logger.debug("SHITEM_URIENTRY @ %s.", hex(offset))
        super(SHITEM_URIENTRY, self).__init__(buf, offset, parent)

        self.declare_field("dword", "flags", 0x3)
        self.declare_field("wstring", "uri", 0x7)

    def __unicode__(self):
        return u"SHITEM_URIENTRY @ %s: %s." % \
          (hex(self.offset()), self.name())

    def name(self):
        return self.uri()


class SHITEM_CONTROLPANELENTRY(SHITEM):
    def __init__(self, buf, offset, parent):
        g_logger.debug("SHITEM_CONTROLPANELENTRY @ %s.", hex(offset))
        super(SHITEM_CONTROLPANELENTRY, self).__init__(buf, offset, parent)

        self.declare_field("byte", "flags", 0x3)
        self.declare_field("guid", "guid", 0xD)

    def __unicode__(self):
        return u"SHITEM_CONTROLPANELENTRY @ %s: %s." % \
          (hex(self.offset()), self.name())

    def name(self):
        if self.guid() in known_guids:
            return known_guids[self.guid()]
        else:
            return "{CONTROL PANEL %s}" % (self.guid())


class SHITEM_VOLUMEENTRY(SHITEM):
    def __init__(self, buf, offset, parent):
        g_logger.debug("SHITEM_VOLUMEENTRY @ %s.", hex(offset))
        super(SHITEM_VOLUMEENTRY, self).__init__(buf, offset, parent)

        self.declare_field("string", "name", 0x3)

    def __unicode__(self):
        return u"SHITEM_VOLUMEENTRY @ %s: %s." % \
          (hex(self.offset()), self.name())


class SHITEM_NETWORKVOLUMEENTRY(SHITEM):
    def __init__(self, buf, offset, parent):
        g_logger.debug("SHITEM_NETWORKVOLUMEENTRY @ %s.", hex(offset))
        super(SHITEM_NETWORKVOLUMEENTRY, self).__init__(buf, offset, parent)

        self.declare_field("byte", "flags", 0x4)
        self._off_name = 0x5

    def __unicode__(self):
        return u"SHITEM_NETWORKVOLUMEENTRY @ %s: %s." % \
          (hex(self.offset()), self.name())

    def name(self):
        if self.flags() & 0x2:
            return self.unpack_string(self._off_name)
        return ""

    def description(self):
        if self.flags() & 0x2:
            return self.unpack_string(self._off_name + len(self.name()) + 1)
        return ""


class SHITEM_NETWORKSHAREENTRY(SHITEM):
    def __init__(self, buf, offset, parent):
        g_logger.debug("SHITEM_NETWORKSHAREENTRY @ %s.", hex(offset))
        super(SHITEM_NETWORKSHAREENTRY, self).__init__(buf, offset, parent)

        self.declare_field("byte", "flags", 0x4)
        self.declare_field("string", "path", 0x5)
        self.declare_field("string", "description", 0x5 + len(self.path()) + 1)

    def __unicode__(self):
        return u"SHITEM_NETWORKSHAREENTRY @ %s: %s." % \
          (hex(self.offset()), self.name())

    def name(self):
        return self.path()


class Fileentry(SHITEM):
    """
    The Fileentry structure is used both in the BagMRU and Bags keys with
    minor differences (eg. sizeof and location of size field).
    """
    def __init__(self, buf, offset, parent, filesize_offset):
        g_logger.debug("Fileentry @ %s.", hex(offset))
        super(Fileentry, self).__init__(buf, offset, parent)

        off = filesize_offset
        self.declare_field("dword", "filesize", off); off += 4
        self.declare_field("dosdate", "m_date", off); off += 4
        self.declare_field("word", "fileattrs", off); off += 2
        self.declare_field("string", "short_name", off)

        off += len(self.short_name()) + 1
        off = align(off, 2)

        self.declare_field("word", "ext_size", off); off += 2
        self.declare_field("word", "ext_version", off); off += 2

        if self.ext_version() >= 0x03:
            off += 4 # unknown

            self.declare_field("dosdate", "cr_date", off); off += 4
            self.declare_field("dosdate", "a_date", off); off += 4

            off += 4 # unknown
        else:
            self.cr_date = lambda: datetime.datetime.min
            self.a_date = lambda: datetime.datetime.min

        if self.ext_version() >= 0x0007:
            off += 8 # fileref
            off += 8 # unknown

            self._off_long_name_size = off
            off += 2

            if self.ext_version() >= 0x0008:
                off += 4 # unknown

            self._off_long_name = off
            off += self.long_name_size()
        elif self.ext_version() >= 0x0003:
            self._off_long_name_size = False
            self._off_long_name = off
            g_logger.debug("(WSTRING) long_name @ %s", hex(self.absolute_offset(off)))
        else:
            self._off_long_name_size = False
            self._off_long_name = False

    def __unicode__(self):
        return u"Fileentry @ %s: %s." % (hex(self.offset()), self.name())

    def long_name_size(self):
        if self._off_long_name_size:
            return self.unpack_word(self._off_long_name_size)
        elif self._off_long_name:
            return len(self.long_name()) + 2
        else:
            return 0

    def long_name(self):
        if self._off_long_name and self._off_long_name_size:
            if self.long_name_size() == 0:
                return ""
            else:
                return self.unpack_wstring(self._off_long_name, self.long_name_size())
        elif self._off_long_name:
            return self.unpack_wstring(self._off_long_name)
        else:
            return ""

    def name(self):
        n = self.long_name()
        if len(n) > 0:
            return n
        else:
            return self.short_name()


class SHITEM_FILEENTRY(Fileentry):
    def __init__(self, buf, offset, parent):
        g_logger.debug("SHITEM_FILEENTRY @ %s.", hex(offset))
        super(SHITEM_FILEENTRY, self).__init__(buf, offset, parent, 0x4)

        self.declare_field("byte", "flags", 0x3)

    def __unicode__(self):
        return u"SHITEM_FILEENTRY @ %s: %s." % (hex(self.offset()),
                                                self.name())


class ITEMPOS_FILEENTRY(SHITEM):
    def __init__(self, buf, offset, parent):
        g_logger.debug("ITEMPOS_FILEENTRY @ %s.", hex(offset))
        super(ITEMPOS_FILEENTRY, self).__init__(buf, offset, parent)

        self.declare_field("word", "size", 0x0)  # override
        self.declare_field("word", "flags", 0x2)

        if self.flags() & 0xFF == 0xC3:
            # network share type, printers, etc
            self.declare_field("string", "long_name", 0x5)
            return

        off = 4
        self.declare_field("dword", "filesize", off); off += 4
        self.declare_field("dosdate", "m_date", off); off += 4
        self.declare_field("word", "fileattrs", off); off += 2
        self.declare_field("string", "short_name", off)

        off += len(self.short_name()) + 1
        off = align(off, 2)

        self.declare_field("word", "ext_size", off); off += 2
        self.declare_field("word", "ext_version", off); off += 2

        if self.ext_version() >= 0x03:
            off += 4  # unknown

            self.declare_field("dosdate", "cr_date", off); off += 4
            self.declare_field("dosdate", "a_date", off); off += 4

            off += 4  # unknown
        else:
            self.cr_date = lambda: datetime.datetime.min
            self.a_date = lambda: datetime.datetime.min

        if self.ext_version() >= 0x0007:
            off += 8  # fileref
            off += 8  # unknown

            self._off_long_name_size = off
            off += 2

            if self.ext_version() >= 0x0008:
                off += 4  # unknown

            self._off_long_name = off
            off += self.long_name_size()
        elif self.ext_version() >= 0x0003:
            self._off_long_name_size = False
            self._off_long_name = off
            g_logger.debug("(WSTRING) long_name @ %s", hex(self.absolute_offset(off)))
        else:
            self._off_long_name_size = False
            self._off_long_name = False

    def long_name_size(self):
        if self._off_long_name_size:
            return self._off_long_name_size
        elif self._off_long_name:
            return len(self.long_name()) + 2
        else:
            return 0

    def long_name(self):
        if self._off_long_name and self._off_long_name_size:
            return self.unpack_wstring(self._off_long_name, self.long_name_size())
        elif self._off_long_name:
            return self.unpack_wstring(self._off_long_name)
        else:
            return ""

    def name(self):
        n = self.long_name()
        if len(n) > 0:
            return n
        else:
            return self.short_name()

    def __unicode__(self):
        return u"ITEMPOS_FILEENTRY @ %s: %s." % (hex(self.offset()), self.name())


class FILEENTRY_FRAGMENT(SHITEM):
    def __init__(self, buf, offset, parent, filesize_offset):
        g_logger.debug("FILEENTRY_FRAGMENT @ %s.", hex(offset))
        super(FILEENTRY_FRAGMENT, self).__init__(buf, offset, parent)

        off = filesize_offset
        self.declare_field("dword", "filesize", off); off += 4
        self.declare_field("dosdate", "m_date", off); off += 4
        self.declare_field("word", "fileattrs", off); off += 2
        self.declare_field("string", "short_name", off)

        off += len(self.short_name()) + 1
        off = align(off, 2)

    def name(self):
        return self.short_name()

    def __unicode__(self):
        return u"ITEMPOS_FILEENTRY @ %s: %s." % (hex(self.offset()), self.name())


class SHITEM_UNKNOWNENTRY3(Fileentry):
    def __init__(self, buf, offset, parent):
        g_logger.debug("SHITEM_UNKNOWNENTRY3 @ %s.", hex(offset))
        super(SHITEM_UNKNOWNENTRY3, self).__init__(buf, offset, parent, 0x4)

        self.declare_field("word", "size", 0x0)
        # most of this is unknown
        offs = 0x18
        self.declare_field("string", "short_name", offs)
        offs += len(self.short_name()) + 1
        offs = align(offs, 2)
        offs += 0x4C
        self.declare_field("wstring", "long_name", offs)

    def __unicode__(self):
        return u"SHITEM_UNKNOWNENTRY3 @ %s: %s." % (hex(self.offset()), self.name())

    def name(self):
        return self.long_name()


class SHITEMLIST(Block):
    def __init__(self, buf, offset, parent):
        g_logger.debug("SHITEMLIST @ %s.", hex(offset))
        super(SHITEMLIST, self).__init__(buf, offset, parent)

    def items(self):
        off = self.offset()

        while True:
            size = self.unpack_word(off)
            if size == 0:
                return

            # UNKNOWN1

            _type = self.unpack_byte(off + 2)
            if _type == SHITEMTYPE.FILE_ENTRY0 or \
               _type == SHITEMTYPE.FILE_ENTRY1 or \
               _type == SHITEMTYPE.FILE_ENTRY2:
                try:
                    item = SHITEM_FILEENTRY(self._buf, off, self)
                except OverrunBufferException:
                    item = FILEENTRY_FRAGMENT(self._buf, off, self, 0x4)

            elif _type == SHITEMTYPE.FOLDER_ENTRY:
                item = SHITEM_FOLDERENTRY(self._buf, off, self)

            elif _type == SHITEMTYPE.VOLUME_NAME:
                item = SHITEM_VOLUMEENTRY(self._buf, off, self)

            elif _type == SHITEMTYPE.NETWORK_VOLUME_NAME0 or \
                 _type == SHITEMTYPE.NETWORK_VOLUME_NAME1 or \
                 _type == SHITEMTYPE.NETWORK_VOLUME_NAME2 or \
                 _type == SHITEMTYPE.NETWORK_VOLUME_NAME3:
                item = SHITEM_NETWORKVOLUMEENTRY(self._buf, off, self)

            elif _type == SHITEMTYPE.NETWORK_SHARE:
                item = SHITEM_NETWORKSHAREENTRY(self._buf, off, self)

            elif _type == SHITEMTYPE.URI:
                item = SHITEM_URIENTRY(self._buf, off, self)

            elif _type == SHITEMTYPE.CONTROL_PANEL:
                if len(self._buf) - off != 0x20:
                    g_logger.warning("CONTROLPANELENTRY with size != 0x20: %s",
                            len(self._buf) - off)
                    return
                item = SHITEM_CONTROLPANELENTRY(self._buf, off, self)

            elif _type == SHITEMTYPE.UNKNOWN0:
                item = SHITEM_UNKNOWNENTRY0(self._buf, off, self)

            elif _type == SHITEMTYPE.UNKNOWN2:
                item = SHITEM_UNKNOWNENTRY2(self._buf, off, self)

            elif _type == SHITEMTYPE.UNKNOWN3:
                item = SHITEM_UNKNOWNENTRY3(self._buf, off, self)

            else:
                g_logger.debug("Unknown type: %s", hex(_type))
                item = SHITEM(self._buf, off, self)

            yield item
            off += item.size()

    def __unicode__(self):
        return u"SHITEMLIST @ %s." % (hex(self.offset()))
