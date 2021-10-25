# The MIT License (MIT) - Copyright (c) 2021 Dave Vandenbout.

from .setup_teardown import setup_function, teardown_function  # isort:skip

from casc.interfaces.pmod import (
    pmod_plug_6,
    pmod_plug_12,
    pmod_socket_6,
    pmod_socket_12,
)
from casc.utilities import units
from skidl import Net


def test_pmod_1():
    j1 = pmod_plug_6()
    j2 = pmod_socket_6()
    j3 = pmod_plug_12()
    j4 = pmod_socket_12()

    j1["io[0:3]"] += j2["io[0:3]"]
    j3["io[0:7]"] += j4["io[0:7]"]

    vcc, gnd = Net("VCC"), Net("GND")
    vcc += j1["VCC"], j2["VCC"], j3["VCC"], j4["VCC"]
    gnd += j1["GND"], j2["GND"], j3["GND"], j4["GND"]

    assert len(vcc) == 6
    assert len(gnd) == 6
