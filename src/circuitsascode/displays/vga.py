# The MIT License (MIT) - Copyright (c) 2021 xesscorp

import skidl
from casc import units
from skidl import (  # generate_pcb
    ERC,
    NC,
    POWER,
    TEMPLATE,
    Bus,
    Interface,
    Net,
    Part,
    SubCircuit,
    generate_netlist,
)

import circuitsascode as casc
from circuitsascode.utilities import apply_units, find_nearest_r


@SubCircuit
def vga(rgb=None, e_series="E12", logic_lvl=3.3 * units.volts):
    """Analog-RGB VGA port driven by red, grn, blu digital color buses.

    Takes list of red, green and blue bus widths and creates a resistor network
    to convert the digital color buses to analog RGB signals that are output
    through a DB-15 connector.

    Args:
        rgb (list, optional): List of integer widths for the red, green and blue buses. Defaults to (3, 3, 3).
        e_series (str, optional): E-series of resistor values (E3, E6, E12, E24, E48, E96, E192). Defaults to "E12" (10%).
        logic_lvl (float, optional): V_hi voltage for digital signals. Defaults to 3.3V.

    Returns:
        Interface:
        An Interface object containing the following I/O
            * red:   Input bus for red component.
            * grn:   Input bus for green component.
            * blu:   Input bus for blue component.
            * hsync: Output net for horizontal sync.
            * vsync: Output net for vertical sync.
            * gnd:   Ground net.

    Example:
        >>> from circuitsascode.displays.vga import vga
        >>> red, grn, blu = Bus(5), Bus(4), Bus(3)
        >>> hsync, vsync, gnd = Net(), Net(), Net()
        >>> vga1 = vga(rgb=(len(red), len(grn), len(blu)))
        >>> vga1.red += red
        >>> vga1.grn += grn
        >>> vga1.blu += blu
        >>> vga1.hsync += hsync
        >>> vga1.vsync += vsync
        >>> vga1.gnd += gnd
    """

    # Substitute default RGB bus widths if needed.
    if rgb is None:
        rgb = (3, 3, 3)

    # Apply volts unit to logic level.
    logic_lvl = apply_units(logic_lvl, units.volts)

    # Create buses and nets for connections.
    red, grn, blu = Bus(rgb[0]), Bus(rgb[1]), Bus(rgb[2])
    hsync, vsync, gnd = Net(), Net(), Net()

    # Create the VGA interface circuitry.
    # _vga_subckt(red, grn, blu, hsync, vsync, gnd, e_series=e_series, logic_lvl=logic_lvl)

    # Determine the color depth by finding the max width of the digital color buses.
    # (Note that the color buses don't have to be the same width.)
    depth = max(rgb)

    # Add extra bus lines to any bus that's smaller than the depth and
    # connect these extra lines to the original LSB bit of the bus.
    exp_red = Bus([red[0] for _ in range(depth - len(red))], red[:])
    exp_grn = Bus([grn[0] for _ in range(depth - len(grn))], grn[:])
    exp_blu = Bus([blu[0] for _ in range(depth - len(blu))], blu[:])

    # Calculate the resistor weights to support the given color depth.
    vga_input_impedance = 75.0 * units.ohms  # Impedance of VGA analog inputs.
    vga_analog_max = 0.7 * units.volts  # Maximum brightness color voltage.
    # Compute the resistance of the upper leg of the voltage divider that will
    # drop the logic_lvl to the vga_analog_max level if the lower leg has
    # a resistance of vga_input_impedance.
    R = (logic_lvl - vga_analog_max) * vga_input_impedance / vga_analog_max
    # The basic weight is R * (1 + 1/2 + 1/4 + ... + 1/2**(width-1))
    r = R * sum([1.0 / 2 ** n for n in range(depth)])
    # The most significant color bit has a weight of r. The next bit has a weight
    # of 2r. The next bit has a weight of 4r, and so on. The weights are arranged
    # in decreasing order so the least significant weight is at the start of the list.
    weights = [r * 2 ** n for n in reversed(range(depth))]

    # Convert resistor weights into standard values.
    weights = [find_nearest_r(w, e_series=e_series) for w in weights]

    # Quad resistor packs are used to create weighted sums of the digital
    # signals on the red, green and blue buses. (One resistor in each pack
    # will not be used since there are only three colors.)
    res_network = Part(
        lib="Device",
        name="R_Pack04",
        footprint="Resistor_SMD:R_Array_Concave_4x0603",
        dest=TEMPLATE,
    )

    # Create a list of resistor packs, one for each weight.
    res = res_network(value=weights)

    # Create the nets that will accept the weighted sums.
    analog_red = Net("R")
    analog_grn = Net("G")
    analog_blu = Net("B")

    # Match each resistor pack (least significant to most significant) with
    # the the associated lines of each color bus (least significant to
    # most significant) as follows:
    #    res[0], red[0], grn[0], blu[0]
    #    res[1], red[1], grn[1], blu[1]
    #    ...
    # Then attach the individual resistors in each pack between
    # a color bus line and the associated analog color net:
    #    red[0] --- (1)res[0](8) --- analog_red
    #    grn[0] --- (2)res[0](7) --- analog_grn
    #    blu[0] --- (3)res[0](6) --- analog_blu
    #    red[1] --- (1)res[1](8) --- analog_red
    #    grn[1] --- (2)res[1](7) --- analog_grn
    #    blu[1] --- (3)res[1](6) --- analog_blu
    #    ...
    for w, r, g, b in zip(res, exp_red, exp_grn, exp_blu):
        w[:] += skidl.NC  # Attach unused pins to no-connect.
        r & w[1, 8] & analog_red  # Red uses the 1st resistor in each pack.
        g & w[2, 7] & analog_grn  # Green uses the 2nd resistor in each pack.
        b & w[3, 6] & analog_blu  # Blue uses the 3rd resistor in each pack.

    # VGA connector outputs the analog red, green and blue signals and the syncs.
    vga_conn = Part(
        lib="Connector",
        name="DB15_Female_HighDensity_MountingHoles",
        footprint="Connector_Dsub:DSUB-15-HD_Female_Horizontal_P2.29x1.98mm_EdgePinOffset3.03mm_Housed_MountingHolesOffset4.94mm",
    )
    vga_conn[5, 6, 7, 8, 9, 10] += gnd  # Ground pins.
    vga_conn[4, 11, 12, 15] += NC  # Unconnected pins.
    vga_conn[0] += gnd  # Ground connector shield.
    vga_conn[1] += analog_red  # Analog red signal.
    vga_conn[2] += analog_grn  # Analog green signal.
    vga_conn[3] += analog_blu  # Analog blue signal.
    vga_conn[13] += hsync  # Horizontal sync.
    vga_conn[14] += vsync  # Vertical sync.

    # Return an interface to the VGA circuitry.
    return Interface(red=red, grn=grn, blu=blu, hsync=hsync, vsync=vsync, gnd=gnd)


