# The MIT License (MIT) - Copyright (c) 2021 Dave Vandenbout.

from .setup_teardown import setup_function, teardown_function  # isort:skip

from casc.utilities import units
from casc.vregs.linear import adj_vreg
from skidl import Net, generate_netlist


def test_vreg_1():
    vrg = adj_vreg(v_out=2.5 * units.volt, r_total=100 * units.kohm)
    vin = Net("VIN")
    vout = Net("VOUT")
    gnd = Net("GND")
    vrg["vin vout gnd"] += vin, vout, gnd
    generate_netlist()
    assert len(vin) == 2
    assert len(vout) == 3
    assert len(gnd) == 3
