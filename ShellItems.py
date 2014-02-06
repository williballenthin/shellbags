import datetime

from BinaryParser import Block
from BinaryParser import debug
from BinaryParser import align
from BinaryParser import OverrunBufferException


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
        debug("SHITEM @ %s of type %s." % (hex(offset), hex(self.type())))

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

known_guids = {
    "031e4825-7b94-4dc3-b131-e946b44c8dd5": "Libraries",
    "1ac14e77-02e7-4e5d-b744-2eb1ae5198b7": "CSIDL_SYSTEM",
    "208d2c60-3aea-1069-a2d7-08002b30309d": "My Network Places",
    "20d04fe0-3aea-1069-a2d8-08002b30309d": "My Computer",
    "21ec2020-3aea-1069-a2dd-08002b30309d": "{Unknown CSIDL}",
    "22877a6d-37a1-461a-91b0-dbda5aaebc99": "{Unknown CSIDL}",
    "2400183a-6185-49fb-a2d8-4a392a602ba3": "Public Videos",
    "2559a1f1-21d7-11d4-bdaf-00c04f60b9f0": "{Unknown CSIDL}",
    "2559a1f3-21d7-11d4-bdaf-00c04f60b9f0": "{Unknown CSIDL}",
    "26ee0668-a00a-44d7-9371-beb064c98683": "{Unknown CSIDL}",
    "3080f90e-d7ad-11d9-bd98-0000947b0257": "{Unknown CSIDL}",
    "3214fab5-9757-4298-bb61-92a9deaa44ff": "Public Music",
    "33e28130-4e1e-4676-835a-98395c3bc3bb": "Pictures",
    "374de290-123f-4565-9164-39c4925e467b": "Downloads",
    "4336a54d-038b-4685-ab02-99bb52d3fb8b": "{Unknown CSIDL}",
    "450d8fba-ad25-11d0-98a8-0800361b1103": "My Documents",
    "4bd8d571-6d19-48d3-be97-422220080e43": "Music",
    "5399e694-6ce5-4d6c-8fce-1d8870fdcba0": "Control Panel",
    "59031a47-3f72-44a7-89c5-5595fe6b30ee": "Users",
    "645ff040-5081-101b-9f08-00aa002f954e": "Recycle Bin",
    "724ef170-a42d-4fef-9f26-b60e846fba4f": "Administrative Tools",
    "7b0db17d-9cd2-4a93-9733-46cc89022e7c": "Documents Library",
    "7c5a40ef-a0fb-4bfc-874a-c0f2e0b9fa8e": "Program Files (x86)",
    "871c5380-42a0-1069-a2ea-08002b30309d": "Internet Explorer (Homepage)",
    "905e63b6-c1bf-494e-b29c-65b732d3d21a": "Program Files",
    "9e52ab10-f80d-49df-acb8-4330f5687855": "Temporary Burn Folder",
    "a305ce99-f527-492b-8b1a-7e76fa98d6e4": "Installed Updates",
    "b4bfcc3a-db2c-424c-b029-7fe99a87c641": "Desktop",
    "b6ebfb86-6907-413c-9af7-4fc2abf07cc5": "Public Pictures",
    "c1bae2d0-10df-4334-bedd-7aa20b227a9d": "Common OEM Links",
    "cce6191f-13b2-44fa-8d14-324728beef2c": "{Unknown CSIDL}",
    "d0384e7d-bac3-4797-8f14-cba229b392b5": "Common Administrative Tools",
    "d65231b0-b2f1-4857-a4ce-a8e7c6ea7d27": "System32 (x86)",
    "de61d971-5ebc-4f02-a3a9-6c82895e5c04": "Get Programs",
    "df7266ac-9274-4867-8d55-3bd661de872d": "Programs and Features",
    "dfdf76a2-c82a-4d63-906a-5644ac457385": "Public",
    "de974d24-d9c6-4d3e-bf91-f4455120b917": "Common Files",
    "ed228fdf-9ea8-4870-83b1-96b02cfe0d52": "My Games",
    "f02c1a0d-be21-4350-88b0-7367fc96ef3c": "Network",
    "f38bf404-1d43-42f2-9305-67de0b28fc23": "Windows",
    "f3ce0f7c-4901-4acc-8648-d5d44b04ef8f": "Users Files",
    "fdd39ad0-238f-46af-adb4-6c85480369c7": "Documents",
    # Control Panel Items
    "d20ea4e1-3957-11d2-a40b-0c5020524153": "Administrative Tools",
    "9c60de1e-e5fc-40f4-a487-460851a8d915": "AutoPlay",
    "d9ef8727-cac2-4e60-809e-86f80a666c91": "BitLocker Drive Encryption",
    "b2c761c6-29bc-4f19-9251-e6195265baf1": "Color Management",
    "e2e7934b-dce5-43c4-9576-7fe4f75e7480": "Date and Time",
    "17cd9488-1228-4b2f-88ce-4298e93e0966": "Default Programs",
    "74246bfc-4c96-11d0-abef-0020af6b0b7a": "Device Manager",
    "d555645e-d4f8-4c29-a827-d93c859c4f2a": "Ease of Access Center",
    "6dfd7c5c-2451-11d3-a299-00c04f8ef6af": "Folder Options",
    "93412589-74d4-4e4e-ad0e-e0cb621440fd": "Fonts",
    "259ef4b1-e6c9-4176-b574-481532c9bce8": "Game Controllers",
    "15eae92e-f17a-4431-9f28-805e482dafd4": "Get Programs",
    "87d66a43-7b11-4a28-9811-c86ee395acf7": "Indexing Options",
    "a3dd4f92-658a-410f-84fd-6fbbbef2fffe": "Internet Options",
    "a304259d-52b8-4526-8b1a-a1d6cecc8243": "iSCSI Initiator",
    "725be8f7-668e-4c7b-8f90-46bdb0936430": "Keyboard",
    "6c8eec18-8d75-41b2-a177-8831d59d2d50": "Mouse",
    "8e908fc9-becc-40f6-915b-f4ca0e70d03d": "Network and Sharing Center",
    "d24f75aa-4f2b-4d07-a3c4-469b3d9030c4": "Offline Files",
    "96ae8d84-a250-4520-95a5-a47a7e3c548b": "Parental Controls",
    "5224f545-a443-4859-ba23-7b5a95bdc8ef": "People Near Me",
    "78f3955e-3b90-4184-bd14-5397c15f1efc": "Performance Information and Tools",
    "ed834ed6-4b5a-4bfe-8f11-a626dcb6a921": "Personalization",
    "025a5937-a6be-4686-a844-36fe4bec8b6d": "Power Options",
    "7b81be6a-ce2b-4676-a29e-eb907a5126c5": "Programs and Features",
    "00f2886f-cd64-4fc9-8ec5-30ef6cdbe8c3": "Scanners and Cameras",
    "9c73f5e5-7ae7-4e32-a8e8-8d23b85255bf": "Sync Center",
    "bb06c0e4-d293-4f75-8a90-cb05b6477eee": "System ",
    "80f3f1d5-feca-45f3-bc32-752c152e456e": "Tablet PC Settings",
    "0df44eaa-ff21-4412-828e-260a8728e7f1": "Taskbar and Start Menu",
    "d17d1d6d-cc3f-4815-8fe3-607e7d5d10b3": "Text to Speech",
    "60632754-c523-4b62-b45c-4172da012619": "User Accounts",
    "be122a0e-4503-11da-8bde-f66bad1e3f3a": "Windows Anytime Upgrade",
    "78cb147a-98ea-4aa6-b0df-c8681f69341c": "Windows CardSpace",
    "d8559eb9-20c0-410e-beda-7ed416aecc2a": "Windows Defender",
    "4026492f-2f69-46b8-b9bf-5654fc07e423": "Windows Firewall",
    "5ea4f148-308c-46d7-98a9-49041b1dd468": "Windows Mobility Center",
    "e95a4861-d57a-4be1-ad0f-35267e261739": "Windows SideShow",
    "36eef7db-88ad-4e81-ad49-0e313f0c35f8": "Windows Update",
    # Vista Control Panel Items
    "7a979262-40ce-46ff-aeee-7884ac3b6136": "Add Hardware",
    "f2ddfc82-8f12-4cdd-b7dc-d4fe1425aa4d": "Sound",
    "b98a2bea-7d42-4558-8bd1-832f41bac6fd": "Backup and Restore Center",
    "3e7efb4c-faf1-453d-89eb-56026875ef90": "Windows Marketplace",
    "a0275511-0e86-4eca-97c2-ecd8f1221d08": "Infrared",
    "f82df8f7-8b9f-442e-a48c-818ea735ff9b": "Pen and Input Devices",
    "40419485-c444-4567-851a-2dd7bfa1684d": "Phone and Modem",
    "2227a280-3aea-1069-a2de-08002b30309d": "Printers",
    "fcfeecae-ee1b-4849-ae50-685dcf7717ec": "Problem Reports and Solutions",
    "62d8ed13-c9d0-4ce8-a914-47dd628fb1b0": "Regional and Language Options",
    "087da31b-0dd3-4537-8e23-64a18591f88b": "Windows Security Center",
    "58e3c745-d971-4081-9034-86e34b30836a": "Speech Recognition Options",
    # Windows 7 Control Panel Items
    "bb64f8a7-bee7-4e1a-ab8d-7d8273f7fdb6": "Action Center",
    "0142e4d0-fb7a-11dc-ba4a-000ffe7ab428": "Biometric Devices",
    "1206f5f1-0569-412c-8fec-3204630dfb70": "Credential Manager",
    "00c6d95f-329c-409a-81d7-c46c66ea7f33": "Default Location",
    "37efd44d-ef8d-41b1-940d-96973a50e9e0": "Desktop Gadgets",
    "a8a91a66-3a7d-4424-8d24-04e180695c7a": "Devices and Printers",
    "c555438b-3c23-4769-a71f-b6d3d9b6053a": "Display",
    "cb1b7f8c-c50a-4176-b604-9e24dee8d4d1": "Getting Started",
    "67ca7650-96e6-4fdd-bb43-a8e774f73a57": "HomeGroup",
    "e9950154-c418-419e-a90a-20c5287ae24b": "Location and Other Sensors",
    "05d7b0f4-2121-4eff-bf6b-ed3f69b894d9": "Notification Area Icons",
    "9fe63afd-59cf-4419-9775-abcc3849f861": "Recovery",
    "241d7c96-f8bf-4f85-b01f-e2b043341a4b": "RemoteApp and Desktop Connections",
    "c58c4893-3be0-4b45-abb5-a63e4b8c8651": "Troubleshooting",
    # Folder Types
    "0b2baaeb-0042-4dca-aa4d-3ee8648d03e5": "Pictures Library",
    "36011842-dccc-40fe-aa3d-6177ea401788": "Documents Search Results",
    "3f2a72a7-99fa-4ddb-a5a8-c604edf61d6b": "Music Library",
    "4dcafe13-e6a7-4c28-be02-ca8c2126280d": "Pictures Search Results",
    "5c4f28b5-f869-4e84-8e60-f11db97c5cc7": "Generic (All folder items)",
    "5f4eab9a-6833-4f61-899d-31cf46979d49": "Generic Library",
    "5fa96407-7e77-483c-ac93-691d05850de8": "Videos",
    "631958a6-ad0f-4035-a745-28ac066dc6ed": "Videos Library",
    "71689ac1-cc88-45d0-8a22-2943c3e7dfb3": "Music Search Results",
    "7d49d726-3c21-4f05-99aa-fdc2c9474656": "Documents",
    "7fde1a1e-8b31-49a5-93b8-6be14cfa4943": "Generic Search Results",
    "80213e82-bcfd-4c4f-8817-bb27601267a9": "Compressed Folder (zip folder)",
    "94d6ddcc-4a68-4175-a374-bd584a510b78": "Music",
    "b3690e58-e961-423b-b687-386ebfd83239": "Pictures",
    "ea25fbd7-3bf7-409e-b97f-3352240903f4": "Videos Search Results",
    "fbb3477e-c9e4-4b3b-a2ba-d3f5d3cd46f9": "Documents Library",
}


