"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies whether on not an NDIR is present

example JSON:
{"model": "TxNDIR", "tally": 1}
"""

from scs_core.gas.ndir_conf import NDIRConf as AbstractNDIRConf

from scs_ndir.gas.tx_ndir.tx_ndir import TxNDIR


# --------------------------------------------------------------------------------------------------------------------

class NDIRConf(AbstractNDIRConf):
    """
    classdocs
    """

    @classmethod
    def filename(cls, host):
        return host.conf_dir() + cls._FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        model = jdict.get('model')
        tally = jdict.get('tally')

        return NDIRConf(model, tally)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, tally):
        """
        Constructor
        """
        super().__init__(model, tally)


    # ----------------------------------------------------------------------------------------------------------------
    # abstract NDIRConf implementation...

    def ndir(self, host):
        if self.model is None:
            raise ValueError('unknown model: %s' % self.model)

        return TxNDIR(host.ndir_usb_device())
