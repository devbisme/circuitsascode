# The MIT License (MIT) - Copyright (c) 2021 xesscorp

"""
PMOD(TM) Plugs & Sockets.

Warning:
    The pin numbering that Digilent uses for the PMOD connectors is completely
    different from the numbering used by the KiCad footprints, so use the
    pin names when assigning connections.

Note:
    GND/VCC pins on a PMOD *plug* usually serve as power inputs to a PMOD board.
    Therefore, these pins feed power to parts on the PMOD board so
    they are assigned to be *POWER OUTPUTS* w.r.t. on-board parts.

    GND/VCC pins on a PMOD *socket* usually serve as power outputs from
    a main board to a PMOD board that is inserted in the socket.
    Therefore, these pins feed power from the main board to the PMOD board
    so they are assigned to be *POWER INPUTS* because some part on the
    main board has to supply power to them.

Example:
    >>> from circuitsascode.interfaces.pmod import *
    >>> j1 = pmod_plug_6()
    >>> j2 = pmod_socket_6()
    >>> j3 = pmod_plug_12()
    >>> j4 = pmod_socket_12()
    >>>
    >>> j1["io[0:3]"] += j2["io[0:3]"]
    >>> j3["io[0:7]"] += j4["io[0:7]"]
    >>>
    >>> vcc, gnd = Net("VCC"), Net("GND")
    >>>
    >>> vcc += j1["VCC"], j2["VCC"], j3["VCC"], j4["VCC"]
    >>> gnd += j1["GND"], j2["GND"], j3["GND"], j4["GND"]
"""

from skidl import SKIDL, Bus, Net, Part, Pin, generate_netlist  # generate_pcb


def pmod_plug_6():
    """Returns a 6-pin (1x6) PMOD plug (male header).

    Args:
        None

    Returns:
        A Part object for a 6-pin (1x6) PMOD plug (male header).
    """
    return Part(
        name="PMOD_PLUG_6",
        tool=SKIDL,
        keywords="PMOD 1x6 plug male header",
        description="6-pin (1x6) PMOD plug (male header)",
        ref_prefix="J",
        num_units=1,
        footprint="Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Horizontal",
        do_erc=True,
        pins=[
            Pin(num="6", name="IO0", func=Pin.BIDIR, do_erc=True),
            Pin(num="5", name="IO1", func=Pin.BIDIR, do_erc=True),
            Pin(num="4", name="IO2", func=Pin.BIDIR, do_erc=True),
            Pin(num="3", name="IO3", func=Pin.BIDIR, do_erc=True),
            Pin(num="2", name="GND", func=Pin.PWROUT, do_erc=True),
            Pin(num="1", name="VCC", func=Pin.PWROUT, do_erc=True),
        ],
    )


def pmod_plug_12():
    """Returns a 12-pin (2x6) PMOD plug (male header).

    Args:
        None

    Returns:
        A Part object for a 12-pin (2x6) PMOD plug (male header).
    """
    return Part(
        name="PMOD_PLUG_12",
        tool=SKIDL,
        keywords="PMOD 2x6 plug male header",
        description="12-pin (2x6) PMOD plug (male header)",
        ref_prefix="J",
        num_units=1,
        footprint="Connector_PinHeader_2.54mm:PinHeader_2x06_P2.54mm_Horizontal",
        do_erc=True,
        pins=[
            Pin(num="12", name="IO4", func=Pin.BIDIR, do_erc=True),
            Pin(num="11", name="IO0", func=Pin.BIDIR, do_erc=True),
            Pin(num="10", name="IO5", func=Pin.BIDIR, do_erc=True),
            Pin(num="9", name="IO1", func=Pin.BIDIR, do_erc=True),
            Pin(num="8", name="IO6", func=Pin.BIDIR, do_erc=True),
            Pin(num="7", name="IO2", func=Pin.BIDIR, do_erc=True),
            Pin(num="6", name="IO7", func=Pin.BIDIR, do_erc=True),
            Pin(num="5", name="IO3", func=Pin.BIDIR, do_erc=True),
            Pin(num="4", name="GND", func=Pin.PWROUT, do_erc=True),
            Pin(num="3", name="GND", func=Pin.PWROUT, do_erc=True),
            Pin(num="2", name="VCC", func=Pin.PWROUT, do_erc=True),
            Pin(num="1", name="VCC", func=Pin.PWROUT, do_erc=True),
        ],
    )


def pmod_socket_6():
    """Returns a 6-pin (1x6) PMOD socket (female header).

    Args:
        None

    Returns:
        A Part object for a 6-pin (1x6) PMOD socket (female header).
    """
    return Part(
        name="PMOD_SOCKET_6",
        tool=SKIDL,
        keywords="PMOD 1x6 socket female header",
        description="6-pin (1x6) PMOD socket (female header)",
        ref_prefix="J",
        num_units=1,
        footprint="Connector_PinSocket_2.54mm:PinSocket_1x06_P2.54mm_Horizontal",
        do_erc=True,
        pins=[
            Pin(num="6", name="IO0", func=Pin.BIDIR, do_erc=True),
            Pin(num="5", name="IO1", func=Pin.BIDIR, do_erc=True),
            Pin(num="4", name="IO2", func=Pin.BIDIR, do_erc=True),
            Pin(num="3", name="IO3", func=Pin.BIDIR, do_erc=True),
            Pin(num="2", name="GND", func=Pin.PWRIN, do_erc=True),
            Pin(num="1", name="VCC", func=Pin.PWRIN, do_erc=True),
        ],
    )


def pmod_socket_12():
    """Returns a 12-pin (2x6) PMOD socket (female header).

    Args:
        None

    Returns:
        A Part object for a 12-pin (2x6) PMOD socket (female header).
    """
    return Part(
        name="PMOD_SOCKET_12",
        tool=SKIDL,
        keywords="PMOD 2x6 socket female header",
        description="12-pin (2x6) PMOD socket (female header)",
        ref_prefix="J",
        num_units=1,
        footprint="Connector_PinSocket_2.54mm:PinSocket_2x06_P2.54mm_Horizontal",
        do_erc=True,
        pins=[
            Pin(num="12", name="IO4", func=Pin.BIDIR, do_erc=True),
            Pin(num="11", name="IO0", func=Pin.BIDIR, do_erc=True),
            Pin(num="10", name="IO5", func=Pin.BIDIR, do_erc=True),
            Pin(num="9", name="IO1", func=Pin.BIDIR, do_erc=True),
            Pin(num="8", name="IO6", func=Pin.BIDIR, do_erc=True),
            Pin(num="7", name="IO2", func=Pin.BIDIR, do_erc=True),
            Pin(num="6", name="IO7", func=Pin.BIDIR, do_erc=True),
            Pin(num="5", name="IO3", func=Pin.BIDIR, do_erc=True),
            Pin(num="4", name="GND", func=Pin.PWRIN, do_erc=True),
            Pin(num="3", name="GND", func=Pin.PWRIN, do_erc=True),
            Pin(num="2", name="VCC", func=Pin.PWRIN, do_erc=True),
            Pin(num="1", name="VCC", func=Pin.PWRIN, do_erc=True),
        ],
    )