class SHITEM_FOLDERENTRY(SHITEM):
    def __init__(self, buf, offset, parent):
        debug("SHITEM_FOLDERENTRY @ %s." % (hex(offset)))
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
        debug("SHITEM_UNKNOWNENTRY0 @ %s." % (hex(offset)))
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
        debug("SHITEM_UNKNOWNENTRY2 @ %s." % (hex(offset)))
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
        debug("SHITEM_URIENTRY @ %s." % (hex(offset)))
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
        debug("SHITEM_CONTROLPANELENTRY @ %s." % (hex(offset)))
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
        debug("SHITEM_VOLUMEENTRY @ %s." % (hex(offset)))
        super(SHITEM_VOLUMEENTRY, self).__init__(buf, offset, parent)

        self.declare_field("string", "name", 0x3)

    def __unicode__(self):
        return u"SHITEM_VOLUMEENTRY @ %s: %s." % \
          (hex(self.offset()), self.name())


class SHITEM_NETWORKVOLUMEENTRY(SHITEM):
    def __init__(self, buf, offset, parent):
        debug("SHITEM_NETWORKVOLUMEENTRY @ %s." % (hex(offset)))
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
        debug("SHITEM_NETWORKSHAREENTRY @ %s." % (hex(offset)))
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
        debug("Fileentry @ %s." % (hex(offset)))
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
            debug("(WSTRING) long_name @ %s" % (hex(self.absolute_offset(off))))
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
        debug("SHITEM_FILEENTRY @ %s." % (hex(offset)))
        super(SHITEM_FILEENTRY, self).__init__(buf, offset, parent, 0x4)

        self.declare_field("byte", "flags", 0x3)

    def __unicode__(self):
        return u"SHITEM_FILEENTRY @ %s: %s." % (hex(self.offset()),
                                                self.name())


