# The MIT License (MIT) - Copyright (c) 2021 Dave Vandenbout.

from .setup_teardown import setup_function, teardown_function  # isort:skip

from casc.simple.v_div import v_div_c, v_div_r
from casc.utilities import units
from skidl import Net, generate_netlist


def test_v_div_r_1():
    div1 = v_div_r(ratio=0.3, r_total=100 * units.kohm)
    vin = Net("VIN")
    vout = Net("VOUT")
    gnd = Net("GND")
    div1["vin vout gnd"] += vin, vout, gnd
    generate_netlist()
    assert len(vin) == 1
    assert len(vout) == 2
    assert len(gnd) == 1


def test_v_div_c_1():
    div1 = v_div_c(ratio=0.3, c_total=100 * units.nanofarad)
    vin = Net("VIN")
    vout = Net("VOUT")
    gnd = Net("GND")
    div1["vin vout gnd"] += vin, vout, gnd
    generate_netlist()  # doctest: +ELLIPSIS
    len(vin) == 1
    len(vout) == 2
    len(gnd) == 1
