# Circuits as Code

This is a collection of pre-built circuits written as scripts in [SKiDL](http://xesscorp.github.io/skidl).


## Description

[SKiDL](http://xesscorp.github.io/skidl) lets you create electronic circuits by writing Python scripts instead of using a schematic editor.
The `circuitsascode` auxiliary Python package gives you a library of ready-made electronic circuits that serves several purposes:

1. It provides a set of lower-level modules that you can integrate within your own designs.
1. It shows you examples of how to write SKiDL code.

## Installation

You can install this circuit library using `pip`:

```bash
pip install circuitsascode
```

## Usage

Just import the library to use a circuit module:

```py
# Import the function that creates a VGA display interface.
from circuitsascode.displays.vga import vga

# Create color and sync signals to connect to the VGA interface.
red, grn, blu = Bus(5), Bus(4), Bus(3)
hsync, vsync, gnd = Net(), Net(), Net()

# Create a VGA interface circuit customized for the widths
# of the RGB buses.
vga1 = vga(rgb=(len(red), len(grn), len(blu)))

# Connect the signals to the VGA interface circuit.
vga1.red += red
vga1.grn += grn
vga1.blu += blu
vga1.hsync += hsync
vga1.vsync += vsync
vga1.gnd += gnd
```
