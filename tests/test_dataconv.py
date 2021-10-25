# The MIT License (MIT) - Copyright (c) 2021 Dave Vandenbout.

from .setup_teardown import setup_function, teardown_function  # isort:skip

from casc.dataconv.dac import dac_r2r
from casc.utilities import units
from skidl import Bus, Net, generate_netlist


def test_dac_1():
    din = Bus("DIN", 3)
    vout = Net("VOUT")
    gnd = Net("GND")
    dac = dac_r2r(n_bits=len(din))
    dac["din vout gnd"] += din, vout, gnd
    generate_netlist()
    len(din) == 3
    len(vout) == 2
    len(gnd) == 1
