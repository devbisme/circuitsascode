![Circuits as Code banner](logos/banner.png)

[![](https://img.shields.io/pypi/v/circuitsascode.svg)](https://pypi.python.org/pypi/circuitsascode)

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
import circuitsascode as casc

vin, vout, gnd = Net("VIN"), Net("VOUT"), Net("GND")
vreg1 = circuitsascode.vreg.linear.adj_reg(vin, vout, gnd, v_vout=3.3)
...
```
