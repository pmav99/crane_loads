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
# L     :
# e_min :
# a     :
# br    :
# e     :
L       = 18
e_min   = 1.510
a       = 4
br      = 0.05

### Loads
# G,cr      :
# G,tr      :
# T,tot     :
# Qr,nom    :
Gcr     = 89.28
Gtr     = 11.84
Qr_nom  = 80

### General
# HC : Hoisting class
# FC : fatigue class
# RT : rolling type
# m  :
HC = "HC2"
FC = "S3"
RT = "IFF"
m = 0
a_rad = 0.0015

vh = 5 / 60
mf = 0.2
mw = 2
nr = 2
e1 = 0

### Dynamic coefficients
v1 = 1.1
v3 = 1
v4 = 1
v5 = 1.5
v6 = 1