class ITEMPOS_FILEENTRY(SHITEM):
    def __init__(self, buf, offset, parent):
        debug("ITEMPOS_FILEENTRY @ %s." % (hex(offset)))
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
            debug("(WSTRING) long_name @ %s" % (hex(self.absolute_offset(off))))
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
        debug("FILEENTRY_FRAGMENT @ %s." % (hex(offset)))
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
        debug("SHITEM_UNKNOWNENTRY3 @ %s." % (hex(offset)))
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
        debug("SHITEMLIST @ %s." % (hex(offset)))
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
                item = SHITEM_CONTROLPANELENTRY(self._buf, off, self)

            elif _type == SHITEMTYPE.UNKNOWN0:
                item = SHITEM_UNKNOWNENTRY0(self._buf, off, self)

            elif _type == SHITEMTYPE.UNKNOWN2:
                item = SHITEM_UNKNOWNENTRY2(self._buf, off, self)

            elif _type == SHITEMTYPE.UNKNOWN3:
                item = SHITEM_UNKNOWNENTRY3(self._buf, off, self)

            else:
                debug("Unknown type: %s" % hex(_type))
                item = SHITEM(self._buf, off, self)

            yield item
            off += item.size()

    def __unicode__(self):
        return u"SHITEMLIST @ %s." % (hex(self.offset()))
