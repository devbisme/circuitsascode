# The MIT License (MIT) - Copyright (c) 2021 devbisme

"""
This module provides both resistive and capacitive voltage dividers.

The only required parameter is the ratio of the output voltage w.r.t
the input voltage. The resistance/capacitance of each leg of the divider
is computed using this ratio.

Optional parameters include:
    * the total resistance/capacitance of both legs of the divider,
    * the resistor/capacitor tolerance as given by the E series (https://www.wikiwand.com/en/E_series_of_preferred_numbers),
    * and a resistor/capacitor part template that's used to instantiate both legs of the divider.
"""

from skidl import TEMPLATE, Interface, Net, Part, SubCircuit, generate_netlist

from circuitsascode import units
from circuitsascode.utilities import find_nearest_c, find_nearest_r


@SubCircuit
def v_div_r(
    ratio,
    r_total=10 * units.kohm,
    part_dict={},
    dflt_part_dict={
        "r": Part(
            lib="Device",
            name="R",
            e_series="E24",
            dest=TEMPLATE,
            footprint="Resistor_SMD:R_0603_1608Metric",
        ),
    },
):
    """Creates a resistor voltage divider.

    Args:
        ratio (float): Voltage division ratio in the range [0, 1].
        r_total (float, optional): Total resistance of both legs of the divider. Defaults to 10 KOhm.
        part_dict (dict, optional): Dictionary of user-supplied {part name: Part template} entries that are used to build the circuit.
        dflt_part_dict(dict, optional): Dictionary of default parts that will be used if corresponding entires do not exist in the part_dict argument.

    Returns:
        Interface:
        An Interface object containing the following I/O
            * vin:  Input voltage to top leg of divider.
            * vout: Output voltage from junction of upper & lower legs of divider.
            * gnd:  Reference voltage (usually ground) to bottom leg of divider.

    Example:
        >>> from circuitsascode.simple.v_div import *
        >>> div1 = v_div_r(ratio=0.3, r_total=100*units.kohm)
        >>> vin = Net("VIN")
        >>> vout = Net("VOUT")
        >>> gnd = Net("GND")
        >>> div1["vin vout gnd"] += vin, vout, gnd
        >>> generate_netlist() # doctest: +ELLIPSIS
        '(...
        >>> len(vin)
        1
        >>> len(vout)
        2
        >>> len(gnd)
        1
    """

    assert 0 <= ratio <= 1

    # Create the dict of parts to be used in the circuit, starting with the default parts
    # and then overwriting them with any user-supplied parts.
    parts = {k: v for d in [dflt_part_dict, part_dict] for k, v in d.items()}

    # Instantiate the needed parts from the part dictionary.
    r_u, r_l = 2 * parts["r"]  # Upper and lower resistors for setting the voltage.

    # Set the resistance of the lower leg of the divider.
    r_l.value = ratio * r_total
    r_l.value = find_nearest_r(r_l)

    # Set the resistance of the upper leg of the divider.
    r_u.value = (1 - ratio) * r_total
    r_u.value = find_nearest_r(r_u)

    # Attach upper and lower legs of divider.
    r_u[1, 2] & r_l[1, 2]

    # Return an interface to the divider with:
    #    vin: Input voltage to upper leg of divider.
    #    vout: Output voltage from junction of upper & lower legs of divider.
    #    gnd: Reference voltage (usually ground) to lower leg of divider.
    return Interface(vin=r_u[1], vout=r_l[1], gnd=r_l[2])


@SubCircuit
def v_div_c(
    ratio,
    c_total=1 * units.ufarad,
    part_dict={},
    dflt_part_dict={
        "c": Part(
            lib="Device",
            name="C",
            e_series="E12",
            dest=TEMPLATE,
            footprint="Capacitor_SMD:C_0603_1608Metric",
        ),
    },
):
    """Creates a capacitor voltage divider.

    Args:
        ratio (float): Voltage division ratio in the range [0, 1].
        c_total (float, optional): Total capacitance of both legs of the divider. Defaults to 1 microfarad.
        part_dict (dict, optional): Dictionary of user-supplied {part name: Part template} entries that are used to build the circuit.
        dflt_part_dict(dict, optional): Dictionary of default parts that will be used if corresponding entires do not exist in the part_dict argument.

    Returns:
        Interface:
        An Interface object with the following I/O
            * vin:  Input voltage to upper leg of divider.
            * vout: Output voltage from junction of upper & lower legs of divider.
            * gnd:  Reference voltage (usually ground) to lower leg of divider.

    Example:
        >>> from circuitsascode.simple.v_div import *
        >>> div1 = v_div_c(ratio=0.3, c_total=100*units.nanofarad)
        >>> vin = Net("VIN")
        >>> vout = Net("VOUT")
        >>> gnd = Net("GND")
        >>> div1["vin vout gnd"] += vin, vout, gnd
        >>> generate_netlist() # doctest: +ELLIPSIS
        '(...
        >>> len(vin)
        1
        >>> len(vout)
        2
        >>> len(gnd)
        1
    """

    assert 0 <= ratio <= 1

    # Create the dict of parts to be used in the circuit, starting with the default parts
    # and then overwriting them with any user-supplied parts.
    parts = {k: v for d in [dflt_part_dict, part_dict] for k, v in d.items()}

    # Instantiate the needed parts from the part dictionary.
    c_u, c_l = 2 * parts["c"]  # Upper and lower capacitors for setting the voltage.

    # Set the capacitance of the lower leg of the divider.
    c_l.value = (1 - ratio) * c_total
    c_l.value = find_nearest_c(c_l)

    # Set the capacitance of the upper leg of the divider.
    c_u.value = ratio * c_total
    c_u.value = find_nearest_c(c_u)

    # Attach upper and lower legs of the divider.
    c_u[1, 2] & c_l[1, 2]

    # Return an interface to the divider with:
    #    vin: Input voltage to upper leg of divider.
    #    vout: Output voltage from junction of upper & lower legs of divider.
    #    gnd: Reference voltage (usually ground) to bottom leg of divider.
    return Interface(vin=c_u[1], vout=c_l[1], gnd=c_l[2])
