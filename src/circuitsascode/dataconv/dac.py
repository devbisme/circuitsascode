# The MIT License (MIT) - Copyright (c) 2021 devbisme

"""
This module provides some digital-to-analog converters (DACs).
"""

from skidl import TEMPLATE, Bus, Interface, Net, Part, SubCircuit, generate_netlist

from circuitsascode import units
from circuitsascode.utilities import find_nearest_c, find_nearest_r


@SubCircuit
def dac_r2r(
    n_bits=5,
    r_val=1000 * units.ohm,
    e_series="E96",
    r_temp=Part(
        "Device", "R", dest=TEMPLATE, footprint="Resistor_SMD:R_0603_1608Metric"
    ),
):
    """
    Creates an unbuffered R-2R DAC using a resistor ladder. (https://www.wikiwand.com/en/Resistor_ladder)

    Args:
        n_bits (int, optional): Number of bits of resolution.
        r_val (float, optional): Base ladder resistor value. Defaults to 1 KOhm.
        e_series (string, optional): E-series of resistor value (E3, E6, E12, E24, E48, E96, E192). Defaults to "E96" (1%).
        r_temp (Part): Part template for creating resistors. Defaults to two-pin, surface-mount 0603 footprint.

    Returns:
        Interface:
        An Interface object containing the following I/O
            * din:  Digital input bus of width n_bits.
            * vout: DAC output voltage.
            * gnd:  Ground reference.

    Example:
        >>> from circuitsascode.dataconv.dac import *
        >>> din = Bus("DIN", 3)
        >>> vout = Net("VOUT")
        >>> gnd = Net("GND")
        >>> dac = dac_r2r(n_bits=len(din))
        >>> dac.din += din
        >>> dac.gnd += gnd
        >>> dac.vout += vout
        >>> generate_netlist() # doctest: +ELLIPSIS
        '(...
        >>> len(din)
        3
        >>> len(vout)
        2
        >>> len(gnd)
        1
    """

    # DAC must have more than 1 bit of resolution, otherwise what's the point?
    assert n_bits > 1

    # Set R and 2R resistor templates to the nearest standard resistor values.
    r1_val = find_nearest_r(r_val, e_series)
    r2_val = find_nearest_r(2 * r1_val, e_series)
    r1_t = r_temp(dest=TEMPLATE, value=r1_val)
    r2_t = r_temp(dest=TEMPLATE, value=r2_val)

    gnd = Net()  # Ground reference.
    din = Bus(n_bits)  # Digital input bus.
    vo = Net()  # Analog output net from each DAC bit.

    # LSB of DAC.
    gnd & r2_t() & vo & r2_t() & din[0]

    # Iterate through remaining DAC bits, stopping after MSB is reached.
    for b in range(1, n_bits):
        voo = Net()  # Output from current DAC bit.
        vo & r1_t() & voo & r2_t() & din[b]
        vo = voo  # Pass output from DAC bit to the next stage.

    # Return the interface to the DAC circuitry.
    return Interface(din=din, vout=vo, gnd=gnd)
