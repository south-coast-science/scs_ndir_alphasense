# scs_ndir_alphasense
Environmental sampling abstractions for the Alphasense IRC-A1 NDIR CO2 sensor Transmitter board.

_South Coast Science is currently developing an SPI interface board for the Alphasense IRC-AT thermopile 
NDIR sensor. The SPI board will in most cases replace the Alphasense IRC-A1 NDIR USB Transmitter board. The IRC-A1 
NDIR USB Transmitter board code is no longer supported, but is provided to users who need to develop 
their own USB solution._

_See **[scs_ndir](https://github.com/south-coast-science/scs_ndir)** for more information._


**Required libraries:** 

* Third party: pyserial
* SCS root: scs_core
* SCS host: scs_host_bbe or scs_host_rpi


**Branches:**

The stable branch of this repository is master. For deployment purposes, use:

    git clone --branch=master https://github.com/south-coast-science/scs_ndir_alphasense.git
