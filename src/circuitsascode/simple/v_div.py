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

from skidl import TEMPLATE, Interface, Part, SubCircuit

from circuitsascode import units
from circuitsascode.utilities import find_nearest_c, find_nearest_r


@SubCircuit
def v_div_r(
    ratio,
    r_total=10 * units.kohm,
    e_series="E24",
    r_temp=Part(
        "Device", "R", dest=TEMPLATE, footprint="Resistor_SMD:R_0603_1608Metric"
    ),
):
    """Creates a resistor voltage divider.

    Args:
        ratio (float): Voltage division ratio in the range [0, 1].
        r_total (float, optional): Total resistance of both legs of the divider. Defaults to 10 KOhm.
        e_series (string, optional): E-series of resistor values (E3, E6, E12, E24, E48, E96, E192). Defaults to "E24" (5%).
        r_temp (Part): Part template for creating divider resistors. Defaults to two-pin, surface-mount 0603 footprint.

    Returns:
        Interface:
        An Interface object containing the following I/O
            * vin:  Input voltage to top leg of divider.
            * vout: Output voltage from junction of upper & lower legs of divider.
            * gnd:  Reference voltage (usually ground) to bottom leg of divider.

    Example:
        >>> from circuitsascode.simple.v_div import *
        >>> div1 = v_div_r(ratio=0.3, r_total=100*units.kohm, e_series='E12')
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

    # Create lower leg of resistor divider.
    r_low = find_nearest_r(ratio * r_total, e_series)
    r_l = r_temp(value=r_low)

    # Create upper leg of resistor divider.
    r_high = find_nearest_r((1 - ratio) * r_total, e_series)
    r_h = r_temp(value=r_high)

    # Attach upper and lower legs of resistor divider.
    r_h[1, 2] & r_l[1, 2]

    # Return an interface to the resistor divider with:
    #    vin: Input voltage to top leg of divider.
    #    vout: Output voltage from junction of upper & lower legs of divider.
    #    gnd: Reference voltage (usually ground) to bottom leg of divider.
    return Interface(vin=r_h[1], vout=r_l[1], gnd=r_l[2])


@SubCircuit
def v_div_c(
    ratio,
    c_total=1000 * units.nanofarad,
    e_series="E12",
    c_temp=Part(
        "Device", "C", dest=TEMPLATE, footprint="Capacitor_SMD:C_0603_1608Metric"
    ),
):
    """Creates a capacitor voltage divider.

    Args:
        ratio (float): Voltage division ratio in the range [0, 1].
        c_total (float, optional): Total capacitance of both legs of the divider. Defaults to 1000 nanofarads.
        e_series (string, optional): E-series of capacitor values (E3, E6, E12, E24, E48, E96, E192). Defaults to "E12" (10%).
        c_temp (Part): Part template for creating divider capacitors. Defaults to two-pin, surface-mount 0603 footprint.

    Returns:
        Interface:
        An Interface object with the following I/O
            * vin:  Input voltage to top leg of divider.
            * vout: Output voltage from junction of upper & lower legs of divider.
            * gnd:  Reference voltage (usually ground) to bottom leg of divider.

    Example:
        >>> from circuitsascode.simple.v_div import *
        >>> div1 = v_div_c(ratio=0.3, c_total=100*units.nanofarad, e_series='E24')
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

    # Create lower leg of capacitor divider.
    c_low = find_nearest_c((1 - ratio) * c_total, e_series)
    c_l = c_temp(value=c_low)

    # Create upper leg of capacitor divider.
    c_high = find_nearest_c(ratio * c_total, e_series)
    c_h = c_temp(value=c_high)

    # Attach upper and lower legs of capacitor divider.
    c_h[1, 2] & c_l[1, 2]

    # Return an interface to the capacitor divider with:
    #    vin: Input voltage to top leg of divider.
    #    vout: Output voltage from junction of upper & lower legs of divider.
    #    gnd: Reference voltage (usually ground) to bottom leg of divider.
    return Interface(vin=c_h[1], vout=c_l[1], gnd=c_l[2])
