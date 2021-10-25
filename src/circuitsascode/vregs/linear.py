# The MIT License (MIT) - Copyright (c) 2021 devbisme

"""
This module provides circuits based upon linear voltage regulators.
"""

import sympy as sp
from skidl import TEMPLATE, Interface, Net, Part, SubCircuit, generate_netlist

from circuitsascode import units
from circuitsascode.utilities import apply_units, find_nearest_c, find_nearest_r

# These are default values for the regulator's reference voltage and ADJ terminal current.
DFLT_V_REF = 1.25 * units.volt
DFLT_I_ADJ = 50 * units.uamp

# Sympy is used to derive the equations for the resistor divider values that set the
# output voltage. Two sets of equations are derived: one with the ADJ terminal current != 0
# and another with it set to zero. (The second set is needed because the first set
# becomes indeterminate when the current goes to zero.)
r1, r2, r_total, i_adj, v_ref, v_out = sp.symbols(
    "r1, r2, r_total, i_adj, v_ref, v_out"
)
r1_r2_i_adj_solutions = sp.solve(
    (r_total - r1 - r2, -v_out + v_ref * (1 + r2 / r1) + i_adj * r2),
    (r1, r2),
    dict=True,
)
r1_r2_solutions = sp.solve(
    (r_total - r1 - r2, -v_out + v_ref * (1 + r2 / r1)), (r1, r2), dict=True
)

# Create functions for the R1/R2 resistor values when the ADJ terminal current != 0.
calc_r1_i_adj_val = sp.lambdify(
    (v_out, r_total, v_ref, i_adj), r1_r2_i_adj_solutions[1][r1]
)
calc_r2_i_adj_val = sp.lambdify(
    (v_out, r_total, v_ref, i_adj), r1_r2_i_adj_solutions[1][r2]
)

# Create functions for the R1/R2 resistor values when the ADJ terminal current == 0.
calc_r1_val = sp.lambdify((v_out, r_total, v_ref), r1_r2_solutions[0][r1])
calc_r2_val = sp.lambdify((v_out, r_total, v_ref), r1_r2_solutions[0][r2])


@SubCircuit
def adj_vreg(
    v_out=3.3 * units.volts,
    r_total=10 * units.kohm,
    part_dict={},
    dflt_part_dict={
        "vreg": Part(
            lib="Regulator_Linear",
            name="AZ1117-ADJ",
            v_ref=DFLT_V_REF,
            i_adj=DFLT_I_ADJ,
            dest=TEMPLATE,
            footprint="Package_TO_SOT_SMD:SOT-223-3_TabPin2",
        ),
        "r": Part(
            lib="Device",
            name="R",
            e_series="E48",
            dest=TEMPLATE,
            footprint="Resistor_SMD:R_0603_1608Metric",
        ),
        "c_in": Part(
            lib="Device",
            name="C",
            value=10 * units.ufarad,
            e_series="E12",
            dest=TEMPLATE,
            footprint="Capacitor_SMD:C_0603_1608Metric",
        ),
        "c_out": Part(
            lib="Device",
            name="C",
            value=22 * units.ufarad,
            e_series="E12",
            dest=TEMPLATE,
            footprint="Capacitor_SMD:C_0805_2012Metric",
        ),
    },
):
    """Linear voltage regulator.

    Creates a voltage regulator with input/output filter capacitors and appropriately-sized resistors to set
    the output voltage of an adjustable, three-terminal regulator.

    Args:
        v_out (float): Desired output voltage of the regulator.
        r_total (float, optional): Total resistance of the resistor divider that sets the output voltage. Defaults to 10 KOhm.
        part_dict (dict, optional): Dictionary of user-supplied {part name: Part template} entries that are used to build the circuit.
        dflt_part_dict(dict, optional): Dictionary of default parts that will be used if corresponding entires do not exist in the part_dict argument.

    Returns:
        Interface:
        An Interface object containing the following I/O
            * vin:  Unregulated input voltage.
            * vout: Regulated output voltage.
            * gnd:  Reference voltage (usually ground).

    Example:
        >>> from circuitsascode.vregs.linear import adj_vreg
        >>> vrg = adj_vreg(v_out=2.5 * units.volt, r_total=100 * units.kohm)
        >>> vin = Net("VIN")
        >>> vout = Net("VOUT")
        >>> gnd = Net("GND")
        >>> vrg["vin vout gnd"] += vin, vout, gnd
        >>> generate_netlist() # doctest: +ELLIPSIS
        '(...
        >>> len(vin)
        2
        >>> len(vout)
        3
        >>> len(gnd)
        3
    """

    # Create the dict of parts to be used in the circuit, starting with the default parts
    # and then overwriting them with any user-supplied parts.
    parts = {k: v for d in [dflt_part_dict, part_dict] for k, v in d.items()}

    # Instantiate the needed parts from the part dictionary.
    vreg = parts["vreg"]()  # Adjustable voltage regulator.
    c_in = parts["c_in"]()  # Input filter capacitor.
    c_out = parts["c_out"]()  # Output filter capacitor.
    r1, r2 = 2 * parts["r"]  # Resistors for setting the output voltage.

    # Get the reference voltage and ADJ terminal current for the adjustable regulator.
    # Use default values if they aren't provided by the Part object.
    v_ref = getattr(vreg, "v_ref", DFLT_V_REF)
    i_adj = getattr(vreg, "i_adj", DFLT_I_ADJ)

    # The regulated output must be greater than the regulator's reference voltage.
    v_out = apply_units(v_out, units.volt)
    assert v_out > v_ref

    # The total resistance of both resistors must be greater than zero.
    r_total = apply_units(r_total, units.kohm)
    assert r_total > 0

    # Compute the resistor values needed to create the regulated output voltage.
    if i_adj < (v_out / r_total) / 1000:
        # Ignore i_adj because it is small compared to the current thru the resistors.
        r1.value = calc_r1_val(v_out, r_total, v_ref)
        r2.value = calc_r2_val(v_out, r_total, v_ref)
    else:
        # i_adj cannot be ignored because it is large enough to affect the output voltage.
        r1.value = calc_r1_i_adj_val(v_out, r_total, v_ref, i_adj)
        r2.value = calc_r2_i_adj_val(v_out, r_total, v_ref, i_adj)

    # Round the resistor and capacitor values to their nearest E-series values.
    r1.value = find_nearest_r(r1)
    r2.value = find_nearest_r(r2)
    c_in.value = find_nearest_c(c_in)
    c_out.value = find_nearest_c(c_out)

    # Connect the parts to create the voltage regulator.
    gnd = Net()

    # Attach filter capacitors to the input and output.
    vreg.VI & c_in & gnd
    vreg.VO & c_out & gnd

    # Attach resistor divider from the output to the ADJ pin and then to ground.
    vreg.VO & r1 & vreg.ADJ & r2 & gnd

    # Return an interface to the voltage regulator with:
    #    vin: Unregulated input voltage.
    #    vout: Regulated output voltage.
    #    gnd: Reference voltage (usually ground).
    return Interface(vin=vreg.VI, vout=vreg.VO, gnd=gnd)
