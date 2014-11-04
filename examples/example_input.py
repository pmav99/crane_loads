#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Panagiotis Mavrogiorgos
# email : gmail, pmav99

"""
This file can act as input data for the calculation of the crane loads.

Some of the data are derived from the other values. If you want to give
them values yourself, just comment out the lines that calculate them
and type the values you need.
"""

# Load factors
g = 1.35

### Geometry
L       = 18                            # Length
e_min   = 1.05                          # Min distance between crab and rail
a       = 4                             # Distance between wheels
e1      = 0                             # Eccentricity of rail 1
br      = 0.05                          # Width of rail head
a_rad = 0.0015

### Loads
Gcr     = 89.28
Gtr     = 11.84
Qr_nom  = 80

### General
# HC :
# FC :
# RT :
# m  :
HC = "HC2"                              # Hoisting class
FC = "S3"                               # fatigue class
RT = "IFF"                              # rolling type
m = 0                                   # Number of pairs of coupled wheels.

vh = 6.25 / 60                          # Hoisting speed
mf = 0.2                                # friction factor
mw = 2                                  # Number of single wheel drives
nr = 2                                  # Number of wheels per axis

### Dynamic coefficients
v1 = 1.1
v3 = 1
v4 = 1
v5 = 1.5
v6 = 1
