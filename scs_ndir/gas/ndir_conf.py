"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies whether on not an NDIR is present

example JSON:
{"present": true}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

class NDIRConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "ndir_conf.json"

    @classmethod
    def filename(cls, host):
        return host.conf_dir() + cls.__FILENAME


    @classmethod
    def load_from_host(cls, host):
        return cls.load_from_file(cls.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __addr_str(cls, addr):
        if addr is None:
            return None

        return "0x%02x" % addr


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return NDIRConf(False)

        present = jdict.get('present')

        return NDIRConf(present)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, present):
        """
        Constructor
        """
        self.__present = bool(present)


    # ----------------------------------------------------------------------------------------------------------------

    def ndir(self, host):
        if not self.present:
            return None

        return NDIR(host.ndir_device())


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        PersistentJSONable.save(self, self.__class__.filename(host))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def present(self):
        return self.__present


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['present'] = self.present

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRConf:{present:%s}" %  self.present
