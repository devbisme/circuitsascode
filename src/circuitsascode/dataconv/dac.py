# The MIT License (MIT) - Copyright (c) 2021 devbisme

"""
This module provides some digital-to-analog converters (DACs).
"""

from skidl import TEMPLATE, Bus, Interface, Net, Part, SubCircuit, generate_netlist

from circuitsascode import units
from circuitsascode.utilities import find_nearest_c, find_nearest_r

# Set default resistor value and precision for the R2R DAC.
DFLT_RESISTANCE = 1.0 * units.kohm
DFLT_E_SERIES = "E96"


@SubCircuit
def dac_r2r(
    n_bits=5,
    part_dict={},
    dflt_part_dict={
        "r": Part(
            "Device",
            "R",
            value=DFLT_RESISTANCE,
            e_series="E96",
            dest=TEMPLATE,
            footprint="Resistor_SMD:R_0603_1608Metric",
        ),
    },
):
    """R-2R digital-to-analog converter.

    Creates an unbuffered R-2R DAC using a resistor ladder. (https://www.wikiwand.com/en/Resistor_ladder)
    The part dictionary contains a single resistor template that is instantiated using R and 2*R values.

    Args:
        n_bits (int, optional): Number of bits of resolution.
        part_dict (dict, optional): Dictionary of user-supplied {part name: Part template} entries that are used to build the circuit.
        dflt_part_dict(dict, optional): Dictionary of default parts that will be used if corresponding entires do not exist in the part_dict argument.

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
        >>> dac["din vout gnd"] += din, vout, gnd
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

    # Create the dict of parts to be used in the circuit, starting with the default parts
    # and then overwriting them with any user-supplied parts.
    parts = {k: v for d in [dflt_part_dict, part_dict] for k, v in d.items()}

    # Set R and 2R resistor templates to the nearest standard resistor values.
    r_t = parts["r"]  # Base reistor template.
    r_val = getattr(r_t, "value", DFLT_RESISTANCE)
    e_series = getattr(r_t, "e_series", DFLT_E_SERIES)
    r1_val = find_nearest_r(r_val, e_series)
    r2_val = find_nearest_r(2 * r1_val, e_series)
    r1_t = r_t(dest=TEMPLATE, value=r1_val)
    r2_t = r_t(dest=TEMPLATE, value=r2_val)

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
