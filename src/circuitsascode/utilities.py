# The MIT License (MIT) - Copyright (c) 2021 devbisme

"""
Utility functions.
"""

import eseries

from circuitsascode import units

__all__ = ("apply_units", "find_nearest_r", "find_nearest_c")


def series_key_from_name(name):
    """Get an ESeries from its name.

    Args:
        name: The series name as a string, for example 'E24'

    Returns:
        An ESeries object which can be uses as a series_key.

    Raises:
        ValueError: If no such series exists.
    """
    try:
        return eseries.ESeries[name]
    except KeyError:
        raise ValueError(
            "E-series with name {!r} not found. Available E-series keys are {}".format(
                name, ", ".join(str(key.name) for key in eseries.series_keys())
            )
        )


def apply_units(v, units):
    """Apply unit to a dimensionless value. Return dimensional values unchanged.

    Args:
        v (numeric, unit): The value to which units will be applied.
        units (unit): Unit to apply to the value.

    Returns:
        unit: A value with a Pint unit applied to it.

    Example:
        >>> from circuitsascode.utilities import *
        >>> apply_units(5, units.volts)
        <Quantity(5, 'volt')>
        >>> apply_units(10 * units.ohms, units.kohms)
        <Quantity(10, 'ohm')>
        >>> apply_units(1000000 * units.volts, units.volts)
        <Quantity(1.0, 'megavolt')>
    """

    if isinstance(v, type(1 * units)):
        # Value already has a unit.
        return v.to_compact()
    else:
        # Dimensionless quantity, so apply unit to it.
        return (v * units).to_compact()


def _find_nearest(v, dflt_unit, e_series="E24"):

    # Get the value and E-series attributes if the passed-in argument is a Part.
    # Otherwise, use the passed-in value and E-series.
    e_series = getattr(v, "e_series", e_series)
    v = getattr(v, "value", v)

    # Make sure value has units attached to it.
    v = apply_units(v, dflt_unit)

    # Get E series of values.
    try:
        series = series_key_from_name(e_series)
    except ValueError:
        # Unknown E-series, so just return the value unchanged.
        return v
    else:
        # Return the E-series value nearest to the given value.
        return eseries.find_nearest(series, v.magnitude) * v.units


def find_nearest_r(r, e_series="E24"):
    """Find the nearest E-series resistor value to the given value.

    Args:
        r (numeric/Part, unit): Resistor Part or resistance as a number with or without an attached Pint Ohm unit.
        e_series (string, optional): E-series of resistor values (E3, E6, E12, E24, E48, E96, E192). Defaults to "E24" (5%).

    Returns:
        unit: The closest E-series value with Pint Ohm unit attached.

    Example:
        >>> from circuitsascode.utilities import *
        >>> find_nearest_r(350)
        <Quantity(360.0, 'ohm')>
        >>> find_nearest_r(350 * units.kohm, "E12")
        <Quantity(330.0, 'kiloohm')>
    """

    return _find_nearest(r, units.ohm, e_series)


def find_nearest_c(c, e_series="E24"):
    """Find the nearest E-series capacitor value to the given value.

    Args:
        c (numeric/Part, unit): Capacitor Part or capacitance as a number with or without an attached Pint nanofarad unit.
        e_series (string, optional): E-series of capacitor values (E3, E6, E12, E24, E48, E96, E192). Defaults to "E24" (5%).

    Returns:
        unit: The closest E-series value with Pint Farad unit attached.

    Example:
        >>> from circuitsascode.utilities import *
        >>> find_nearest_c(350)
        <Quantity(360.0, 'nanofarad')>
        >>> find_nearest_r(350 * units.microfarad, "E12")
        <Quantity(330.0, 'microfarad')>
    """

    return _find_nearest(c, units.nanofarad, e_series)