if __name__ == "__main__":
    from circuitsascode.interfaces.pmod import pmod_plug_12

    # Define some nets and buses.

    gnd = Net("GND")  # Ground reference.
    gnd.drive = POWER

    # Five-bit digital buses carrying red, green, blue color values.
    # red = Bus("RED", 5)
    # grn = Bus("GRN", 5)
    # blu = Bus("BLU", 5)
    # Digital buses of varying widths carrying red, green, blue color values.
    red = Bus("RED", 5)
    grn = Bus("GRN", 4)
    blu = Bus("BLU", 3)

    # VGA horizontal and vertical sync signals.
    hsync = Net("HSYNC")
    vsync = Net("VSYNC")

    # Two PMOD headers and a breadboard header bring in the digital red, green,
    # and blue buses along with the horizontal and vertical sync.
    # The PMOD and breadboard headers bring in the same signals. PMOD connectors
    # are used when the VGA interface connects to a StickIt! motherboard, and the
    # breadboard header is for attaching it to a breadboard.
    pm = pmod_plug_12(), pmod_plug_12()
    bread_board_conn = Part(
        "Connector",
        "Conn_01x18_Male",
        footprint="Connector_PinHeader_2.54mm:PinHeader_1x18_P2.54mm_Vertical",
    )

    # Connect the digital red, green and blue buses and the sync signals to
    # the pins of the PMOD and breadboard headers.
    hsync += bread_board_conn[1], pm[0]["IO0"]
    vsync += bread_board_conn[2], pm[0]["IO1"]
    # red[4] += bread_board_conn[3], pm[0]["IO2"]
    # grn[4] += bread_board_conn[4], pm[0]["IO3"]
    # blu[4] += bread_board_conn[5], pm[0]["IO4"]
    # red[3] += bread_board_conn[6], pm[0]["IO5"]
    # grn[3] += bread_board_conn[7], pm[0]["IO6"]
    # blu[3] += bread_board_conn[8], pm[0]["IO7"]
    # red[2] += bread_board_conn[9], pm[1]["IO0"]
    # grn[2] += bread_board_conn[10], pm[1]["IO1"]
    # blu[2] += bread_board_conn[11], pm[1]["IO2"]
    # red[1] += bread_board_conn[12], pm[1]["IO3"]
    # grn[1] += bread_board_conn[13], pm[1]["IO4"]
    # blu[1] += bread_board_conn[14], pm[1]["IO5"]
    # red[0] += bread_board_conn[15], pm[1]["IO6"]
    # grn[0] += bread_board_conn[16], pm[1]["IO7"]
    # blu[0] += bread_board_conn[17]
    red[4] += bread_board_conn[3], pm[0]["IO2"]
    red[3] += bread_board_conn[6], pm[0]["IO5"]
    red[2] += bread_board_conn[9], pm[1]["IO0"]
    red[1] += bread_board_conn[12], pm[1]["IO3"]
    red[0] += bread_board_conn[15], pm[1]["IO6"]
    grn[3] += bread_board_conn[4], pm[0]["IO3"]
    grn[2] += bread_board_conn[7], pm[0]["IO6"]
    grn[1] += bread_board_conn[10], pm[1]["IO1"]
    grn[0] += bread_board_conn[13], pm[1]["IO4"]
    blu[2] += bread_board_conn[5], pm[0]["IO4"]
    blu[1] += bread_board_conn[8], pm[0]["IO7"]
    blu[0] += bread_board_conn[11], pm[1]["IO2"]

    # The VGA interface has no active components, so don't connect the PMOD's VCC pins.
    NC += pm[0]["VCC"], pm[1]["VCC"]

    # Connect the ground reference pins on all the connectors.
    gnd += bread_board_conn[18], pm[0]["GND"], pm[1]["GND"]

    # The PMOD ground pins are defined as power outputs so there will be an error
    # if they're connected together. Therefore, turn off the error checking on one
    # of them to swallow the error.
    pm[1]["GND"].do_erc = False

    # Send the RGB buses and syncs to the VGA port circuit.
    vga1 = vga(rgb=(len(red), len(grn), len(blu)))
    vga1.red += red
    vga1.grn += grn
    vga1.blu += blu
    vga1.hsync += hsync
    vga1.vsync += vsync
    vga1.gnd += gnd

    ERC()  # Run error checks.
    # generate_pcb()
    generate_netlist()  # Generate the netlist.
    # generate_svg()
